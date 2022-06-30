from tabulate import tabulate
from base_webs import SppWeb, VseWeb, AntikWeb
from authorize import Authorize
from datetime import date
from common_defs import ResponseStatus
from typing import List
import csv
from secret.home_scan_settings import settings

headers = ["Date", "Service", "Status", "Info"]
web_list = [SppWeb(), VseWeb(), AntikWeb()]


def save_to_file(res_list: List):
    with open(settings.get("output_file"), "a", encoding="Windows-1250", newline="") as f:
        writer = csv.writer(f)
        writer .writerow(res_list)


def main():
    today = date.today()
    day = today.strftime("%Y-%m-%d")
    print(day)
    res_list = list()
    for idx, service in enumerate(web_list):
        new_list: List = list()
        print(service)
        new_list.append(day)
        new_list.append(service.service_key)
        inst = Authorize(service)
        resp = inst.login()
        if resp.status == ResponseStatus.unable_to_check:
            new_list.append(resp.status)
            new_list.append(resp.info)
            continue
        resp = inst.bill_page()
        new_list.append(resp.status)
        new_list.append(resp.info)
        res_list.append(new_list)
        save_to_file(new_list)
    print(tabulate(res_list, headers=headers))


if __name__ == "__main__":
    main()
