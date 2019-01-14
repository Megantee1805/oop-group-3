class Stats:
    def __init__(self):
        self.__height = 0
        self.__weight = 0
        self.__Bmi = 0

    def enter_details(self, height:float, weight:int):
        self.__height = height
        self.__weight = weight
        self.__Bmi = weight / (height * height)
        print(self.__Bmi)

user = Stats()
user.enter_details(1.64, 60)
