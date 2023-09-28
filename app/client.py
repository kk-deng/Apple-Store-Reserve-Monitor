import logging
import time
import typing as tp

from bs4 import BeautifulSoup
from httpx import Client
from app.logger import RichHandler
from app.helper import sleep_pro
from app.config import UserSettings, settings_dev

logging.basicConfig(
    level="INFO", format="%(message)s", datefmt="[%x %X]", handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)
T = tp.TypeVar("T", bound="AppleStoreClient")


class AppleStoreClient(Client):
    def __init__(self, settings: UserSettings, **kwargs) -> None:
        kwargs.update(
            {
                "headers": {
                    "authority": "www.apple.com",
                    "accept": "*/*",
                    "accept-language": "zh-CN,zh;q=0.9,en-CA;q=0.8,en;q=0.7",
                    "dnt": "1",
                    "referer": "https://www.apple.com/ca/shop/buy-iphone/iphone-15-pro/6.7-inch-display-256gb-white-titanium",
                    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"102\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "\"Windows\"",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
                },
                "base_url": settings.BASE_URI,
            }
        )
        super().__init__(**kwargs)
        self.settings = settings
        self.instock_storename_lst = []

    def get_pickup_msg(self) -> dict:
        logger.info(f"Getting pickup info from: {self.base_url}")
        logger.info(
            f"\t => Part number: '{self.settings.PART_NUMBER}' | "
            f"Postal Code: {self.settings.LOCATION_CODE}"
        )

        resp = self.get(
            "/shop/retail/pickup-message?pl=true"
            f"&parts.0={self.settings.PART_NUMBER}"
            f"&location={self.settings.LOCATION_CODE}"
        )
        resp.raise_for_status()
        if resp.status_code not in [302, 200]:
            raise RuntimeError(f"Error while fetching: {resp}\n{resp.content}")

        # logger.info(f"\t => Pickup Info got: '{resp.status_code}'.")
        return resp.json()

    def __enter__(self: T) -> T:
        self._transport.__enter__()
        for transport in self._mounts.values():
            if transport is not None:
                transport.__enter__()
        return self


if __name__ == "__main__":
    with AppleStoreClient(settings=settings_dev) as client:
        resp_json = client.get_pickup_msg()
        print(resp_json.keys())
