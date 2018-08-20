import copy
import datetime
import json
import os


class Optimizer():
    def __init__(self):
        self.mines = {}
        self.items = {}
        # get mine stats
        with open(os.path.join("modules", "deeptownOptimizer", "mines.json")) as mines:
            self.mines = json.load(mines)
        # get items stats
        with open(os.path.join("modules", "deeptownOptimizer", "items.json")) as items:
            self.items = json.load(items)
        # Add zero values to mine stat
        ores = self.mines["0"].keys()
        for area, stats in self.mines.items():
            for ore in ores:
                if self.mines[area].get(ore) is None:
                    self.mines[area].update({ore: 0})

    def best_mines(self, ore):
        if ore not in self.mines["0"].keys():
            raise ValueError("{ore} is not a correct ore.".format(ore=ore))
        ordered_mines = [(k, v) for k, v in self.mines.items()]
        ordered_mines.sort(key=lambda x: x[1][ore], reverse=True)
        return ordered_mines

    def to_make(self, item, quantity=1):
        if item not in self.items.keys():
            raise ValueError("{item} is not a correct item.".format(item=item))
        number_of_craft = int(quantity / self.items[item]["quantity"])
        if number_of_craft % 1 != 0:
            number_of_craft = int((number_of_craft // 1) + 1)
        time = self.items[item]["time"] * number_of_craft
        value = self.items[item]["value"] * number_of_craft * self.items[item]["quantity"]
        needed = {}
        for resource, quantity in self.items[item]["required"].items():
            needed.update({resource: quantity * number_of_craft})
        return {"time": time, "value": value, "needed": needed}

    def recursive_to_make(self, item, quantity=1):
        if item in self.items.keys():
            needed = self.to_make(item, quantity)
            results = [(item, quantity, needed["time"])]
            for needed_item, needed_quantity in needed["needed"].items():
                needed_result = self.recursive_to_make(needed_item, needed_quantity)
                already_crafted = [result[0] for result in results]
                index = 0
                for i, q, t in needed_result:
                    print(i, q, t)
                    if i in already_crafted:
                        results[already_crafted.index(i)] = (
                            results[already_crafted.index(i)][0],
                            results[already_crafted.index(i)][1] + q,
                            results[already_crafted.index(i)][2] + t
                        )
                    else:
                        results.append((i, q, t))
                    index += 1
            return results
        else:
            return [(item, quantity, 0)]
