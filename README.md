# Google Maps Scraper

A Python-based scraper for extracting detailed listing data from Google Maps. The scraper gathers a variety of information about businesses or listings while using rotating user agents to bypass Google's anti-scraping mechanisms.

## Features

The scraper extracts the following data fields from Google Maps listings:

1. **Job Title**: The title or name of the business or job.
2. **Photo and Images**: URLs or paths to images related to the listing.
3. **Job Group/Category**: The type or category of the listing (e.g., Restaurant, Store, etc.).
4. **Location**: Latitude and longitude coordinates of the listing.
5. **Phone Number**: Contact number associated with the listing.
6. **Hours and Days of Operation**: Business hours and operating days.
7. **Website**: Official website URL of the listing.
8. **Text Address**: Full textual address of the listing.

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Use

The scraper works by targeting specific cities and job titles. You must define the target city and job title in the `src/run.py` file before running the scraper. For example:

- **Markets in London**
- **Bars in Houston**

### Steps:

1. Open the `src/run.py` file in your text editor or IDE.
2. Locate the section where the target city and job title are defined.
3. Edit the file to include your desired search query. Example:
   ```python
   city = "London"
   job_title = "markets"
   ```
4. Save the file after making the changes.

5. Run the scraper:
   ```bash
   python src/run.py
   ```

6. The scraped data will be saved to a file in your preferred format (e.g., CSV, JSON, etc.).

### Example Usage:

To scrape data for **markets in London**, set the following in `src/run.py`:
```python
city = "London"
job_title = "markets"
```
Run the script, and the scraper will gather data specific to this query.

## Anti-Scraping Measures

This scraper uses the following techniques to avoid detection and bypass Google's blockers:

- **Rotating User Agents**: The scraper frequently changes the User-Agent header to mimic different devices and browsers.
- **Request Rate Limiting**: To prevent triggering anti-scraping mechanisms, the scraper includes delays between requests.

## Legal Disclaimer

This tool is intended for educational and personal use only. Scraping Google Maps may violate their terms of service. Use this scraper responsibly and at your own risk.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contributions

Contributions are welcome! Feel free to fork the repository and submit pull requests.

## Contact

For any issues or suggestions, please open an issue or contact the developer directly.
