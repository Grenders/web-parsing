## Web Scraping Project

## Overview
This project is designed to scrape data about tablets from Webscraper.io. The script extracts information such as title, description, price, star rating, number of reviews, and images, saving the data to a CSV file (results.csv) and a PostgreSQL database (table tablets in database scraping_db).

## Key Features
- Scrapes data using Selenium and BeautifulSoup.
- Saves data to CSV for local analysis.
- Stores data in PostgreSQL with support for updating existing records (ON CONFLICT).
- Logs operations to parser.log and console.


## Project Structure
   ```plain
   ├── alembic/                  # Alembic migration files
   ├── alembic.ini               # Alembic configuration
   ├── db.py                     # SQLAlchemy setup
   ├── models.py                 # TabletProduct model
   ├── parse.py                  # Scraping script
   ├── parser.log                # Execution log
   ├── requirements.txt          # Dependencies
   ├── results.csv               # Output CSV file
   ├── .env                      # Environment variables
   └── README.md                 # Documentation
   ```

## Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate (Linux/Mac)
   venv\Scripts\activate ( Windows )

3. Install dependencies:
    ```bash
   pip install -r requirements.txt

4. Create a .env file based on the .env.example file:
   ```bash
   cp .env.example .env

# Running the Project
Ensure PostgreSQL is running:

- Windows: Check via services.msc or run pg_ctl start.
- Linux: sudo service postgresql start.
- Mac: brew services start postgresql.

# Run the script
   ```bash
   python parse.py
