import os
import random

from fs.ftpfs import FTPFS
from fs.osfs import OSFS
from fs import path
import re
import requests
import bs4

fileSystem = None

if os.environ.get("FTP_ADDRESS", False) and os.environ.get("FTP_USER", False) and os.environ.get("FTP_PASS", False):
    print("FTP")
    fileSystem = FTPFS(os.environ["FTP_ADDRESS"], user=os.environ["FTP_USER"], passwd=os.environ["FTP_PASS"],
                       timeout=600)
else:
    print("OS")
    fileSystem = OSFS(os.getcwd())


def format_string(text):
    text = text.replace(" ", "").replace("-", "").replace("_", "").lower()
    return text


def get_all_item_urls():
    page = requests.get("https://deeptownguide.com/Items")
    item_urls = []
    if page.status_code == 200:
        regex = re.compile(r"/Items/Details/[0-9]+/([a-zA-Z0-9]|-)*", re.MULTILINE)
        item_urls_match = regex.finditer(str(page.content))
        for match in item_urls_match:
            if "https://deeptownguide.com" + match.group(0) not in item_urls:
                item_urls.append("https://deeptownguide.com" + match.group(0))
    return item_urls


def get_item_info(url):
    result = {"type": None,
              "building": None,
              "value": None,
              "quantity": 0,
              "needed": {}}
    page = requests.get(url)
    texte = str(page.content).replace(" ", "").replace("\n", "").replace(r"\n", "")

    # regex used to find infos
    type_regex = re.compile(r"<strong>Type</strong><br/>\w*")
    value_regex = re.compile(r"<strong>SellPrice</strong><br/>([0-9]|,)*")
    building_regex = re.compile(r"<divclass=\"panelpanel-default\"><divclass=\"panel-headingtext-center\"><h4style=\"di"
                                r"splay:inline;\"><spanclass=\"text-capitalize\">\w*</span>iscreatedfromthisrecipe</h4>"
                                r"</div><divclass=\"panel-body\"><divclass=\"table-responsivecol-sm-12\"><tableclass=\""
                                r"tabletable-striped\"><thead><tr><th>BuildingName</th><th>UnlockedatDepth</th><th>Cost"
                                r"ToUnlock</th><th>TimeRequired</th><th>AmountCreated</th><th>ItemsRequired</th></tr></"
                                r"thead><tbody><tr><td><ahref=\"/Buildings/Details/[0-9]+/\w+")
    time_regex = re.compile(r"<divclass=\"panelpanel-default\"><divclass=\"panel-headingtext-center\"><h4style=\"displa"
                            r"y:inline;\"><spanclass=\"text-capitalize\">\w*</span>iscreatedfromthisrecipe</h4></div><d"
                            r"ivclass=\"panel-body\"><divclass=\"table-responsivecol-sm-12\"><tableclass=\"tabletable-s"
                            r"triped\"><thead><tr><th>BuildingName</th><th>UnlockedatDepth</th><th>CostToUnlock</th><th"
                            r">TimeRequired</th><th>AmountCreated</th><th>ItemsRequired</th></tr></thead><tbody><tr><td"
                            r"><ahref=\"/Buildings/Details/[0-9]+/\w+\"><imgsrc=\"/images/placeholder\.png\"data-src=\""
                            r"/images/ui/(\w|[0-9]|-)+\.png\"alt=\"\w*\"class=\"Icon36pxlazyload\"/>\w*</a></td><td>[0-"
                            r"9]*</td><td>([0-9]|,)*</td><td>([0-9]+|Seconds?|Minutes?|Hours?)+")
    quantity_regex = re.compile(r"<divclass=\"panelpanel-default\"><divclass=\"panel-headingtext-center\"><h4style=\"di"
                                r"splay:inline;\"><spanclass=\"text-capitalize\">\w*</span>iscreatedfromthisrecipe</h4>"
                                r"</div><divclass=\"panel-body\"><divclass=\"table-responsivecol-sm-12\"><tableclass=\""
                                r"tabletable-striped\"><thead><tr><th>BuildingName</th><th>UnlockedatDepth</th><th>Cost"
                                r"ToUnlock</th><th>TimeRequired</th><th>AmountCreated</th><th>ItemsRequired</th></tr></"
                                r"thead><tbody><tr><td><ahref=\"/Buildings/Details/[0-9]+/\w+\"><imgsrc=\"/images/place"
                                r"holder\.png\"data-src=\"/images/ui/(\w|[0-9]|-)+\.png\"alt=\"\w*\"class=\"Icon36pxlaz"
                                r"yload\"/>\w*</a></td><td>[0-9]*</td><td>([0-9]|,)*</td><td>([0-9]+|Seconds?|Minutes?|"
                                r"Hours?)+</td><td>[0-9]+")
    needed_regex = re.compile(r"</td><td>(<ahref=\"/Items/Details/[0-9]+/(\w|-)+\"><imgsrc=\"/images/placeholder.png\"d"
                              r"ata-src=\"/images/ui/([a-zA-Z]|-|\.)+\"alt=\"\w*\"class=\"\w*\"/>\w+</a>(<br/>)?)+")

    type_iter = type_regex.finditer(str(texte))
    value_iter = value_regex.finditer(str(texte))
    building_iter = building_regex.finditer(str(texte))
    time_iter = time_regex.finditer(str(texte))
    quantity_iter = quantity_regex.finditer(str(texte))
    needed_iter = needed_regex.finditer(str(texte))

    # Extract value from regex result
    result["type"] = format_string(re.sub(r"<strong>Type</strong><br/>", "", str(type_iter.__next__().group(0))))
    result["value"] = int(
        re.sub(r"<strong>SellPrice</strong><br/>", "", str(value_iter.__next__().group(0))).replace(
            ",", ""))
    # Extract for recipe
    try:
        result["building"] = format_string(re.sub(
            r"<divclass=\"panelpanel-default\"><divclass=\"panel-headingtext-center\"><h4style=\"di"
            r"splay:inline;\"><spanclass=\"text-capitalize\">\w*</span>iscreatedfromthisrecipe</h4>"
            r"</div><divclass=\"panel-body\"><divclass=\"table-responsivecol-sm-12\"><tableclass=\""
            r"tabletable-striped\"><thead><tr><th>BuildingName</th><th>UnlockedatDepth</th><th>Cost"
            r"ToUnlock</th><th>TimeRequired</th><th>AmountCreated</th><th>ItemsRequired</th></tr></"
            r"thead><tbody><tr><td><ahref=\"/Buildings/Details/[0-9]+/",
            "",
            str(building_iter.__next__().group(0))))
        time_str = str(
            re.sub(r"<divclass=\"panelpanel-default\"><divclass=\"panel-headingtext-center\"><h4style=\"displa"
                   r"y:inline;\"><spanclass=\"text-capitalize\">\w*</span>iscreatedfromthisrecipe</h4></div><d"
                   r"ivclass=\"panel-body\"><divclass=\"table-responsivecol-sm-12\"><tableclass=\"tabletable-s"
                   r"triped\"><thead><tr><th>BuildingName</th><th>UnlockedatDepth</th><th>CostToUnlock</th><th"
                   r">TimeRequired</th><th>AmountCreated</th><th>ItemsRequired</th></tr></thead><tbody><tr><td"
                   r"><ahref=\"/Buildings/Details/[0-9]+/\w+\"><imgsrc=\"/images/placeholder\.png\"data-src=\""
                   r"/images/ui/(\w|[0-9]|-)+\.png\"alt=\"\w*\"class=\"Icon36pxlazyload\"/>\w*</a></td><td>[0-"
                   r"9]*</td><td>([0-9]|,)*</td><td>",
                   "",
                   str(time_iter.__next__().group(0))))
        # Time:
        time_str = time_str.replace("s", "")  # remove plural
        time_list = re.split("([0-9]+)", time_str)
        if time_list[0] == '':
            del time_list[0]
        time = 0
        for number, unit in zip(time_list[::2], time_list[1::2]):
            if unit == "Second":
                time += int(number)
            elif unit == "Minute":
                time += int(number) * 60
            elif unit == "Hour":
                time += int(number) * 60 * 60
        print(time)

        result["quantity"] = int(str(re.sub("<divclass=\"panelpanel-default\"><divclass=\"panel-headingtext-center\"><h"
                                            "4style=\"display:inline;\"><spanclass=\"text-capitalize\">\w*</span>iscrea"
                                            "tedfromthisrecipe</h4></div><divclass=\"panel-body\"><divclass=\"table-res"
                                            "ponsivecol-sm-12\"><tableclass=\"tabletable-striped\"><thead><tr><th>Build"
                                            "ingName</th><th>UnlockedatDepth</th><th>CostToUnlock</th><th>TimeRequired<"
                                            "/th><th>AmountCreated</th><th>ItemsRequired</th></tr></thead><tbody><tr><t"
                                            "d><ahref=\"/Buildings/Details/[0-9]+/\w+\"><imgsrc=\"/images/placeholder\."
                                            "png\"data-src=\"/images/ui/(\w|[0-9]|-)+\.png\"alt=\"\w*\"class=\"Icon36px"
                                            "lazyload\"/>\w*</a></td><td>([0-9]|,)*</td><td>([0-9]|,)*</td><td>([0-9]+|Seconds?"
                                            "|Minutes?|Hours?)+</td><td>",
                                            "",
                                            quantity_iter.__next__().group(0))))
        needed_text = re.sub(r"</td><td>", "", needed_iter.__next__().group(0))
        item_name_iter = re.finditer(r"<ahref=\"/Items/Details/[0-9]+/(\w|-)+", str(needed_text))
        item_quantity_iter = re.finditer(r"class=\"\w*\"/>[A-Za-z]+[0-9]+", str(needed_text))

        for item_name_match, item_quantity_match in zip(item_name_iter, item_quantity_iter):
            item_name = re.sub(r"<ahref=\"/Items/Details/[0-9]+/", "", item_name_match.group(0))
            item_quantity = int(re.sub(r"class=\"\w*\"/>[A-Za-z]+", "", item_quantity_match.group(0)))
            result["needed"].update({format_string(item_name): item_quantity})


    except StopIteration:
        pass

    return result

def get_sector_info():
    page = requests.get("https://deeptownguide.com/Items")
    num_regex = re.compile(r"<tr><tdclass=\"([a-zA-Z]|-)*\">[0-9]+")



def update_data(file_system):
    items = {}
    urls_item = get_all_item_urls()
    for item_url in urls_item:
        items.update({
            format_string(re.sub("https://deeptownguide.com/Items/Details/[0-9]+/", "", item_url)): get_item_info(
                item_url)
        })
    return None



if __name__ == "__main__":
    update_data()
