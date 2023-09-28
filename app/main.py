import random
import os
import sys
import logging
import time
import typing as tp
from datetime import datetime, timedelta
# Used to import from parent folder src
GRANDFA = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(GRANDFA)

from app.logger import RichHandler
from app.helper import sleep_pro
from app.client import AppleStoreClient
from app.config import settings_dev
from app.pickup_data import PickupData, Store
from app.telegram_bot import TelegramBot


logging.basicConfig(
    level="INFO", format="%(message)s", datefmt="[%x %X]", handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)
tg_bot = TelegramBot(spider_name="AppleStore")


def collect_available_stores(pickup_data: PickupData) -> list[Store]:
    store_lst = pickup_data.body.stores
    available_store_lst = []
    for store in store_lst:
        regular = store.partsAvailability.MU6Q3VC_A.messageTypes.regular
        if regular.storeSelectionEnabled is True:
            available_store_lst.append(store)

    return available_store_lst


def collect_store_name_lst(store_lst: list[Store]) -> list[str]:
    return sorted([store.storeName for store in store_lst])


def main(client: AppleStoreClient):
    resp_json = client.get_pickup_msg()
    pickup_data = PickupData.model_validate(resp_json)
    available_store_lst = collect_available_stores(pickup_data=pickup_data)
    store_name_lst = collect_store_name_lst(store_lst=available_store_lst)
    
    resp_store_lst = pickup_data.body.stores
    random_gap = random.randint(50, 70)

    if store_name_lst != client.instock_storename_lst:
        instock_msg = (
            f"[IN STOCK!] {len(store_name_lst)}/{len(resp_store_lst)} stores: "
            f"{', '.join(store_name_lst)}"
        )
        logger.warning(instock_msg)

        client.instock_storename_lst = store_name_lst
    else:
        logger.info(f"['OUT OF STOCK'] {len(resp_store_lst)} stores received. Sleeping {random_gap} s")
    
    sleep_pro(random_gap)


if __name__ == "__main__":
    try:
        while True:
            try:
                client_prod = AppleStoreClient(settings=settings_dev)
                main(client=client_prod)
            except Exception as error:
                logger.error(f"Error: {error}")
                sleep_pro(60)
    except KeyboardInterrupt:
        logger.info("Ctrl + C. Exiting ...")
