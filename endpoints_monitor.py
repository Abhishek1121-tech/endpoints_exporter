import time
import httpx
import logging
import argparse
from prometheus_client import start_http_server, Gauge
from configparser import ConfigParser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define custom metric
service_live_metric = Gauge('endpoint_service_live_status', 'Response code of the URL endpoint', ['url', 'name'])
response_time_metric = Gauge('endpoint_response_time_seconds', 'Response time of the URL endpoint', ['url', 'name'])
status_code_metric = Gauge('endpoint_status_code', 'HTTP Status code of the URL endpoint', ['url', 'name'])

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Endpoint metrics exporter')
parser.add_argument('--config', required=True, help='Path to the configuration file')
args = parser.parse_args()

# Read configuration from the provided file
config = ConfigParser()
config.read(args.config)

# Read global settings from configuration
SLEEP_TIME = config.getint('Global', 'sleep_time', fallback=30)
PORT = config.getint('Global', 'port', fallback=8000)


# Function to fetch data from a URL and update metrics
def fetch_and_update_metrics(section_name):
    # Extract configuration values from the provided configuration object
    url = config.get(section_name, 'url')
    name = config.get(section_name, 'name')
    timeout_seconds = config.getint(section_name, 'timeout')
    follow_redirects = config.getboolean(section_name, 'follow_redirects', fallback=True)
    max_redirects = config.getint(section_name, 'max_redirects', fallback=5)  # Default to 5 redirects

    try:
        response = fetch_data(url, timeout_seconds, follow_redirects, max_redirects)
        update_metrics(url, name, response)
    
    except httpx.RequestError as e:
        handle_request_error(url, name, e)

def fetch_data(url, timeout_seconds, follow_redirects, max_redirects):
    with httpx.Client(http2=True, timeout=timeout_seconds) as client:
        logging.info(f"Fetching data from {url}...")
        redirect_count = 0
        response = client.get(url)

        while follow_redirects and response.status_code in (301, 302, 303, 307, 308) and redirect_count < max_redirects:
            redirect_url = response.headers.get('location')
            response = client.get(redirect_url)
            redirect_count += 1

        logging.info(f"Fetch from {url} completed successfully.")
        return response

def update_metrics(url, name, response):
    response_time = response.elapsed.total_seconds()
    service_live_metric.labels(url=url, name=name).set(1)
    response_time_metric.labels(url=url, name=name).set(response_time)
    status_code_metric.labels(url=url, name=name).set(response.status_code)

def handle_request_error(url, name, e):
    logging.error(f"An error occurred while fetching data from {url}: {e}")
    service_live_metric.labels(url=url, name=name).set(0)
    response_time_metric.labels(url=url, name=name).set(0)
    status_code_metric.labels(url=url, name=name).set(0)


if __name__ == '__main__':
    # Start the Prometheus HTTP server
    start_http_server(PORT)  # Expose metrics on specified port

    # Get sections with a specific prefix and iterate through them
    prefix = "Endpoint_"
    matching_sections = [section for section in config.sections() if section.startswith(prefix)]

    # Periodically fetch data and update metrics for each matching endpoint
    while True:
        for section_name in matching_sections:
            fetch_and_update_metrics(section_name)
        logging.info(f"Waiting for {SLEEP_TIME} seconds before fetching again...")
        time.sleep(SLEEP_TIME)  # Wait for sleep_time seconds before fetching again

