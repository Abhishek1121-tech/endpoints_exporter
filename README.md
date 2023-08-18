# Endpoints Exporter

![GitHub](https://img.shields.io/github/license/Abhishek1121-tech/endpoints_exporter)
![GitHub stars](https://img.shields.io/github/stars/Abhishek1121-tech/endpoints_exporter?style=social)

Endpoints Exporter is a tool designed to collect and export endpoint availability and response time metrics. It can be used to monitor the health and performance of various services and APIs.

## Features

- Monitor multiple endpoints concurrently
- Record response time and HTTP status codes
- Export metrics in a format compatible with Prometheus

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Abhishek1121-tech/endpoints_exporter.git
   cd endpoints_exporter

2. Create Configuration:
    Edit the endpoints.yaml file to define the endpoints you want to monitor: Add your section in the endpoints_exporter_config.ini file. Prefix with Endpoint_ will be considered for health check.
    ```
    [Global]
    sleep_time = 300
    port = 8000

    [Endpoint_Example]
    url = https://example.com
    name = Example Website
    timeout = 10
    follow_redirects = false
    max_redirects = 5

    [EndpointTest]
    url = http://fakeurl.com
    name = Test Endpoint
    timeout = 10
    follow_redirects = true
    max_redirects = 5
    ```

3. Build the Docker Image:
    Build the Docker image using the provided Dockerfile:
    ```bash
    docker build -t endpoints-monitor:0.0.1 .

4. Run the Docker Container:
    Run the Docker container based on the image you just built: 
    ```bash
    docker run -p 8000:8000 endpoints-monitor:0.0.1 python endpoints_monitor.py --config /app/endpoints_exporter_config.ini

5. Access Prometheus Metrics:
    The Prometheus metrics server is now running inside the Docker container. Access the metrics at http://localhost:8000/metrics in your web browser. These metrics can be scraped by Prometheus for monitoring and analysis.

6. Metric currnetly exposed by exporter
    ```
    service_live_metric = Gauge('endpoint_service_live_status', 'Response code of the URL endpoint', ['url', 'name'])
    response_time_metric = Gauge('endpoint_response_time_seconds', 'Response time of the URL endpoint', ['url', 'name'])
    status_code_metric = Gauge('endpoint_status_code', 'HTTP Status code of the URL endpoint', ['url', 'name'])
    ```
## Customization
    Modify endpoints.yaml to add or remove endpoints for monitoring.
    Adjust the Dockerfile or application code according to your requirements.
    Contributing
    Contributions are welcome! If you find a bug or have an enhancement in mind, please open an issue or submit a pull request.

## License
    This project is licensed under the MIT License.









