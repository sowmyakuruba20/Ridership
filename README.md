# Ridership

NODES 2023

Project Title: Enhancing Decision-Making and Rider Experience in the BART Transit System through Predictive Analytics and Graph Databases

Project Objective:
The primary objective of this project is to leverage the power of Neo4j, a graph database, and machine learning to optimize the Bay Area Rapid Transit (BART) system by addressing key challenges and enhancing the rider experience. The project encompasses the following key aspects:

Ridership Prediction: Develop an accurate machine learning model to predict the ridership between any two BART stations. This prediction will enable BART authorities to proactively allocate resources, plan schedules, and optimize services to accommodate fluctuating demand effectively.
Network-Wide Ridership Estimation: Utilize the predictive models to estimate the ridership between any two stations within the entire BART network. This capability will facilitate informed decision-making regarding station-specific resource allocation, crowd management, and infrastructure improvements.
Travel Time Calculation: Calculate and provide the most efficient travel time between any two BART stations. This information will enable commuters and passengers to plan their journeys more effectively, promoting customer satisfaction and a seamless travel experience.
Fare Estimation: Compute the fare cost for traveling between two stations within the BART system. Accurate fare estimation supports both travelers and BART authorities by ensuring transparency and helping passengers make budget-conscious decisions.
By addressing these objectives, this project aims to transform the BART Transit System into a more efficient, data-driven, and rider-centric network. The integration of Neo4j, machine learning, and real-time data updates will empower decision-makers and riders with the insights needed for informed choices, leading to improved resource allocation, operational efficiency, and a better overall BART experience.

Methodology

1. Data Collection and Understanding: The primary dataset for this project is sourced from the official Bay Area Rapid Transit (BART) website, accessible at https://www.bart.gov/. This dataset encompasses critical information related to the BART transit system, including ridership fare data, ridership reports, and detailed travel time records between stations.

2. Data Preparation: This involves data cleaning, preprocessing, and feature selection
Is done using Python and its library pandas. 
The fare data was initially stored in well-structured tables. To prepare this data for integration into Neo4j and the subsequent graph creation, it was necessary to perform table merging and data transformation operations. This process ensured that the data was appropriately formatted and compatible with Neo4j's graph database structure.The Time related data between connecting stations was scraped using Google APIs. The ridership data in the form of the report we did data cleansing using pandas so that the data could be fed into the ML model. This transformation was done within the model development phase.

3. Creating Graph database:

Graph Model: 
Nodes -  station: station_id, station_name
Relationships
time: travel_time
fare: clipper_fare, clipper_start_fare, senior_fare, youth_fare
ridership: ridership_count

Station: Each station in the BART transit system is represented as a node in the Neo4j graph model. This node type encapsulates various attributes and information related to each station.

Time: The "Time" relationship, represented as an edge between two stations, signifies the time taken to travel between those two specific stations. These time relationships exist only between directly connected stations. The network of time relationships, when visualized, closely resembles the structure of the BART transit map. This connectivity enables the approximate prediction of travel time between any two stations by traversing the path and summing up the individual time values. Additionally, this network structure facilitates pathfinding between stations, which can be valuable for various analytical purposes, including centrality analysis and route planning.

Fare: The "Fare" relationship signifies the fare associated with traveling from one station to any other station in the network. Unlike the collective fare for a sequence of connected stations, the fare relationship accounts for the specific fare associated with each individual station-to-station journey. This allows for precise fare calculations and analysis for any station pair in the BART system.

Ridership: The "Ridership" relationship exists between stations and encompasses the "ridership_count" attribute. This attribute is populated using the predictions from the ML model (bart_xgb_model). The model calculates and predicts the ridership count for each station based on a set of features, including hour, day, week, and month. The "Ridership" relationship thus quantifies the ridership interactions between stations, providing insights into passenger flows and trends within the BART transit system.

Creating Graph database Neo4j using py2neo

The Neo4j graph, based on the provided model, was constructed in the neo4j database environment through Jupyter notebook using  Python in conjunction with the Py2neo package, a powerful tool that facilitates connections to Neo4j database servers, as well as the creation and manipulation of the graph structure within Neo4j.

First, we established the fundamental building blocks by generating nodes to represent each BART transit station, and we interlinked these nodes using 'fare' edges. These fare edges defined the pricing relationships between one station to every other station, forming a foundational element of our graph.

Following this, we enhanced the graph by introducing 'time' edges. These time edges were selectively applied to nodes corresponding to stations strategically positioned along the BART map path. They symbolized the travel time between these interconnected stations. 

Source: https://www.bart.gov/system-map

As we can see on the BART transit map, MacArthur serves as a critical junction connecting three stations: Ashby, Rockridge, and 19th St/Oakland. The Neo4j graph below illustrates this connectivity. In the graph, station_id 11 corresponds to MacArthur, which serves as a central hub connecting stations 12, 10, and 33, representing 19th St/Oakland, Ashby, and Rockridge, respectively. While there is a fare edge connecting each station to every other station, including itself, the time edge specifically follows the layout of the BART map.

The image below visually depicts all the BART station nodes interconnected with both fare (green edges) and time (red edges) relationships. This representation provides a clear visualization of how these stations are linked in the Neo4j graph, highlighting the connections based on both travel time and fare information.

Leveraging the Neo4j Data Science Playground for Station Centrality Analysis

In our project, we harnessed the power of Neo4j's Data Science Playground to gain valuable insights into station centrality within the BART transit system. By employing the Centralities algorithm, specifically the Betweenness algorithm, we sought to determine the most central station within the network. In the context of the BART transit system, it helps pinpoint stations that play a critical role in facilitating passenger flows and efficient transfers.


As you can see MacArthur is the critical junction that has the highest centrality score when compared to other stations

4. Model development
Create an ML Model for Ridership Prediction
Data Preprocessing: The first step in model development is to preprocess the dataset obtained from BART, making it compatible with the XGBoost model. This includes cleaning and organizing the data, as well as feature engineering to extract relevant information. We only use Source, Destination, Hour, Day, Week, and Month columns as features.
 The data is split into training, validation, and test sets in the ratio of (80:10:10) to facilitate model evaluation. 
The XGBoost model is trained on the prepared dataset. During training, the model learns to make predictions by optimizing a loss function, aiming to minimize the difference between predicted and actual ridership counts. The model is trained with a specified learning rate = 0.01 , and the number of training rounds = 60  is determined to achieve optimal performance.
Learning rate: 0.01
XGBoost model parameters: {"max_depth": 15, "tree_method": "gpu_hist"}
Number of rounds/epochs: 60
Evaluate the model's accuracy using metrics like RMSE (Root Mean Square Error).

After model training, we assessed its accuracy, which resulted in the following metrics:
Training accuracy (RMSE): 3.32920
Validation accuracy (RMSE): 3.65339

Once trained, the model is evaluated using a test dataset to determine its predictive accuracy.

The index on the x-axis corresponds to the index of the input vectors that contain the descriptive feature for the XGB model(source, destination, hour, day, week, month). The Rider Count on the y-axis represents the actual count of riders for the given input vector. It's evident that the model's predictions closely align with the actual values, indicating the model's effectiveness in capturing and approximating the target variable.

The model is saved as bart_xgb.model, which is then used in the backend of the web application.

5. Integration with Neo4j:
Data Update: Populate the Neo4j graph with the predicted ridership counts using the ML model. Create "ridership" relationships between stations and assign the "ridership_count" property.
The ridership prediction using the ML model:
Ridership predictions between stations are determined through the utilization of the bart_xgb_model, which has been trained on key features such as Hour, Day, Week, and Month. To predict ridership counts between every pair of stations, we implement an iterative process. Subsequently, we create new relationships in our graph, specifically denoted as "ridership," and assign these relationships a property named "ridership_count" This property quantifies the predicted ridership count between the two respective stations, effectively updating our Neo4j graph with this valuable information. Integrating the ML model with Neo4j to update the ridership count property on the relationship edges between the stations.

The figure illustrates the "ridership edge" for the same example that we used when constructing the graph. It showcases the connections between various stations and visualizes the predicted ridership count.

The image below visually depicts all the BART station nodes interconnected with fare (green edges), time (red edges), and ridership(yellow edges) relationships. This representation provides a clear visualization of how these stations are linked in the Neo4j graph, highlighting the connections based on travel time, fare, and ridership information.

6. Development of the Web Application:
Backend Development: Develop the backend of your web application using Flask and Python. This includes setting up routes for data retrieval and processing.
Frontend Development: Create the user interface with HTML and Bootstrap. Design features such as the Time and Fare Calculator and Ridership Prediction functionalities.
Database Connectivity: Use the Py2neo package to connect to the Neo4j database for real-time queries.This connection empowers us to perform real-time queries with the database server, executed as Cypher queries via driver sessions on the backend.

Backend
Time and Fare Calculator:

Travel Time Calculation:
We employed Neo4j's shortest path algorithms to calculate the optimal travel time between any two stations in the BART system. This provides real-time travel time estimates for riders, which can be accessed through our web app

MATCH (start:Station {station_id: $source}), (end:Station {station_id: $destination})
MATCH path = allShortestPaths((start)-[:travel_time*]->(end))
WITH reduce(totalTime = 0, rel in relationships(path) | totalTime + rel.time) as totalTime
RETURN totalTime


Fare Calculation:
Utilizing  BART's fare structure data to calculate the fare for a journey between any two stations w.r.t to the ridership category. This enables riders to estimate their travel costs and optimize their journeys based on fare information.
MATCH (origin:Station {station_id: $source})-[fare:fare]->(destination:Station {station_id: $destination})
RETURN origin.station_name as Source, destination.station_name as Destination,
fare.youth_fare as YouthClipper, fare.senior_fare as SeniorDisabledClipper,
fare.clipper_start_fare as ClipperStart, fare.clipper_fare as Clipper


Front end

Predicting the ridership between any two stations 

Backend
Utilize the predictive models to estimate the ridership between any two stations within the entire BART network
MATCH (origin:Station {station_id: $source})-[ridership:ridership]->(destination:Station {station_id: $destination})
RETURN origin.station_name as Source, destination.station_name as Destination, ridership.ridership_count as RidershipCount

Utilize Neo4j's graph traversal capabilities to calculate the total ridership count between any two given stations. This involves finding the paths between stations and aggregating the ridership data along these paths.
MATCH (start:Station {station_id: $source}), (end:Station {station_id: $destination})
MATCH path = allShortestPaths((start)-[:travel_time*]->(end))
WITH nodes(path) AS stations
UNWIND RANGE(0, size(stations) - 2) AS i
WITH stations[i] AS source, stations[i + 1] AS destination
MATCH (source)-[ridership:ridership]->(destination)
RETURN sum(ridership.ridership_count) AS TotalRidershipCount

An intuitive web application that allows users to input the necessary features for predicting ridership across all stations.

Frontend

Predicting the ridership between the stations Millbrae and Antioch.

The Estimated Ridership from source to destination, with a count of 2, signifies that precisely 2 riders embarked at Millbrae and disembarked at Antioch.
The Total Ridership count from source to destination, amounting to 115, represents the collective count of 115 riders who boarded the train at any point along the route between Millbrae and their final stop at Antioch.

7. Visualize Results and Analysis:
Visualize graph-based insights, fare calculations, travel times, and ridership predictions through the web app.

8. Documentation and Reporting:

Key takeaways from the project 
Graph Databases for Complex Relationships: Neo4j excels in handling complex relationships, making it ideal for modeling and managing the intricate connections within the BART transit system. The project demonstrates how graph databases can efficiently represent and query such relationships.
Property Graphs: Neo4j's support for property graphs, where relationships can have properties like travel time and fare information, proves essential for this project's data representation.
Cypher Query Language: The use of Cypher queries, Neo4j's query language, demonstrates the power of expressing complex graph traversals and data retrieval in an intuitive and efficient manner.
Data Integration: Neo4j's seamless integration with Python (through libraries like Py2neo) highlights its compatibility with popular programming languages, facilitating easy data import, management, and real-time interaction.
Machine Learning Integration: The project showcases how Neo4j can be integrated with machine learning models like XGBoost, expanding its utility in advanced analytics and predictive modeling.
User-Friendly Applications: By integrating Neo4j with a user-friendly Flask web application, the project underscores how graph databases can be utilized to deliver real-time insights to end-users in an accessible manner.
Pathfinding and Calculations: Neo4j's shortest path algorithms facilitate optimal travel time calculations between stations. This is a critical feature for providing real-time travel time estimates to riders.
Centrality Analysis: Neo4j's graph algorithms, such as the Betweenness algorithm, are invaluable for centrality analysis. The project showcases how these algorithms can identify central stations critical for passenger flows and network resilience.


