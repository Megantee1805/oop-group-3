def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


### Creates the classes ###


class Vendor:
    def __init__(self, code, name, average_calories, area, location, location_code, description, rating, image_location):
        self.__code = code
        self.__name = name
        self.__average_calories = average_calories
        self.__area = area
        self.__location = location
        self.__location_code = location_code
        self.__description = description
        self.__rating = rating
        self.__image_location = image_location

    def set_code(self, code):
        self.__code = code
    def set_name(self, name):
        self.__name = name
    def set_average_calories(self, average_calories):
        self.__average_calories = average_calories
    def set_area(self, area):
        self.__area = area
    def set_location(self, location):
        self.__location = location
    def set_location_code(self, location_code):
        self.__location_code = location_code
    def set_description(self, description):
        self.__description = description
    def set_rating(self, rating):
        self.__rating = rating
    def set_image_location(self, image_location):
        self.__image_location = image_location

    def get_code(self):
        return self.__code
    def get_name(self):
        return self.__name
    def get_average_calories(self):
        return self.__average_calories
    def get_area(self):
        return self.__area
    def get_location(self):
        return self.__location
    def get_location_code(self):
        return self.__location_code
    def get_description(self):
        return self.__description
    def get_rating(self):
        return self.__rating
    def get_image_location(self):
        return self.__image_location


class Food:
    def __init__(self, code, name, calories, vendor):
        self.__code = code
        self.__name = name
        self.__calories = calories
        self.__vendor = vendor

    def set_code(self, code):
        self.__code = code
    def set_name(self, name):
        self.__name = name
    def set_calories(self, calories):
        self.__calories = calories
    def set_vendor(self, vendor):
        self.__vendor = vendor

    def get_code(self):
        return self.__code
    def get_name(self):
        return self.__name
    def get_calories(self):
        return self.__calories
    def get_vendor(self):
        return self.__vendor


class Questions:
    def __init__(self, question):
        self.__question = question
        self.__list_of_queries = []

    def set_questions(self, question):
        self.__question = question

    def get_question(self):
        return self.__question
    def get_list(self):
        return self.__list_of_queries

    def add_question(self, question):
        self.__list_of_queries.append(question)


class ProcessUserInfo:
    def __init__(self, food_items, users):
        self.food_items = food_items
        self.__food_exists = 0
        self.__all_dates = []
        self.__food_dates = []
        self.__calories_list = []
        self.__user_average_calories = 0
        self.__number_of_days = 0

        self.users = users
        self.__id = ''
        self.__name = ''
        self.__weight = 0
        self.__height = 0
        self.__bmi = 0
        self.__email = ''
        self.__user_location = ''
        self.__password = ''
        self.__user_vendors = []
        self.__breakfast_list = []
        self.__lunch_list = []
        self.__dinner_list = []
        self.__snack_list = []
        self.__average_breakfast_calories = 0
        self.__average_lunch_calories = 0
        self.__average_dinner_calories = 0
        self.__average_snack_calories = 0
        self.__bmi_statement = ''
        self.__calories_statement = 'You have not added enough food to your journal to generate a summary. Keep adding more food!'
        self.__snack_message = ''

    def get_info(self):
        for user in self.users:
            self.__id = user['id']
            self.__name = user['name']
            self.__weight = user['weight']
            self.__height = user['height']
            self.__email = user['email']
            self.__user_location = user['location']
            self.__password = user['password']
            self.__bmi = round(self.__weight / self.__height ** self.__height, 2)

        for vendor in vendor_list:
            vendor = vendor_list[vendor]
            if self.__user_location == vendor.get_area():
                self.__user_vendors.append(vendor)

        if self.food_items != []:
            self.__food_exists = 1

            for food in self.food_items:
                food_date = food['created'].strftime('%d-%m-%y')
                self.__all_dates.append(food_date)
            self.__all_dates = remove_duplicates(self.__all_dates)

            for date in self.__all_dates:
                current_date_food = []
                current_date_calories = []

                for food in self.food_items:
                    if date == food['created'].strftime('%d-%m-%y'):
                        current_date_food.append(food)
                        current_date_calories.append(food['calories'])

                current_date_calories = sum(current_date_calories)

                self.__calories_list.append(current_date_calories)
                self.__number_of_days = len(self.__calories_list)
                self.__user_average_calories = int(sum(self.__calories_list) / self.__number_of_days)
                self.__food_dates.append(current_date_food)

        for food in self.food_items:
            if 5 <= int(food['created'].strftime('%H')) <= 9:
                self.__breakfast_list.append(food['calories'])
                self.__average_breakfast_calories = round(sum(self.__breakfast_list) / self.__number_of_days, 2)
            elif 11 <= int(food['created'].strftime('%H')) <= 14:
                self.__lunch_list.append(food['calories'])
                self.__average_lunch_calories = round(sum(self.__lunch_list) / self.__number_of_days, 2)
            elif 17 <= int(food['created'].strftime('%H')) <= 21:
                self.__dinner_list.append(food['calories'])
                self.__average_dinner_calories = round(sum(self.__dinner_list) / self.__number_of_days, 2)
            else:
                self.__snack_list.append(food['calories'])
                self.__average_snack_calories = round(sum(self.__snack_list) / self.__number_of_days, 2)

        ideal_weight = self.__weight

        if self.__bmi < 22:
            while ideal_weight / self.__height ** self.__height < 23:
                ideal_weight = ideal_weight + 1
            lose_weight = ideal_weight - self.__weight
            self.__bmi_statement = "{0}, you have a BMI of {1}, which is below the healthy range of 22 to 24. You are recommended " \
                                 "to gain {2} kg to reach a body mass of {3} kg, which will get you back to the healthy BMI range." \
                .format(self.__name, self.__bmi, lose_weight, ideal_weight)
        elif 22 < self.__bmi < 24:
            self.__bmi_statement = "{0}, you have a BMI of {1}, which is exactly within the healthy BMI range. " \
                                 "Keep it up!".format(self.__name, self.__bmi)

        elif self.__bmi > 24:
            while ideal_weight / self.__height ** self.__height > 23:
                ideal_weight = ideal_weight - 1
            lose_weight = self.__weight - ideal_weight
            self.__bmi_statement = "{0}, you have a BMI of {1}, which is above the healthy range of 22 to 24. You are recommended " \
                                 "to lose {2} kg to reach a body mass of {3} kg, which will get you back to the healthy BMI range." \
                .format(self.__name, self.__bmi, lose_weight, ideal_weight)

        if self.__user_average_calories:
            if self.__user_average_calories < 1500:
                self.__calories_statement = "You consumed an average of {0} kcal daily over the last {1} days you've entered food " \
                                          "into your food journal, which is below the daily recommended amount of 2500 kcal." \
                    .format(self.__user_average_calories, self.__number_of_days)
            elif 1500 <= self.__user_average_calories <= 2500:
                self.__calories_statement = "You consumed an average of {0} kcal daily over the {1} days you've entered food " \
                                          "into your food journal, which is within the daily recommended amount, so keep following your current diet." \
                    .format(self.__user_average_calories, self.__number_of_days)

            elif self.__user_average_calories > 2500:
                self.__calories_statement = "You consumed an average of {} kcal daily over the last {} days you've entered food " \
                                          "which is above the daily recommended amount of 2500 kcal." \
                    .format(self.__user_average_calories, self.__number_of_days)

        if self.__average_snack_calories:
            if self.__average_snack_calories > 300:
                self.__snack_message = "Also, you need to decrease your out-of-schedule snack intake."

        info = {
            "id": self.__id,
            "name": self.__name,
            "weight": self.__weight,
            "height": self.__height,
            "bmi": self.__bmi,
            "email": self.__email,
            "user_location": self.__user_location,
            "password": self.__password,
            "user_vendors": self.__user_vendors,

            "food_items": self.food_items,
            "food_exists": self.__food_exists,
            "all_dates": self.__all_dates,
            "calories_list": self.__calories_list,
            "number_of_days": self.__number_of_days,
            "user_average_calories": self.__user_average_calories,
            "food_dates": self.__food_dates,

            "bmi_statement": self.__bmi_statement,
            "calories_statement": self.__calories_statement,
            "breakfast_list": self.__breakfast_list,
            "lunch_list": self.__lunch_list,
            "dinner_list": self.__dinner_list,
            "snack_list": self.__snack_list,
            "average_breakfast_calories": self.__average_breakfast_calories,
            "average_lunch_calories": self.__average_lunch_calories,
            "average_dinner_calories": self.__average_dinner_calories,
            "average_snack_calories": self.__average_snack_calories,
            "snack_message": self.__snack_message,
        }

        return info


class SupportData:
    def __init__(self, food_items):
        self.food_items = food_items
        self.__food_list = food_list
        self.__food_dict = {}
        self.__food_code = ''

    def add_food(self, food_code:str):
        count = 0
        for key in self.__food_dict:
            if self.__food_code == key:
                count = count + 1
                self.__food_dict[key] = count
        self.__food_code = food_code
        count = count + 1
        self.__food_dict[food_code] = count


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
    description = 'The blatantly correct choice.',
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

pun01 = Vendor (
    code = "pun01",
    name = "Grains",
    average_calories = 467,
    area = 'Punggol',
    location = '11 Northshore Drive, Punggol - 828670',
    location_code = 'pun',
    description = 'Ensuring that better food, prepared from whole, unprocessed ingredients is accessible to everyone.',
    rating = 4,
    image_location = '../static/images/grains-punggol-image.jpg'
    )

pun02 = Vendor (
    code = "pun02",
    name = "The Soup Spoon",
    average_calories = 892,
    area = 'Punggol',
    location = '9 Sentul Cres, #05-01 SAFRA Punggol Club, Punggol - 828654',
    location_code = 'pun',
    description = 'We provide a one-of-a-kind experience that energizes everyone with an enthusiastic welcome, exceptional service, awesome food, killer tunes, and an unforgettable time.',
    rating = 2,
    image_location = '../static/images/soupspoon-punggol-image.jpg'
    )

pun03 = Vendor (
    code = "pun03",
    name = "VeganBurg",
    average_calories = 768,
    area = 'Punggol',
    location = '6 Tebing Lane, #01-03, Punggol East, Punggol - 828835',
    location_code = 'pun',
    description = ' Our goal is to provide incredible taste at a modest price point in a welcoming, stylish atmosphere.',
    rating = 3,
    image_location = '../static/images/veganburg-punggol-image.jpg'
    )

pun04 = Vendor (
    code = "pun04",
    name = 'Izakaya 95',
    average_calories = 768,
    area = 'Punggol',
    location = '3 Punggol Point #02-05 The Punggol Settlement, Punggol - 828694',
    location_code = 'pun',
    description = "Here at The Punggol Settlement's Izakaya 95, traditional items like grilled tori negi, Kagoshima buta, hotate and engiri king mushroom are just some of the tastes you can savour.",
    rating = 4,
    image_location = '../static/images/izakaya95-punggol-image.jpg'
    )


a00001 = Food("a00001", "McSpicy", 752, sen01)
a00002 = Food("a00002", "McSalad", 209, sen01)
a00003 = Food("a00003", "4pc McWings", 300, sen01)
a00004 = Food("a00004", "Big Mac", 954, sen01)
a00005 = Food("a00005", "McChicken", 456, sen01)

a00011 = Food("a00011", "Aglio Olio", 600, sen02)
a00012 = Food("a00012", "Cesear Salad", 540, sen02)
a00013 = Food("a00013", "Cream of Mushroom Soup", 256, sen02)
a00014 = Food("a00014", "Carbonara", 694, sen02)
a00015 = Food("a00015", "Mushroom Pasta", 407, sen02)

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


### Puts the food/vendors in lists accordingly ###


food_list = [a00001, a00002, a00003, a00004, a00005,
             a00011, a00012, a00013, a00014, a00015,
             a00021, a00022, a00023, a00024, a00025,
             a00031, a00032, a00033, a00034, a00035,

             b00001, b00002, b00003, b00004, b00005,
             b00011, b00012, b00013, b00014, b00015,
             b00021, b00022, b00023, b00024, b00025,
             b00031, b00032, b00033, b00034, b00035,

             c00001, c00002, c00003, c00004, c00005,
             c00011, c00012, c00013, c00014, c00015,
             c00021, c00022, c00023, c00024, c00025,
             c00031, c00032, c00033, c00034, c00035,]


vendor_list = {'sen01': sen01, 'sen02': sen02, 'sen03': sen03, 'sen04': sen04,
               'amk01': amk01, 'amk02': amk02, 'amk03': amk03, 'amk04': amk04,
               'pun01': pun01, 'pun02': pun02, 'pun03': pun03, 'pun04': pun04}

# vendor_list = {'sen01': {sen01: [a00001, a00002, a00003, a00004, a00005]},
#                'sen02': {sen02: [a00011, a00012, a00013, a00014, a00015]},
#                'sen03': {sen03: [a00021, a00022, a00023, a00024, a00025]},
#                'sen04': {sen04: [a00031, a00032, a00033, a00034, a00035]},
#
#                'amk01': {amk01: [a00031, a00032, a00033, a00034, a00035]},
#                'amk02': {amk02: [b00011, b00012, b00013, b00014, b00015]},
#                'amk03': {amk03: [b00021, b00022, b00023, b00024, b00025]},
#                'amk04': {amk04: [b00031, b00032, b00033, b00034, b00035]},
#
#                'pun01': {pun01: [c00001, c00002, c00003, c00004, c00005]},
#                'pun02': {pun02: [c00011, c00012, c00013, c00014, c00015]},
#                'pun03': {pun03: [c00021, c00022, c00023, c00024, c00025]},
#                'pun04': {pun04: [c00031, c00032, c00033, c00034, c00035]}}

vendor_food = {sen01: [a00001, a00002, a00003, a00004, a00005],
               sen02: [a00011, a00012, a00013, a00014, a00015],
               sen03: [a00021, a00022, a00023, a00024, a00025],
               sen04: [a00031, a00032, a00033, a00034, a00035],

               amk01: [b00001, b00002, b00003, b00004, b00005],
               amk02: [b00011, b00012, b00013, b00014, b00015],
               amk03: [b00021, b00022, b00023, b00024, b00025],
               amk04: [b00031, b00032, b00033, b00034, b00035],

               pun01: [c00001, c00002, c00003, c00004, c00005],
               pun02: [c00011, c00012, c00013, c00014, c00015],
               pun03: [c00021, c00022, c00023, c00024, c00025],
               pun04: [c00031, c00032, c00033, c00034, c00035],}
