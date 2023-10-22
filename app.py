from flask import Flask, request, json, render_template, jsonify
from neo4j import GraphDatabase, basic_auth
from py2neo import Graph, Node, Relationship
import pandas as pd
import xgboost as xgb
import numpy as np
import math


driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "root@420"))
graph = Graph("bolt://localhost:7687", auth=("neo4j", "root@420"))

app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    source=request.form['source']
    source=int(source)
    destination=request.form['destination']
    destination=int(destination)

    with driver.session() as session:
        # Query for travel time
        result1 = session.run("MATCH (start:Station {station_id: $source}), (end:Station {station_id: $destination}) "
                              "MATCH path = allShortestPaths((start)-[:travel_time*]->(end)) "
                              "WITH reduce(totalTime = 0, rel in relationships(path) | totalTime + rel.time) as totalTime "
                              "RETURN totalTime",
                              source=source,
                              destination=destination
                             )
        record1 = result1.single()
        if record1:
            total_time = record1['totalTime']
        else:
            total_time = "Not found"

        # Query for fare
        result2 = session.run("MATCH (origin:Station {station_id: $source})-[fare:fare]->(destination:Station {station_id: $destination}) "
                              "RETURN origin.station_name as Source, destination.station_name as Destination, fare.youth_fare as YouthClipper, fare.senior_fare as SeniorDisabledClipper,fare.clipper_start_fare as ClipperStart, fare.clipper_fare as Clipper",
                              source=source,
                              destination=destination
                             )
        record2 = result2.single()
        if record2:
            origin_name = record2['Source']
            destination_name = record2['Destination']
            youth_clipper = record2['YouthClipper']
            senior_disabled_clipper = record2['SeniorDisabledClipper']
            clipper_start = record2['ClipperStart']
            clipper = record2['Clipper']
        else:
            origin_name = "Not found"
            destination_name = "Not found"
            youth_clipper = "Not found"
            senior_disabled_clipper = "Not found"
            clipper_start = "Not found"
            clipper = "Not found"

    return render_template('result.html', total_time=total_time, source=source, destination=destination, origin_name=origin_name, destination_name=destination_name, youth_clipper=youth_clipper, senior_disabled_clipper=senior_disabled_clipper, clipper_start=clipper_start, clipper=clipper)      

@app.route('/bart-ridership', methods=['POST'])
def bart(): 
    return render_template('ridership.html') 

@app.route('/calculate-ridership', methods=['POST'])
def ridership_calculate():
    hour=int(request.form['hour'])
    day=int(request.form['day'])
    week=int(request.form['week'])
    month=int(request.form['month'])
     
    station_df = pd.read_csv("stations.csv")

    for index, row in station_df.iterrows():
        origin_id = int(row['origin_id']) 
        destination_id = int(row['destination_id'])
        t = dict(Hour=hour, Source=origin_id, Destination=destination_id, Month=month, Day=day, Week=week)
        ridership_count = predict(t)
        create_stations_ridership(ridership_count, origin_id, destination_id)
    
    return jsonify({'message': 'Ridership calculation complete'})


def create_stations_ridership(ridership_count, origin_id, destination_id):
    origin = graph.nodes.match("Station", station_id=origin_id).first()
    destination = graph.nodes.match("Station", station_id=destination_id).first()
    ridership = Relationship(origin, "ridership", destination, ridership_count=int(ridership_count))
    graph.create(ridership)

def predict(inp):
    model_xgb = xgb.Booster()
    model_xgb.load_model("bart_xgb.model")

    t_df = pd.DataFrame(inp, index=[0])
    res = model_xgb.predict(xgb.DMatrix(t_df))
    print(f"res {res}")
    return math.ceil(res)

@app.route('/station-ridership', methods=['POST'])
def station_ridership():
    source = int(request.form['source'])
    destination = int(request.form['destination'])

    with driver.session() as session:
        # Query for ridership prediction
        result3 = session.run("MATCH (start:Station {station_id: $source}), (end:Station {station_id: $destination}) "
                             "MATCH path = allShortestPaths((start)-[:travel_time*]->(end)) "
                             "WITH nodes(path) AS stations "
                             "UNWIND RANGE(0, size(stations) - 2) AS i "
                             "WITH stations[i] AS source, stations[i + 1] AS destination "
                             "MATCH (source)-[ridership:ridership]->(destination) "
                             "RETURN sum(ridership.ridership_count) AS TotalRidershipCount",
                             source=source,
                             destination=destination
                             )
        record3 = result3.single()
        if record3:
            origin_name = source
            destination_name = destination
            total_ridership_count = record3['TotalRidershipCount']
        else:
            total_ridership_count = "Not found"
        
        result4 = session.run("MATCH (origin:Station {station_id: $source})-[ridership:ridership]->(destination:Station {station_id: $destination}) "
                              "RETURN origin.station_name as Source, destination.station_name as Destination, ridership.ridership_count as RidershipCount",
                              source=source,
                              destination=destination
                             )
        record4 = result4.single()
        if record4:
            ridership_count = record4['RidershipCount']
        else:
            ridership_count = "Not found"


   
    return render_template('ridership_results.html', source=source, destination=destination, origin_name=origin_name, destination_name=destination_name, total_ridership_count=total_ridership_count, ridership_count=ridership_count)


if __name__ == '__main__':
    app.run(debug=True)


    

