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

sen03 = Vendor (
    code = "sen03",
    name = "Real Food",
    average_calories = 768,
    area = "Sengkang",
    location = "1 Sengkang Square #01-225, Sengkang - 545078",
    location_code = 'sen',
    description = 'The obvious correct option.',
    rating = 4,
    image_location = '../static/images/realfood-sengkang-image.jpg'
)

sen04 = Vendor (
    code = "sen04",
    name = "Subway",
    average_calories = 1027,
    area = "Sengkang",
    location = "1 Sengkang Square #01-225, Sengkang - 545078",
    location_code = 'sen',
    description = "Sandwiches & salads made to order, right in front of you, down to your specifications, with the use of a variety of ingredients",
    rating = 3,
    image_location = '../static/images/subway-sengkang-image.jpg'
)

sen05 = Vendor (
    code = "sen05",
    name = '',
    average_calories = 768,
    area = '',
    location = '',
    location_code = '',
    description = '',
    rating = 3,
    image_location = ''
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
    rating = 3,
    image_location = "../static/images/leanbento-amk-image.jpeg"
    )

amk03 = Vendor (
    code = "amk03",
    name =  "The Daily Cut",
    average_calories = 980,
    area = "Ang Mo Kio",
    location = "53 Ang Mo Kio Ave 3 AMK Hub #01-34, AMK - 569933",
    location_code = "amk",
    description = 'Fresh and healthy meat coming right up!',
    rating = 4,
    image_location = '../static/images/dailycut-amk-image.jpeg'
)

amk04 = Vendor (
    code = "amk04",
    name = 'The Warm Drum',
    average_calories = 768,
    area = 'Ang Mo Kio',
    location = '69 Ang Mo Kio Ave 4 #01-34, AMK - 569969',
    location_code = 'amk',
    description = 'High Quality Meat Cuts Available!',
    rating = 2,
    image_location = '../static/images/warmdrum-amk-image.jpeg'
)

amk05 = Vendor (
    code = "amk05",
    name = '',
    average_calories = 768,
    area = '',
    location = '',
    location_code = '',
    description = '',
    rating = 1,
    image_location = ''
)

pun01 = Vendor (
    code = "pun01",
    name = "Grains",
    average_calories = 467,
    area = 'Punggol',
    location = '',
    location_code = 'pun',
    description = '',
    rating = 1,
    image_location = ''
)

pun02 = Vendor (
    code = "pun02",
    name = "The Soup Spoon",
    average_calories = 768,
    area = 'Punggol',
    location = '',
    location_code = 'pun',
    description = '',
    rating = 2,
    image_location = ''
)

pun03 = Vendor (
    code = "pun03",
    name = "VeganBurg",
    average_calories = 768,
    area = 'Punggol',
    location = '',
    location_code = 'pun',
    description = '',
    rating = 3,
    image_location = ''
)

pun04 = Vendor (
    code = "pun04",
    name = '',
    average_calories = 768,
    area = 'Punggol',
    location = '',
    location_code = 'pun',
    description = '',
    rating = 4,
    image_location = ''
)

pun05 = Vendor (
    code = "pun05",
    name = '',
    average_calories = 768,
    area = 'Punggol',
    location = '',
    location_code = 'pun',
    description = '',
    rating = 3,
    image_location = ''
)



a00001 = Food("a00001", "McSpicy", 752, sen01)
a00002 = Food("a00002", "Straight-Up Blood", 109, sen01)
a00003 = Food("a00003", "Soup of Chicken", 200, sen01)
a00004 = Food("a00004", "Just Another Food", 109, sen01)
a00005 = Food("a00005", "Straight-Up Blood", 109, sen01)

a00011 = Food("a00011", "Aglio Olio", 600, sen02)
a00012 = Food("a00012", "Cesear Salad", 540, sen02)
a00013 = Food("a00013", "Cream Pasta", 756, sen02)
a00014 = Food("a00014", "Carbonara", 694, sen02)
a00015 = Food("a00015", "Mushroom", 307, sen02)

a00021 = Food("a00021", "Aglio Olio", 600, sen03)
a00022 = Food("a00022", "Cesear Salad", 540, sen03)
a00023 = Food("a00023", "Cream Pasta", 756, sen03)
a00024 = Food("a00024", "Carbonara", 694, sen03)
a00025 = Food("a00025", "Mushroom", 307, sen03)

a00031 = Food("a00031", "Aglio Olio", 600, sen04)
a00032 = Food("a00032", "Cesear Salad", 540, sen04)
a00033 = Food("a00033", "Cream Pasta", 756, sen04)
a00034 = Food("a00034", "Carbonara", 694, sen04)
a00035 = Food("a00035", "Mushroom", 307, sen04)

a00041 = Food("a00041", "Aglio Olio", 600, sen05)
a00042 = Food("a00042", "Cesear Salad", 540, sen05)
a00043 = Food("a00043", "Cream Pasta", 756, sen05)
a00044 = Food("a00044", "Carbonara", 694, sen05)
a00045 = Food("a00045", "Mushroom", 307, sen05)

b00001 = Food("b00001", "Chicken Rice", 673, amk01)
b00002 = Food("b00002", "Fried Rice", 840, amk01)
b00003 = Food("b00003", "Pineapple Rice", 840, amk01)
b00004 = Food("b00004", "Some kind of rice", 840, amk01)
b00005 = Food("b00005", "Hokkien Style Food", 840, amk01)

b00011 = Food("b00011", "Teriyaki Bento", 631, amk02)
b00012 = Food("b00012", "Karage Ramen", 570, amk02)
b00013 = Food("b00013", "Unagi Bento", 570, amk02)
b00014 = Food("b00014", "Cold Udon", 570, amk02)
b00015 = Food("b00015", "Some kind of Japanese food", 570, amk02)

b00021 = Food("b00021", "Teriyaki Bento", 631, amk03)
b00022 = Food("b00022", "Karage Ramen", 570, amk03)
b00023 = Food("b00023", "Unagi Bento", 570, amk03)
b00024 = Food("b00024", "Cold Udon", 570, amk03)
b00025 = Food("b00025", "Some kind of Japanese food", 570, amk03)

b00031 = Food("b00031", "Teriyaki Bento", 631, amk04)
b00032 = Food("b00032", "Karage Ramen", 570, amk04)
b00033 = Food("b00033", "Unagi Bento", 570, amk04)
b00034 = Food("b00034", "Cold Udon", 570, amk04)
b00035 = Food("b00035", "Some kind of Japanese food", 570, amk04)

b00041 = Food("b00041", "Teriyaki Bento", 631, amk05)
b00042 = Food("b00042", "Karage Ramen", 570, amk05)
b00043 = Food("b00043", "Unagi Bento", 570, amk05)
b00044 = Food("b00044", "Cold Udon", 570, amk05)
b00045 = Food("b00045", "Some kind of Japanese food", 570, amk05)

c00001 = Food("c00001", "Teriyaki Bento", 631, pun01)
c00002 = Food("c00002", "Karage Ramen", 570, pun01)
c00003 = Food("c00003", "Karage Ramen", 570, pun01)
c00004 = Food("c00004", "Karage Ramen", 570, pun01)
c00005 = Food("c00005", "Karage Ramen", 570, pun01)

c00011 = Food("c00011", "Teriyaki Bento", 631, pun02)
c00012 = Food("c00012", "Karage Ramen", 570, pun02)
c00013 = Food("c00013", "Karage Ramen", 570, pun02)
c00014 = Food("c00014", "Karage Ramen", 570, pun02)
c00015 = Food("c00015", "Karage Ramen", 570, pun02)

c00021 = Food("c00021", "Teriyaki Bento", 631, pun03)
c00022 = Food("c00022", "Karage Ramen", 570, pun03)
c00023 = Food("c00023", "Karage Ramen", 570, pun03)
c00024 = Food("c00024", "Karage Ramen", 570, pun03)
c00025 = Food("c00025", "Karage Ramen", 570, pun03)

c00031 = Food("c00031", "Teriyaki Bento", 631, pun04)
c00032 = Food("c00032", "Karage Ramen", 570, pun04)
c00033 = Food("c00033", "Karage Ramen", 570, pun04)
c00034 = Food("c00034", "Karage Ramen", 570, pun04)
c00035 = Food("c00035", "Karage Ramen", 570, pun04)

c00041 = Food("c00041", "Teriyaki Bento", 631, pun05)
c00042 = Food("c00042", "Karage Ramen", 570, pun05)
c00043 = Food("c00043", "Karage Ramen", 570, pun05)
c00044 = Food("c00044", "Karage Ramen", 570, pun05)
c00045 = Food("c00045", "Karage Ramen", 570, pun05)

### Puts the food/vendors in lists accordingly ###

food_list = [a00001, a00002, a00003, a00004, a00005,
             a00011, a00012, a00013, a00014, a00015,
             a00021, a00022, a00023, a00024, a00025,
             a00031, a00032, a00033, a00034, a00035,
             a00041, a00042, a00043, a00044, a00045,

             b00001, b00002, b00003, b00004, b00005,
             b00011, b00012, b00013, b00014, b00015,
             b00021, b00022, b00023, b00024, b00025,
             b00031, b00032, b00033, b00034, b00035,
             b00041, b00042, b00043, b00044, b00045,

             c00001, c00002, c00003, c00004, c00005,
             c00011, c00012, c00013, c00014, c00015,
             c00021, c00022, c00023, c00024, c00025,
             c00031, c00032, c00033, c00034, c00035,
             c00041, c00042, c00043, c00044, c00045]

vendor_list = [sen01, sen02, sen03, sen04, sen05,
               amk01, amk02, amk03, amk04, amk05,
               pun01, pun02, pun03, pun04, pun05]

vendor_food = {sen01: [a00001, a00002, a00003, a00004, a00005],
               sen02: [a00011, a00012, a00013, a00014, a00015],
               sen03: [a00021, a00022, a00023, a00024, a00025],
               sen04: [a00031, a00032, a00033, a00034, a00035],
               sen05: [a00041, a00042, a00043, a00044, a00045],

               amk01: [b00001, b00002, b00003, b00004, b00005],
               amk02: [b00011, b00012, b00013, b00014, b00015],
               amk03: [b00021, b00022, b00023, b00024, b00025],
               amk04: [b00031, b00032, b00033, b00034, b00035],
               amk05: [b00041, b00042, b00043, b00044, b00045],

               pun01: [c00001, c00002, c00003, c00004, c00005],
               pun02: [c00011, c00012, c00013, c00014, c00015],
               pun03: [c00021, c00022, c00023, c00024, c00025],
               pun04: [c00031, c00032, c00033, c00034, c00035],
               pun05: [c00041, c00042, c00043, c00044, c00045]
               }


