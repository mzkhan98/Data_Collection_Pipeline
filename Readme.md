#Data Collection Pipeline

This project is designed to collect structured and unstructured data from https://www.hotukdeals.com/, a well known Deals & Discount website. 


## Technologies Used
- Python 3.9.7
- Chromedriver: latest
- Chrome: latest
- AWS S3
- AWS RDS and Pg4Admin/ PostgreSQL
- AWS EC2 instance
- Docker and Dockerd set up on the EC2 instance
- Prometheus
- Node-Exporter
- Grafana Dashboard

## Features
Scraper code:
- run unittests for XPATHS, inputs, cookies
- takes user input
- accepts cookies
- scrapes data according to selected number of pages
- creates json file for tabular data, uploads to AWS S3 bucket and to Postgres RDS/PG4Admin
- screenshots images, 10 per page, uploaded to AWS S3

## Setup
The required libraries are:
boto3==1.23.10
pandas==1.4.2
psycopg2==2.9.3
psycopg2_binary==2.9.3
requests==2.27.1
selenium==4.2.0
SQLAlchemy==1.4.32
urllib3==1.26.9
webdriver_manager==3.7.0