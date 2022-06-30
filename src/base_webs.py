from typing import Tuple
from secret.home_scan_settings import settings
from common_defs import ResponseStatus


class DefaultWeb:
    _c_login = ""
    _c_check = ""
    _c_login_user_key = ""
    _c_login_password = ""
    _c_login_password_key = "password"
    _c_email = settings.get("email")
    _c_key = ""
    _c_status_xpath = ""
    _c_status_success = "ok"
    _c_login_button_xpath = ""
    _c_status_unpaid = "nezaplatené"

    def __repr__(self):
        return self._c_key

    @property
    def login_page(self) -> str:
        return self._c_login

    @property
    def check_page(self) -> str:
        return self._c_check

    @property
    def login_user_key(self) -> str:
        return self._c_login_user_key

    @property
    def login_password_key(self) -> str:
        return self._c_login_password_key

    @property
    def login_password(self) -> str:
        return settings.get(self._c_key).get("pwd")

    @property
    def email(self) -> str:
        return self._c_email

    @property
    def service_key(self) -> str:
        return self._c_key

    @property
    def bill_page(self) -> str:
        suff = settings.get(self._c_key).get("bill_page_suffix")
        if suff is None:
            return self._c_login
        else:
            return self._c_login + suff

    @property
    def status_xpath(self) -> str:
        return self._c_status_xpath

    @property
    def login_button(self) -> str:
        return self._c_login_button_xpath

    @property
    def status_unpaid(self) -> str:
        return self._c_status_unpaid

    def is_status_success(self, status: str) -> ResponseStatus:
        return ResponseStatus.unpaid if self._c_status_unpaid in status else ResponseStatus.paid


class SppWeb(DefaultWeb):
    _c_login = "https://moje.spp.sk/"
    _c_login_user_key = "userName"
    _c_key = "spp"
    _c_status_xpath = "/html/body/div[1]/div[4]/div[3]/div[3]/div/div[2]/div/div/div/span"
    _c_status_success = "Všetko uhradené"


class VseWeb(DefaultWeb):
    _c_login = "https://www.web-centrum.sk/nwc/domov"
    _c_key = "vse"
    _c_login_user_key = "j_username"
    _c_login_password_key = "j_password"
    _c_status_xpath = "/html/body/div[4]/div[2]/div[2]/div[2]/div/table/tbody/tr[2]/td[2]"
    _c_status_success = "Všetko uhradené"


class RtvsWeb(DefaultWeb):
    _c_login = "https://uhrady.rtvs.sk/moj-ucet/prihlasenie"
    _c_key = "rtvs"
    _c_login_user_key = "/html/body/form"


class AntikWeb(DefaultWeb):
    _c_login = "https://moj.antik.sk/"
    _c_key = "antik"
    _c_login_user_key = "login"
    _c_login_button_xpath = "/html/body/div[1]/div/div/div[2]/form/div/div[2]/button"
    _c_status_xpath = "/html/body/div[5]/div/div[2]/section/div[1]/div/div/div[1]/div/table"
    _c_status_unpaid = "Nehradené"


if __name__ == "__main__":
    a = RtvsWeb()
    print(repr(a))
    print(a.login_user_key)
    print(a.login_password_key)
