class Food:
    def __init__(self, code, name, calories):
        self.code = code
        self.name = name
        self.calories = calories

class Vendor:
    def __init__(self, code, name, average_calories, location, description, food_items):
        self.code = code
        self.name = name
        self.average_calories = average_calories
        self.location = location
        self.description = description
        self.food_items = food_items


a00001 = Food("a00001", "Chicken Rice", 673)
a00002 = Food("a00002", "Fried Rice", 840)
b00001 = Food("b00001", "Mee Goreng", 752)
b00002 = Food("b00002", "Just Blood", 109)

sen01 = Vendor("sen01", "McDonald's", 1207, "Sengkang", "This stuff will literally kill you and you pay us for it.", [a00001, a00002])
sen02 = Vendor("sen02", "Western Delight - Sengkang Kopitiam", 979, "Sengkang", "Come buy overpriced frozen food!", [b00001, b00002])
