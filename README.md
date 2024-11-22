# Google Maps Scraper

This project is a Google Maps scraper built using Python and Playwright. It consists of two main parts: the **scraper** and the **server**.

## Features

- **Server**: Provides two API endpoints:
  - `/status`: Check the status of the application.
  - `/request`: Accepts a JSON payload to enqueue search queries.
- **Scraper**: Listens to a Redis queue for search queries, opens multiple tabs with different browsers and user agents, and scrapes Google Maps.

## API Details

### `/request` Endpoint

Accepts a JSON payload with the following structure:

```json
{
  "place": "",
  "verb": "",
  "city": ""
}
```
The scraper combines these fields to create a search query and enqueues it for processing.

### `/request` Endpoint
Returns the current status of the server.



## How It Works

1. The **server** receives requests via the `/request` endpoint and enqueues the search queries into a Redis queue.
2. The **scraper** listens to the Redis queue, dequeues search queries, and opens multiple tabs with different browser instances and user agents.
3. The scraper processes the search query by interacting with Google Maps.

## Requirements

- Python 3.12
- [Poetry](https://python-poetry.org/) for dependency management
- Redis server

## Setup and Installation

1. Clone the repository:
   git clone git@github.com:AmirEspahbodi/google-map-scraper.git
   cd git@github.com:AmirEspahbodi/google-map-scraper.git

2. Install dependencies:
  ```bash
     poetry install
  ```

3. Install Playwright browsers:
  ```bash
     playwright install
  ```

5. Start the application:
  ```bash
     poetry run python run_app.py
  ```
   
