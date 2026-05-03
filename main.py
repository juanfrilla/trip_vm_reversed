from datetime import datetime, timedelta

from client import TripClient
from constants import BROWSER_VERSION, USER_AGENT
from logger import get_logger
from token_generator import TokenGenerator

if __name__ == "__main__":
    province_id = "10127"
    country_id = "95"
    city_id = "1766"
    city_name = "Lanzarote"
    checkin = datetime.now() + timedelta(days=1)
    checkout = datetime.now() + timedelta(days=2)
    logger = get_logger()
    token_generator = TokenGenerator(
        logger=logger,
        city_id=city_id,
        country_id=country_id,
        province_id=province_id,
        city_name=city_name,
        checkin=checkin,
        checkout=checkout,
    )
    phantom_token = token_generator.generate_token()
    trip_client = TripClient(
        browser_version=BROWSER_VERSION,
        user_agent=USER_AGENT,
        checkin=checkin,
        checkout=checkout,
        logger=logger,
        city_id=city_id,
        country_id=country_id,
        province_id=province_id,
        city_name=city_name,
        phantom_token=phantom_token,
    )
    trip_client.scrape()
