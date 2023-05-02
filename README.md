# Nginx-Log-Analyzer
Nginx-Log-Analyzer is a Python-based tool for processing, analyzing, and visualizing log data from Nginx web servers logs. This tool provides a simple command-line interface for parsing Nginx log files, extracting useful information, and indexing the data into an Elasticsearch cluster.

# Features
* Parse Nginx log files and extract useful information. <br>
* Index log data into Elasticsearch for easy search and analysis. <br>
* Simple command-line interface for ease of use. <br>
* Kibana Visualizations for quick analysis of the data. <br>

# Usage
To use the Nginx-Log-Analyzer, follow these steps:

* Navigate to the root directory of the repository. <br>
* Run the nginx_log_analyzer.py script with the required arguments: <br>
`python nginx_log_analyzer.py <filename> <index_name> <elasticsearch_api> <username> <password>`
* The script will parse the log file, extract useful information, and index the data into Elasticsearch. <br>
