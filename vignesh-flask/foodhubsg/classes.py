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
    def __init__(self, code, name, average_calories, location, location_code, description, food_items, image_location):
        self.code = code
        self.name = name
        self.average_calories = average_calories
        self.location = location
        self.location_code = location_code
        self.description = description
        self.food_items = food_items
        self.__rating = 0
        self.image_location = image_location

    def set_code(self, code):
        self.code = code

    def set_name(self, name):
        self.name = name

    def set_average_calories(self, average_calories):
        self.average_calories = average_calories

    def set_location(self, location):
        self.location = location

    def set_location_code(self, location_code):
        self.location_code = location_code

    def set_description(self, description):
        self.description = description

    def set_food_items(self, food_items):
        self.food_items = food_items

    def set_food_items(self, food_items):
        self.food_items = food_items

    def set_rating(self, rating):
        self.rating = rating

    def set_image_location(self, image_location):
        self.image_location = image_location

    def get_code(self):
        return self.code

    def get_name(self):
        return self.name

    def get_average_calories(self):
        return self.average_calories

    def get_location(self):
        return self.location

    def get_location_code(self):
        return self.location_code

    def get_description(self):
        return self.description

    def get_food_items(self):
        return self.food_items

    def get_rating(self):
        return self.rating

    def get_image_location(self):
        return self.image_location


a00001 = Food("a00001", "Chicken Rice", 673)
a00002 = Food("a00002", "Fried Rice", 840)
a00003 = Food("a00003", "Aglio Olio", 600)
a00004 = Food("a00004", "Cesear Salad", 540)
b00001 = Food("b00001", "McSpicy", 752)
b00002 = Food("b00002", "Straight-Up Blood", 109)
b00003 = Food("b00003", "Teriyaki Bento", 631)
b00004 = Food("b00004", "Karage Ramen", 570)

food_list = [a00001, a00002, a00003, a00004, b00001, b00002, b00003, b00004]

sen01 = Vendor("sen01", "McDonald's", 1207, "1 Sengkang Square #01-225, Sengkang - 545078", "sen", "This stuff will literally kill you and you pay us for it.", [a00001, a00002], "static/images/mcdonalds-sengkang-image.jpg")
sen02 = Vendor("sen02", "Misaka - Sengkang Kopitiam", 979, "1 Sengkang Sq Compass Pt #03-210, Sengkang - 545078", "sen", "Come buy overpriced frozen food!", [a00003, a00004], "static/images/misaka-sengkang-image.jpeg")
amk01 = Vendor("amk01", "The Lawn", 798, "26 Ang Mo Kio Industrial Park 2 #01-00, AMK - 569507", "amk", "The ambience is nice but no more than that", [b00001, b00002], "static/images/thelawn-amk-image.jpeg")
amk02 = Vendor("amk02", "Lean Bento", 699, "53 Ang Mo Kio Ave 3 AMK Hub #01-34, AMK - 569933", "amk", "The food is decently healthy but still way too sweet", [b00003, b00004], "static/images/leanbento-amk-image.jpeg")

sen01.set_rating(1)
sen02.set_rating(3)
amk01.set_rating(3)
amk02.set_rating(4)

vendor_list = [sen01, sen02, amk01, amk02]
