import json
import os
from fs.osfs import OSFS
import re
import requests

fileSystem = None


def format_string(text):
    text = text.replace(" ", "").replace("-", "").replace("_", "").lower()
    return str(text)


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
              "time": 0,
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
                              r"ata-src=\"/images/ui/([a-zA-Z]|-|\.)+\"alt=\"\w*\"class=\"\w*\"/>(\w|,)+</a><br/>)+")

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
        result['time'] = int(time)

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
        item_quantity_iter = re.finditer(r"class=\"\w*\"/>[A-Za-z]+([0-9]|,)+", str(needed_text))

        for item_name_match, item_quantity_match in zip(item_name_iter, item_quantity_iter):
            item_name = re.sub(r"<ahref=\"/Items/Details/[0-9]+/", "", item_name_match.group(0))
            item_quantity = int(
                re.sub(r"class=\"\w*\"/>[A-Za-z]+", "", item_quantity_match.group(0)).replace(",", "").replace(
                    ".", ""))
            result["needed"].update({format_string(item_name): item_quantity})


    except StopIteration:
        pass

    return result


def get_sector_info():
    page = requests.get("https://deeptownguide.com/Areas/Resources")
    texte = str(page.content).replace(" ", "").replace("\n", "").replace(r"\n", "")
    line_regex = re.compile(r"<tr><tdclass=\"([a-zA-Z]|-)*\">[0-9]+</td>(<td>(<ahref=\"/Items/Details/[0-9]+/\w+\"><img"
                            r"src=\"/images/placeholder\.png\"data-src=\"/images/ui/(\w|-)+\.png\"alt=\"\w*\"class=\"\w"
                            r"*\"/><br/>\w*</a><br/>([0-9]|\.|%)+|&nbsp;)</td>)+")
    num_regex = re.compile(r"<tr><tdclass=\"([a-zA-Z]|-)*\">[0-9]+")
    item_regex = re.compile(r"<td>(<ahref=\"/Items/Details/[0-9]+/\w+\"><imgsrc=\"/images/placeholder\.png\"data-src=\""
                            r"/images/ui/(\w|-)+\.png\"alt=\"\w*\"class=\"\w*\"/><br/>\w*</a><br/>([0-9]|\.|%)+|&nbsp;)"
                            r"</td>")
    item_name_regex = re.compile(r"(<ahref=\"/Items/Details/[0-9]+/\w+|&nbsp;)")
    quantity_regex = re.compile(r"<br/>([0-9]|\.)+")

    line_iter = line_regex.finditer(texte)

    etages = {}
    liste_items = []
    for line in line_iter:
        etage_iter = num_regex.finditer(line.group(0))
        etage = int(re.sub(r"<tr><tdclass=\"text-bold\">", "", etage_iter.__next__().group(0)))
        item_iter = item_regex.finditer(line.group(0))
        items = {}
        for item in item_iter:
            name_iter = item_name_regex.finditer(item.group(0))
            name = str(re.sub(r"(<ahref=\"/Items/Details/[0-9]+/|&nbsp;)", "", name_iter.__next__().group(0)))
            if name != "":
                quantity_iter = quantity_regex.finditer(item.group(0))
                quantity = float(re.sub("<br/>", "", quantity_iter.__next__().group(0))) / 100
                items.update({name: quantity})
                if name not in liste_items:
                    liste_items.append(name)
        etages.update({str(etage): items})
    etages.update({"0": {name: 0 for name in liste_items}})
    return etages


def update_data():
    items = {}
    urls_item = get_all_item_urls()
    print(len(urls_item))
    a = 0
    for item_url in urls_item:
        a += 1
        items.update({
            str(format_string(re.sub("https://deeptownguide.com/Items/Details/[0-9]+/", "", item_url))):
                get_item_info(item_url)
        })
        print(a * 100 / len(urls_item), "%")
    with open('items.json', "w") as dest_file:
        json.dump(items, dest_file)
    with open('mines.json', "w") as dest_file:
        json.dump(get_sector_info(), dest_file)
    return None


if __name__ == "__main__":
    print(get_item_info('https://deeptownguide.com/Items/Details/702/stage-ii'))
    update_data()
