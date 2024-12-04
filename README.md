# Google Maps Scraper

- This project is a Google Maps scraper built using Python and Playwright. It consists of two main parts: the **scraper** and the **server**.
- The Scraper scrap title, phone, address, latitude and longitude, category, website, active_hours and first picture of listing.
- it will scrap all liastings that represented in a scrollbar after enter search query (after scrolling to the end of scrollbar).


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
  "city": "",
  "listing_category": "",
  "listing_type": "",
  "province": "",
  "verb": ""
}
```
The scraper combines these fields (listing_type + verb + city + province) to create a search query and enqueues it for processing. use all fields to create excel file for storing search result. 

### `/status` Endpoint
Returns the current status of the server.



## How It Works

1. The **server** receives requests via the `/request` endpoint and enqueues the search queries into a Redis queue.
2. The **scraper** listens to the Redis queue, dequeues search queries, and opens multiple tabs with different browser instances and user agents.
3. The scraper processes the search query by interacting with Google Maps.

## Requirements

- Python 3.12
- [Poetry](https://python-poetry.org/) for dependency management
- Redis server
- Playwright

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
     poetry run playwright install
     poetry run playwright install-deps
  ```

5. Start the application:
  ```bash
     poetry run python run_app.py
  ```
   
