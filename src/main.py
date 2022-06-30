from tabulate import tabulate
from base_webs import SppWeb, VseWeb, AntikWeb
from authorize import Authorize
from datetime import date
from common_defs import ResponseStatus
from typing import List
import csv
from secret.home_scan_settings import settings
from logger import log_settings

headers = ["Date", "Service", "Status", "Info"]
web_list = [SppWeb(), VseWeb(), AntikWeb()]
app_log = log_settings()


def save_to_file(res_list: List):
    with open(settings.get("output_file"), "a", encoding="Windows-1250", newline="") as f:
        writer = csv.writer(f)
        writer .writerow(res_list)


def main():
    app_log.info("App starts")
    today = date.today()
    day = today.strftime("%Y-%m-%d")
    res_list = list()
    for service in web_list:
        app_log.info(f"processing {service.service_key}...")
        new_list: List = list()
        new_list.append(day)
        new_list.append(service.service_key)
        app_log.debug("Authorization starts")
        inst = Authorize(service)
        resp = inst.login()
        if resp.status == ResponseStatus.unable_to_check:
            new_list.append(resp.status)
            new_list.append(resp.info)
            app_log.debug(f"save into file row: {new_list}")
            res_list.append(new_list)
            continue
        app_log.debug("authorization successfull")
        app_log.debug("check payment status")
        resp = inst.bill_page()
        new_list.append(resp.status)
        new_list.append(resp.info)
        res_list.append(new_list)
        app_log.info(f"Payment status: {resp.status}")
        app_log.debug(f"save into file row: {new_list}")
        save_to_file(new_list)
    print(tabulate(res_list, headers=headers))
    app_log.info("App stops")


if __name__ == "__main__":
    main()
