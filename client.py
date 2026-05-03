from datetime import datetime
from logging import Logger

import curl_cffi


class TripClient:
    def __init__(
        self,
        *,
        browser_version: str,
        user_agent: str,
        checkin: datetime,
        checkout: datetime,
        city_name: str,
        city_id: str,
        province_id: str,
        country_id: str,
        phantom_token: str,
        logger: Logger,
    ):
        self.session = curl_cffi.Session(impersonate="chrome146")
        self.checkin = checkin
        self.checkout = checkout
        self.city_name = city_name
        self.city_id = city_id
        self.province_id = province_id
        self.country_id = country_id
        self.phantom_token = phantom_token
        self.browser_version = browser_version
        self.user_agent = user_agent
        self.logger = logger

    def _generate_dynamic_payload(self) -> str:
        today_short = self.checkin.strftime("%Y%m%d")
        tomorrow_short = self.checkout.strftime("%Y%m%d")
        today_dash = self.checkin.strftime("%Y-%m-%d")
        tomorrow_dash = self.checkout.strftime("%Y-%m-%d")

        payload_dict = {
            "date": {
                "dateType": 1,
                "dateInfo": {
                    "checkInDate": today_short,
                    "checkOutDate": tomorrow_short,
                },
            },
            "destination": {
                "type": 1,
                "geo": {"cityId": 1766, "countryId": 95},
                "keyword": {"word": self.city_name},
            },
            "extraFilter": {
                "childInfoItems": [],
                "ctripMainLandBDCoordinate": True,
                "sessionId": "f768ec653cd34d5087a5504d15357844",  # TODO dynamic
                "extendableParams": {
                    "tripWalkDriveSwitch": "T",
                    "isUgcSentenceB": "",
                    "multiLangHotelNameVersion": "E",
                },
            },
            "filters": [
                {
                    "type": "17",
                    "title": "Recomendaciones",
                    "value": "1",
                    "filterId": "17|1",
                },
                {"type": "19", "title": "", "value": "2", "filterId": "19|2"},
                {"type": "80", "title": "Total", "value": "1", "filterId": "80|1|1"},
                {"filterId": "29|1", "type": "29", "value": "1|2"},
            ],
            "roomQuantity": 1,
            "marketInfo": {
                "received": False,
                "isRechargeSuccessful": False,
                "guideBannerInfo": {
                    "title": "Bienvenido",
                    "subItems": [],
                    "bannerSubItems": [],
                },
                "unclaimedActivityInfos": [],
                "authInfo": {"isLogin": False, "isMember": False},
                "extraInfo": {"SpecialActivityId": "T"},
                "paymentMethodIcons": [],
            },
            "paging": {"pageIndex": 2, "pageSize": 10, "pageCode": "10320668148"},
            "hotelIdFilter": {"hotelAldyShown": []},
            "head": {
                "platform": "PC",
                "cver": "0",
                "cid": "1773593048145.ef5el4dAplky",  # TODO dynamic
                "bu": "IBU",
                "group": "trip",
                "locale": "es-ES",
                "timezone": "0",
                "currency": "EUR",
                "pageId": "10320668148",  # TODO dynamic
                "vid": "1773593048145.ef5el4dAplky",  # TODO dynamic
                "isSSR": False,
                "extension": [
                    {"name": "cityId", "value": "2"},
                    {"name": "checkIn", "value": today_dash},
                    {"name": "checkOut", "value": tomorrow_dash},
                    {"name": "region", "value": "ES"},
                ],
            },
        }
        return payload_dict

    def _first_request(self):

        burp0_url = "https://es.trip.com:443/?locale=es-es"

        burp0_headers = {
            "Accept-Language": "es-ES,es;q=0.9",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Ch-Ua": '"Not-A.Brand";v="24", "Chromium";v="146"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=0, i",
            "Connection": "keep-alive",
        }
        return self.session.get(burp0_url, headers=burp0_headers)

    def _third_request(self, payload: dict):

        burp0_url = "https://es.trip.com/restapi/soa2/34951/fetchHotelList"

        burp0_headers = {
            "Sec-Ch-Ua-Platform": '"Windows"',
            "X-Ctx-User-Recognize": "IS_EU",
            "Sec-Ch-Ua": '"Not-A.Brand";v="24", "Chromium";v="146"',
            "Sec-Ch-Ua-Mobile": "?0",
            "X-Ctx-Locale": "es-ES",
            "X-Ctx-Currency": "EUR",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Locale": "es-ES",
            "X-Ctx-Ubt-Pvid": "1",
            "X-Ctx-Ubt-Vid": "1777717324742.2acfaMwHGyUd",  # TODO dynamic
            "X-Ctx-Wclient-Req": "f0d75ec1bbd573c62a95fa54806098c9",  # TODO dynamic
            "X-Ctx-Ubt-Sid": "1",
            "Accept-Language": "es-ES,es;q=0.9",
            "Currency": "EUR",
            "Phantom-Token": self.phantom_token,
            "X-Ctx-Country": "ES",
            # TODO dynamic
            # "W-Payload-Source": "1.0.9@102!KZOWquglOaTbKrb5K2KZ9PtSOPqnGrNH+XKI+XKpGSAS+6t2+XKnOlbbOrK2+ET5+rApbbbpOSTZOSAZOEAnKEVpbEAbKtb5+rbSOEA5KE4pKSb5OlTS+r4pK5bpOSTZOSAZKS4LOStnQljdG29dr1h4NZaF9bb=",
            "X-Ctx-Ubt-Pageid": "10320668148",  # TODO dynamic
            "Cookieorigin": "https://es.trip.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
            "Origin": "https://es.trip.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=1, i",
        }

        return self.session.post(burp0_url, headers=burp0_headers, json=payload)

    def scrape(self):
        payload = self._generate_dynamic_payload()
        response = self._first_request()
        response_post = self._third_request(payload)
        if response_post.status_code == 200:
            self.logger.info(response_post.json())
        else:
            self.logger.error(f"Error body: {response_post.text}")
