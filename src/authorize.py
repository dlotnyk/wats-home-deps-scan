from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebElement
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException, TimeoutException
from selenium.webdriver.common.by import By
from time import sleep
from typing import Optional, Tuple
from base_webs import DefaultWeb, SppWeb
from common_defs import StatusInfo, ResponseStatus
from logger import log_settings

app_log = log_settings()


class Authorize:
    resp_inv_path = StatusInfo(ResponseStatus.unable_to_check, "Invalid xPath")
    resp_ok = StatusInfo(ResponseStatus.in_check_progress, "ok")
    __find_by_list: Tuple = (By.NAME, By.XPATH)

    def __init__(self, service: DefaultWeb) -> None:
        self.service = service
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.timout = 5

    def __repr__(self) -> str:
        return f"Authorize of {self.service.service_key}"

    def _wait_for_element(self, by: By, value: str):
        WebDriverWait(self.driver, self.timout).until(EC.presence_of_element_located((by, value)))

    def _find_field(self, by: By, value: str) -> Optional[WebElement]:
        try:
            self._wait_for_element(by=by, value=value)
            return self.driver.find_element(by=by, value=value)
        except NoSuchElementException:
            self.driver.close()
            app_log.error(f"{value} not found by {by}")
            return None
        except TimeoutException:
            app_log.error(f"Timeout error for {value} {by}")
            return None

    def _find_field_in_by_list(self, value: str) -> Optional[WebElement]:
        for by in self.__find_by_list:
            ret = self._find_field(by=by, value=value)
            if ret is not None:
                return ret
        return None

    def _login_in(self, pwd_field: WebElement) -> StatusInfo:
        if self.service.login_button == "":
            pwd_field.submit()
            return self.resp_ok
        else:
            try:
                ret = self._find_field(by=By.XPATH, value=self.service.login_button)
                if ret is not None:
                    ret.click()
                    return self.resp_ok
                else:
                    return self.resp_inv_path
            except NoSuchElementException:
                self.driver.close()
                app_log.error(f"element not found `{self.service.login_button}`")
                return self.resp_inv_path

    def login(self) -> StatusInfo:
        try:
            self.driver.get(self.service.login_page)
            # sleep(1)
            name = self._find_field_in_by_list(self.service.login_user_key)
            if name is None:
                return self.resp_inv_path
            name.send_keys(self.service.email)
            # sleep(1)
            pwd = self._find_field_in_by_list(self.service.login_password_key)
            if pwd is None:
                return self.resp_inv_path
            pwd.send_keys(self.service.login_password)
            self._login_in(pwd)
            sleep(1)
            return self.resp_ok
        except NoSuchElementException:
            app_log.error(f"username or pwd element is not found while login")
            self.driver.close()
            return self.resp_inv_path
        except Exception as ex:
            app_log.error(f"{ex}")
            self.driver.close()
            return StatusInfo(ResponseStatus.unable_to_check, f"{ex}")

    def bill_page(self) -> StatusInfo:
        try:
            if self.service.bill_page != self.service.login_page:
                self.driver.get(self.service.bill_page)
            sleep(1)
            element = self._find_field(by=By.XPATH, value=self.service.status_xpath)
            if element is not None:
                outtext = element.text
                text = outtext.replace("\n", " ")
                return StatusInfo(self.service.is_status_success(text), text)
            else:
                return self.resp_inv_path
        except InvalidSessionIdException:
            app_log.error("driver already closed")
            return StatusInfo(ResponseStatus.unable_to_check, "driver closed")
        except NoSuchElementException:
            app_log.error("status element not found")
            return self.resp_inv_path
        except Exception as ex:
            app_log.error(f"{ex}")
            return StatusInfo(ResponseStatus.unable_to_check, f"{ex}")
        finally:
            self.driver.quit()


if __name__ == "__main__":
    try:
        A = Authorize(SppWeb())
        resp = A.login()
        print(resp.status)
        sleep(1)
        resp = A.bill_page()
        print(resp.status, resp.info)
        sleep(1)
        # sleep(120)
        if resp.status != ResponseStatus.unable_to_check:
            print("driver close")
            A.driver.close()
    except InvalidSessionIdException:
        print("ok")
