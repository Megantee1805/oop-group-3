### Creates the classes ###

class Vendor:
    def __init__(self, code, name, average_calories, area, location, location_code, description, rating, image_location):
        self.code = code
        self.name = name
        self.average_calories = average_calories
        self.area = area
        self.location = location
        self.location_code = location_code
        self.description = description
        self.rating = rating
        self.image_location = image_location

    def set_code(self, code):
        self.code = code

    def set_name(self, name):
        self.name = name

    def set_average_calories(self, average_calories):
        self.average_calories = average_calories

    def set_area(self, area):
        self.area = area

    def set_location(self, location):
        self.location = location

    def set_location_code(self, location_code):
        self.location_code = location_code

    def set_description(self, description):
        self.description = description

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

    def get_area(self):
        return self.area

    def get_location(self):
        return self.location

    def get_location_code(self):
        return self.location_code

    def get_description(self):
        return self.description

    def get_rating(self):
        return self.rating

    def get_image_location(self):
        return self.image_location


class Food:
    def __init__(self, code, name, calories, vendor):
        self.code = code
        self.name = name
        self.calories = calories
        self.vendor = vendor

    def set_code(self, code):
        self.code = code

    def set_name(self, name):
        self.name = name

    def set_calories(self, calories):
        self.calories = calories

    def set_vendor(self, vendor):
        self.vendor = vendor

    def get_code(self):
        return self.code

    def get_name(self):
        return self.name

    def get_calories(self):
        return self.calories

    def get_vendor(self):
        return self.vendor


class Questions:
    def __init__(self, question):
        self.__question = question
        self.__list_of_queries = []

    def set_questions(self, question):
        self.__question = question

    def get_question(self):
        return self.__question

    def add_question(self, question):
        self.__list_of_queries.append(question)

    def get_list(self):
        return self.__list_of_queries


### Assigns the objects to vendor and food classes accordingly ###

sen01 = Vendor(
    code = "sen01",
    name = "McDonald's",
    average_calories = 1207,
    area = "Sengkang",
    location = "1 Sengkang Square #01-225, Sengkang - 545078",
    location_code = "sen",
    description = "This stuff will literally kill you and you pay us for it.",
    rating = 1,
    image_location = "../static/images/mcdonalds-sengkang-image.jpg"
    )

sen02 = Vendor(
    code = "sen02",
    name = "Misaka - Sengkang Kopitiam",
    average_calories = 979,
    area = "Sengkang",
    location = "1 Sengkang Square #01-225, Sengkang - 545078",
    location_code = "sen",
    description = "Come buy overpriced frozen food!",
    rating = 3,
    image_location = "../static/images/misaka-sengkang-image.jpeg"
    )

amk01 = Vendor(
    code = "amk01",
    name = "The Lawn",
    average_calories = 798,
    area = "Ang Mo Kio",
    location = "26 Ang Mo Kio Industrial Park 2 #01-00, AMK - 569507",
    location_code = "amk",
    description = "The ambience is nice but no more than that.",
    rating = 2,
    image_location = "../static/images/thelawn-amk-image.jpeg"
    )

amk02 = Vendor(
    code = "amk02",
    name = "Lean Bento",
    average_calories = 699,
    area = "Ang Mo Kio",
    location = "53 Ang Mo Kio Ave 3 AMK Hub #01-34, AMK - 569933",
    location_code = "amk",
    description = "The food is decently healthy but still way too sweet",
    rating = 4,
    image_location = "../static/images/leanbento-amk-image.jpeg"
    )

a00001 = Food("a00001", "McSpicy", 752, sen01)
a00002 = Food("a00002", "Straight-Up Blood", 109, sen01)

a00003 = Food("a00003", "Aglio Olio", 600, sen02)
a00004 = Food("a00004", "Cesear Salad", 540, sen02)

b00001 = Food("b00001", "Chicken Rice", 673, amk01)
b00002 = Food("b00002", "Fried Rice", 840, amk01)

b00003 = Food("b00003", "Teriyaki Bento", 631, amk02)
b00004 = Food("b00004", "Karage Ramen", 570, amk02)


### Puts the food/vendors in lists accordingly ###

food_list = [a00001, a00002, a00003, a00004, b00001, b00002, b00003, b00004]
vendor_list = [sen01, sen02, amk01, amk02]
vendor_food = {sen01: [a00001, a00002], sen02: [a00003, a00004], amk01: [b00001, b00002], amk02: [b00003, b00004]}


