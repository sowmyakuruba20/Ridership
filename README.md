# Enhancing Decision-Making and Rider Experience in the BART Transit System through Predictive Analytics and Graph Databases

[![NODES2023: Improving Bay Area Rapid Transit](https://ytcards.demolab.com/?id=8ZmOzmQ_xq8&title=NODES2023%3A+Improving+Bay+Area+Rapid+Transit&lang=en&timestamp=1713139200&background_color=%230d1117&title_color=%23ffffff&stats_color=%23dedede&max_title_lines=2&width=250&border_radius=5&duration=00 "NODES2023: Improving Bay Area Rapid Transit")](https://www.youtube.com/watch?v=8ZmOzmQ_xq8&list=PL9Hl4pk2FsvUu4hzyhWed8Avu5nSUXYrb&index=36)

## Project Objective
This project aims to optimize the Bay Area Rapid Transit (BART) system by leveraging Neo4j, a graph database, and machine learning to enhance rider experience and address key operational challenges.

## Key Features
- Ridership Prediction: Develop a machine learning model to accurately predict ridership between any two BART stations, enabling proactive resource allocation and service optimization.
- Network-Wide Estimation: Estimate ridership across the entire BART network, facilitating informed decision-making for resource allocation and infrastructure improvements.
- Travel Time Calculation: Provide efficient travel time estimates between stations, helping commuters plan their journeys and enhancing customer satisfaction.
- Fare Estimation: Compute fare costs for journeys between stations, ensuring transparency and aiding passengers in budget-conscious decisions.
  
## Getting Started
- Download the input files.
- Install the Neo4j Desktop application and create a new database.
- Run bart.ipynb, replacing Neo4j server authentication details in the Jupyter notebook.
- Execute app.py with the command python app.py, updating Neo4j server authentication details.
- Access the Flask application at http://localhost:5000.
- Select the "BART Ridership" button and choose the desired time period for ridership estimation.
  
## Methodology
- Data Collection: Sourced from the official BART website, the dataset includes ridership fare data, reports, and travel time records.
  
- Data Preparation: Clean and preprocess data using Python and Pandas, merging tables and transforming data for Neo4j compatibility. Time-related data is scraped using Google APIs.
  
- Graph Database Creation:
* Nodes: Represent each BART station with attributes like station_id and station_name.
* Relationships: Define travel time, fare, and ridership relationships to facilitate efficient queries and analysis.
  
- Model Development:
Preprocess data for the XGBoost model, utilizing features such as Source, Destination, Hour, Day, Week, and Month.
Train the model and evaluate its accuracy using RMSE metrics.
Integration with Neo4j: Update the graph with predicted ridership counts, creating relationships that quantify ridership between stations.

- Web Application Development:
* Backend: Built with Flask and Python, enabling data retrieval and processing.
* Frontend: User interface designed with HTML and Bootstrap, featuring travel time and fare calculators, and ridership prediction functionalities.
  
- Results Visualization: Display insights, fare calculations, travel times, and ridership predictions through the web application.
  
- Documentation and Reporting: Highlight the project's key takeaways, including the effectiveness of graph databases in managing complex relationships, seamless integration with machine learning, and user-friendly applications.
  
## Conclusion
This project demonstrates the potential of combining predictive analytics and graph databases to enhance public transit systems, offering valuable insights for decision-makers and improving the overall rider experience. This version enhances clarity, organization, and professionalism while maintaining essential details. It uses headings and bullet points for better readability and flow.
