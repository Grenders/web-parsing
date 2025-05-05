import logging
import sys
from decimal import Decimal
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from sqlalchemy.dialects.postgresql import insert
from webdriver_manager.chrome import ChromeDriverManager
import csv
import dataclasses
from bs4 import BeautifulSoup, Tag
from db import SessionLocal
from models import TabletProduct
from sqlalchemy.exc import SQLAlchemyError

MAIN_URL = "https://webscraper.io/"
SCRAP_URL = urljoin(MAIN_URL, "test-sites/e-commerce/more/computers/tablets")

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)8s]: %(message)s",
    handlers=[
        logging.FileHandler("parser.log"),
        logging.StreamHandler(sys.stdout),
    ],
)


@dataclasses.dataclass
class TabletsProduct:
    title: str
    description: str
    price: Decimal
    stars_rating: int
    reviews: int
    images: str


TABLES_FIELDS = [field.name for field in dataclasses.fields(TabletsProduct)]


def get_more_in_pages(driver: webdriver) -> None:
    while True:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".card-body"))
            )
            items_before = len(driver.find_elements(By.CSS_SELECTOR, ".card-body"))

            pagination = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        ".btn.btn-block.btn-primary.ecomerce-items-scroll-more",
                    )
                )
            )

            if "display: none;" in pagination.get_attribute("style"):
                break

            logging.info(f"Loaded {items_before} items. Clicking 'More' button...")
            pagination.click()

            WebDriverWait(driver, 10).until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, ".card-body"))
                > items_before
            )
        except Exception as e:
            logging.warning(f"Stopped loading more items due to exception: {e}")
            break


def parse_single_table(table: Tag) -> TabletsProduct:
    try:
        return TabletsProduct(
            title=table.select_one(".title")["title"].strip(),
            description=table.select_one(".description").text.strip(),
            price=Decimal(
                table.select_one(".price.float-end.pull-right")
                .text.replace("$", "")
                .strip()
            ),
            stars_rating=len(table.select(".ws-icon.ws-icon-star")),
            reviews=int(
                table.select_one(".float-end.review-count").text.strip().split()[0]
            ),
            images=table.select_one(".img-fluid.card-img-top")["src"],
        )
    except AttributeError as e:
        logging.error(f"Failed to parse table: {e}")
        raise


def get_tablets_page_products(driver: webdriver) -> [TabletsProduct]:
    logging.info("Start parsing")
    driver.get(SCRAP_URL)
    get_more_in_pages(driver)
    text = driver.page_source
    soup = BeautifulSoup(text, "html.parser")
    tablets = soup.select(".card-body")
    return [parse_single_table(table) for table in tablets]


def write_tablets_csv(tablets: [TabletsProduct]) -> None:
    with open("results.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(TABLES_FIELDS)
        writer.writerows([dataclasses.astuple(tablet) for tablet in tablets])


def save_to_db(tablets: [TabletsProduct]) -> None:
    try:
        with SessionLocal() as session:
            for tablet in tablets:
                stmt = insert(TabletProduct).values(
                    title=tablet.title,
                    description=tablet.description,
                    price=tablet.price,
                    stars_rating=tablet.stars_rating,
                    reviews=tablet.reviews,
                    images=tablet.images,
                )
                stmt = stmt.on_conflict_do_update(
                    constraint="uq_tablet_title",
                    set_={
                        "description": tablet.description,
                        "price": tablet.price,
                        "stars_rating": tablet.stars_rating,
                        "reviews": tablet.reviews,
                        "images": tablet.images,
                    },
                )
                session.execute(stmt)
            session.commit()
            logging.info(f"Successfully processed {len(tablets)} tablets in database")
    except SQLAlchemyError as e:
        logging.error(f"Failed to save tablets to database: {e}")
        session.rollback()
        raise
    except Exception as e:
        logging.error(f"Unexpected error while saving to database: {e}")
        session.rollback()
        raise


def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        tablets = get_tablets_page_products(driver)
        write_tablets_csv(tablets)
        save_to_db(tablets)
    except Exception as e:
        logging.error(f"Error in main: {e}")
        raise
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
