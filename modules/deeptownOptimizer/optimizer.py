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
        print(self.mines)

    def best_mines(self, ore):
        if ore not in self.mines["0"].keys():
            raise ValueError("{ore} is not a correct ore.".format(ore=ore))
        ordered_mines = [(k, v) for k, v in self.mines.items()]
        ordered_mines.sort(key=lambda x: x[1][ore], reverse = True)
        return ordered_mines

    def to_make(self, item, quantity=1):
        if item not in self.items.keys():
            raise ValueError("{item} is not a correct item.".format(item=item))
        number_of_craft = quantity/self.items[item]["quantity"]
        if number_of_craft % 1 != 0:
            number_of_craft = (number_of_craft // 1)+1
        time = self.items[item]["time"]*number_of_craft
        value = self.items[item]["value"]*number_of_craft*self.items[item]["quantity"]
        needed = {}
        for resource, quantity in self.items[item]["required"].items():
            needed.update({resource: quantity*number_of_craft})
        return {"time": time, "value": value, "needed": needed}

    def recursive_to_make(self, item, quantity=1):
        # Compute needed time and resource for craft item
        result = self.to_make(item, quantity)
        # For each needed resource try to craft it
        for i, q in result["needed"].keys():
            try:
                temp_result = self.recursive_to_make(i, g)
            result["time"] = result["time"] + temp_result["time"]
            for

        return result
