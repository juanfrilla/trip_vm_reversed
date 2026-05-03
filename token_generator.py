import math
import random as _random
import time
import uuid as uuid_lib
from datetime import datetime, timezone
from logging import Logger
from urllib.parse import quote

import requests

from constants import (
    CONSTANT_STRING,
    HOSTNAME,
    JS_SAFE_CHARS,
    LITTLE_STRING,
    SEPARATORS,
    USER_AGENT,
)


class TokenGenerator:
    def __init__(
        self,
        *,
        logger: Logger,
        city_id: str,
        city_name: str,
        province_id: str,
        country_id: str,
        checkin: datetime,
        checkout: datetime,
    ):
        self.logger = logger
        self.city_id = city_id
        self.city_name = city_name
        self.province_id = province_id
        self.country_id = country_id
        self.checkin = checkin
        self.checkout = checkout

    def _build_dynamic_url(
        self,
    ):

        base_url = f"https://es.{HOSTNAME}/hotels/list"
        query_params = {
            "city": self.city_id,
            "cityName": self.city_name,
            "provinceId": self.province_id,
            "countryId": self.country_id,
            "districtId": "0",
            "checkin": self.checkin.strftime("%Y-%m-%d"),
            "checkout": self.checkout.strftime("%Y-%m-%d"),
            "barCurr": "EUR",
            "searchType": "CT",
            "searchWord": self.city_name,
            "searchValue": f"19|{self.city_id}*19*{self.city_id}*1",
            "searchCoordinate": "BAIDU_-1_-1_0|GAODE_-1_-1_0|GOOGLE_-1_-1_0|NORMAL_29.0468535_-13.5899733_0",
            "crn": "1",
            "adult": "2",
            "children": "0",
            "searchBoxArg": "t",
            "travelPurpose": "0",
            "ctm_ref": "ix_sb_dl",
            "domestic": "false",
            "listFilters": "29|1*29*1|2*2",
            "locale": "es-ES",
            "curr": "EUR",
        }

        response = requests.PreparedRequest()
        response.prepare_url(base_url, query_params)
        return response.url

    def _add32(self, a, b):
        return (a + b) & 0xFFFFFFFF

    def _rotl(self, x, n):
        x &= 0xFFFFFFFF
        return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

    def _md5_F(self, b, c, d):
        return (b & c) | (~b & d)

    def _md5_G(self, b, c, d):
        return (b & d) | (c & ~d)

    def _md5_H(self, b, c, d):
        return b ^ c ^ d

    def _md5_I(self, b, c, d):
        return c ^ (b | ~d)

    def _str_to_words(self, s):
        length = len(s)
        extra_blocks = length // 64 + 1
        blocks = extra_blocks * 16
        words = [0] * blocks
        for i, ch in enumerate(s):
            words[i >> 2] |= (ord(ch) & 0xFF) << ((i % 4) * 8)
        words[length >> 2] |= 0x80 << ((length % 4) * 8)
        words[blocks - 2] = (length * 8) & 0xFFFFFFFF
        words[blocks - 1] = length // 0x20000000
        return words

    def _word_to_hex(self, n):
        n &= 0xFFFFFFFF
        return "".join(f"{(n >> (i * 8)) & 0xFF:02x}" for i in range(4))

    def _custom_md5(self, input_str: str) -> str:

        K = [
            0xD76AA478,
            0xE8C7B756,
            0x242070DB,
            0xC1BDCEEE,
            0xF57C0FAF,
            0x4787C62A,
            0xA8304613,
            0xFD469501,
            0x698098D8,
            0x8B44F7AF,
            0xFFFF5BB1,
            0x895CD7BE,
            0x6B901122,
            0xFD987193,
            0xA679438E,
            0x49B40821,
            0xF61E2562,
            0xC040B340,
            0x265E5A51,
            0xE9B6C7AA,
            0xD62F105D,
            0x02441453,
            0xD8A1E681,
            0xE7D3FBC8,
            0x21E1CDE6,
            0xC33707D6,
            0xF4D50D87,
            0x455A14ED,
            0xA9E3E905,
            0xFCEFA3F8,
            0x676F02D9,
            0x8D2A4C8A,
            0xFFFA3942,
            0x8771F681,
            0x6D9D6122,
            0xFDE5380C,
            0xA4BEEA44,
            0x4BDECFA9,
            0xF6BB4B60,
            0xBEBFBC70,
            0x289B7EC6,
            0xEAA127FA,
            0xD4EF3085,
            0x04881D05,
            0xD9D4D039,
            0xE6DB99E5,
            0x1FA27CF8,
            0xC4AC5665,
            0xF4292244,
            0x432AFF97,
            0xAB9423A7,
            0xFC93A039,
            0x655B59C3,
            0x8F0CCC92,
            0xFFEFF47D,
            0x85845DD1,
            0x6FA87E4F,
            0xFE2CE6E0,
            0xA3014314,
            0x4E0811A1,
            0xF7537E82,
            0xBD3AF235,
            0x2AD7D2BB,
            0xEB86D391,
        ]
        S = [
            7,
            12,
            17,
            22,
            7,
            12,
            17,
            22,
            7,
            12,
            17,
            22,
            7,
            12,
            17,
            22,
            5,
            9,
            14,
            20,
            5,
            9,
            14,
            20,
            5,
            9,
            14,
            20,
            5,
            9,
            14,
            20,
            4,
            11,
            16,
            23,
            4,
            11,
            16,
            23,
            4,
            11,
            16,
            23,
            4,
            11,
            16,
            23,
            6,
            10,
            15,
            21,
            6,
            10,
            15,
            21,
            6,
            10,
            15,
            21,
            6,
            10,
            15,
            21,
        ]

        h0, h1, h2, h3 = 0x67452309, 0xEFCDAB87, 0x98BADCFE, 0x10325476

        M = self._str_to_words(input_str)
        num_blocks = len(M) // 16

        for blk in range(num_blocks):
            W = M[blk * 16 : blk * 16 + 16]
            a, b, c, d = h0, h1, h2, h3

            for i in range(64):
                if i < 16:
                    f = self._md5_F(b, c, d)
                    g = i
                elif i < 32:
                    f = self._md5_G(b, c, d)
                    g = (5 * i + 1) % 16
                elif i < 48:
                    f = self._md5_H(b, c, d)
                    g = (3 * i + 5) % 16
                else:
                    f = self._md5_I(b, c, d)
                    g = (7 * i) % 16

                f &= 0xFFFFFFFF
                temp = d
                d = c
                c = b
                b = self._add32(
                    self._rotl(
                        self._add32(self._add32(a, f), self._add32(W[g], K[i])), S[i]
                    ),
                    b,
                )
                a = temp

            h0 = self._add32(h0, a)
            h1 = self._add32(h1, b)
            h2 = self._add32(h2, c)
            h3 = self._add32(h3, d)

        return (
            self._word_to_hex(h0)
            + self._word_to_hex(h1)
            + self._word_to_hex(h2)
            + self._word_to_hex(h3)
        )

    def _random_char(self) -> str:
        return chr(math.ceil(_random.random() * 94) + 36)

    def _add_noise(self, value: str) -> str:
        chars = [self._random_char() for _ in range(6)]
        prefix = chars[0] + chars[2] + chars[4]
        suffix = chars[1] + chars[3] + chars[5]
        return prefix + str(value) + suffix

    def _compute_checksum(self, s: str) -> int:
        acc = 0
        for i, ch in enumerate(s):
            acc += ord(ch) % (i + 100)
        return acc % 43

    def _shuffle_alphabet(self, alphabet: str, salt: str) -> str:
        if not salt:
            return alphabet
        arr = list(alphabet)
        v = p = j = 0
        i = len(arr) - 1
        while i > 0:
            v = v % len(salt)
            integer = ord(salt[v])
            p = p + integer
            j = (integer + v + p) % i
            arr[i], arr[j] = arr[j], arr[i]
            v += 1
            i -= 1
        return "".join(arr)

    def _to_custom_base(self, n: int, alphabet: str) -> str:
        result = ""
        while True:
            result = alphabet[n % len(alphabet)] + result
            n = n // len(alphabet)
            if not n:
                break
        return result

    def _compute_token(self, combined: str) -> str:
        checksum = self._compute_checksum(combined)
        first_char = CONSTANT_STRING[checksum]
        string_to_work = f"{first_char}c{HOSTNAME}{CONSTANT_STRING}"
        sliced = string_to_work[:43]
        alphabet = self._shuffle_alphabet(CONSTANT_STRING, sliced)

        result = ""
        combined_len = len(combined)
        for i, ch in enumerate(combined):
            code = ord(ch)
            encoded = self._to_custom_base(code, alphabet)
            result += encoded
            if i < combined_len - 1:
                first_char_code = ord(encoded[0])
                sep_idx = (code % (first_char_code + i)) % len(SEPARATORS)
                result += SEPARATORS[sep_idx]
            salt = f"{first_char}c{HOSTNAME}{alphabet[:43]}"
            alphabet = self._shuffle_alphabet(alphabet, salt)
        return f"1004-common-{first_char}{result}"

    def _generate_first_string(self, now: int, uid: str) -> str:

        return f"{now}{USER_AGENT}{uid}"

    def generate_token(self):

        now = int(time.time() * 1000)
        uid = str(uuid_lib.uuid4())
        timezone_offset = -int(
            datetime.now(timezone.utc).astimezone().utcoffset().total_seconds() // 60
        )
        dynamic_url = self._build_dynamic_url()
        encoded_uri = quote(dynamic_url[:200], safe=JS_SAFE_CHARS)

        md5_output = self._custom_md5(self._generate_first_string(now, uid))
        md5_noised = self._add_noise(md5_output)
        timestamp_noised = self._add_noise(now)
        uri_noised = self._add_noise(encoded_uri)
        noised = self._add_noise("")
        uuid_noised = self._add_noise(uid)
        littlestr_noised = self._add_noise(LITTLE_STRING)
        color_depth_noised = self._add_noise("32")
        win32_noised = self._add_noise("Win32")
        timezone_noised = self._add_noise(timezone_offset)
        language_noised = self._add_noise("es-ES")
        screen_res_noised = self._add_noise("1920x1080")
        screen_avail_noised = self._add_noise("1920x1032")
        second_noised = self._add_noise("")
        normal_noised = self._add_noise("normal")
        minus1_1 = self._add_noise("-1")
        minus1_2 = self._add_noise("-1")
        minus1_3 = self._add_noise("-1")
        minus1_4 = self._add_noise("-1")
        _100_noised = self._add_noise("100")
        minus1_5 = self._add_noise("-1")
        minus1_6 = self._add_noise("-1")

        fields = [
            md5_noised,
            timestamp_noised,
            uri_noised,
            noised,
            uuid_noised,
            littlestr_noised,
            color_depth_noised,
            win32_noised,
            timezone_noised,
            language_noised,
            screen_res_noised,
            screen_avail_noised,
            second_noised,
            normal_noised,
            minus1_1,
            minus1_2,
            minus1_3,
            minus1_4,
            _100_noised,
            minus1_5,
            minus1_6,
        ]

        combined = "#".join(fields)
        token = self._compute_token(combined)

        self.logger.info(f"Token length: {len(token)}")
        self.logger.info(f"Token: {token[:80]}...")
        return token
