# Web Scraper for Medical Equipment Data

This project is a web scraper built using Selenium and Python to collect detailed data about medical equipment from the Saudi Food and Drug Authority (SFDA) website. The scraper extracts data from multiple pages and saves it into Excel files for further analysis.

---

## Features

- Collects detailed data about medical equipment, including manufacturer details, classification, and more.
- Handles dynamic page content using Selenium.
- Saves extracted data into Excel files.
- Manages cookies for efficient session handling.
- Logs errors and retries failed pages for robustness.

---

## Prerequisites

Ensure the following are installed on your system:

1. **Python 3.8+**
2. **Google Chrome Browser**
3. **Chromedriver**: Ensure the version matches your Chrome browser.
4. **Required Python Libraries**:
   - `selenium`
   - `pandas`
   - `openpyxl` (for saving Excel files)
   - `pickle`

---

## Installation

1. Clone the repository or download the script file.
2. Install the required libraries using `pip`:
   ```bash
   pip install selenium pandas openpyxl
