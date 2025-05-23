## Web Scraping Project

## Overview
This project is designed to scrape data about tablets from Webscraper.io. The script extracts information such as title, description, price, star rating, number of reviews, and images, saving the data to a CSV file (results.csv) and a PostgreSQL database.

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
   ├── .env.sample               # Environment variables
   ├── pyproject.toml            # Main project configuration file
   ├── poetry.lock               # Contains committed versions of all dependencies, including sub-dependencies
   └── README.md                 # Documentation
   
   ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Grenders/web-parsing.git

2. Install Poetry:
   ```bash
   pip install poetry

3. Install dependencies:
    ```bash
   poetry install

4. Activate the virtual environment:
    ```bash
   poetry shell

5. Create a .env file based on the .env.example file:
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
