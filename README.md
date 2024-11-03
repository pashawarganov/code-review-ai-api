# Code Review AI API 👨‍💻

> Python Fast Api project 

This is a Fast Api powered API for getting reviews to GitHub repositories. 

## Run service on your machine

* Set env file with your own credentials
```shell
git clone https://github.com/pashawarganov/code-review-ai-api
cd train_station_api_service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

## Run with Docker

Docker should be installed
```shell
docker-compose build
docker-compose up
```

# Scaling

Redis could serve as a cache to reduce requests to the GitHub and GroqAl APIs by storing recent analysis results and requests 
to popular repositories, which would minimize latency and overhead. A database with support for horizontal scaling, such as PostgreSQL, 
is suitable for storing metadata about repositories and requests. To get around the rate limit, you should implement a request queue (e.g. via RabbitMQ) 
to control the flow to the API and balance the load. In addition, you can use a queue system for viewing requests 
with prioritization of requests from key users, ensuring high availability and reliability of the system under heavy load.
