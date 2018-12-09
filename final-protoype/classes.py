class Food:
    def __init__(self, code, name, calories):
        self.code = code
        self.name = name
        self.calories = calories

    def set_code(self, code):
        self.code = code

    def set_name(self, name):
        self.name = name

    def set_calories(self, calories):
        self.calories = calories

    def get_code(self):
        return self.code

    def get_name(self):
        return self.name

    def get_calories(self):
        return self.calories


class Vendor:
    def __init__(self, code, name, average_calories, location, description, food_items):
        self.code = code
        self.name = name
        self.average_calories = average_calories
        self.location = location
        self.description = description
        self.food_items = food_items

    def set_code(self, code):
        self.code = code

    def set_name(self, name):
        self.name = name

    def set_average_calories(self, average_calories):
        self.average_calories = average_calories

    def set_location(self, location):
        self.location = location

    def set_description(self, description):
        self.description = description

    def set_food_items(self, food_items):
        self.food_items = food_items

    def get_code(self):
        return self.code

    def get_name(self):
        return self.name

    def get_average_calories(self):
        return self.average_calories

    def get_location(self):
        return self.location

    def get_description(self):
        return self.description

    def get_food_items(self):
        return self.food_items


a00001 = Food("a00001", "Chicken Rice", 673)
a00002 = Food("a00002", "Fried Rice", 840)
b00001 = Food("b00001", "McSpicy", 752)
b00002 = Food("b00002", "Straight-Up Blood", 109)

food_list = [a00001, a00002, b00001, b00002]

sen01 = Vendor("sen01", "McDonald's", 1207, "Sengkang", "This stuff will literally kill you and you pay us for it.", [a00001, a00002])
sen02 = Vendor("sen02", "Western Delight - Sengkang Kopitiam", 979, "Sengkang", "Come buy overpriced frozen food!", [b00001, b00002])
