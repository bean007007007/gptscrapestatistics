# GPT Scrape Statistics

This repository contains a simple web scraper for [vacaturebank.nl](https://www.vacaturebank.nl).
The scraper collects vacancies for the query **"junior systeembeheerder"** and stores them in a SQLite database.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the scraper:
   ```bash
   python vacaturebank_scraper.py
   ```
3. Inspect the generated `vacatures.db` SQLite database.

Use the gathered data for further analysis with an LLM or other tools.
