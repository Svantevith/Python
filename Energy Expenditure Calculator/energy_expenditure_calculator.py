import re
from datetime import date


class Person:
    def __init__(self):
        self.__sex = 'Gender'
        self.__age = 0
        self.__weight = 0
        self.__height = 0
        self.__activity = 0
        self.__BMR = 0
        self.__TDEE = 0

    @property
    def sex(self):
        return self.__sex

    @sex.setter
    def sex(self, sex):
        self.__sex = sex

    @property
    def sex_desc(self):
        return 'Your gender is {}'.format(self.sex)

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        self.__age = age

    @property
    def age_desc(self):
        return 'You are {} years young, remember that number does not define your age! 😉'.format(self.age)

    @property
    def activity(self):
        return self.__activity

    @activity.setter
    def activity(self, activity):
        self.__activity = activity

    @property
    def activity_desc(self):
        return 'Your activity level multiplier is {}'.format(self.activity)

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, weight):
        self.__weight = weight

    @property
    def weight_desc(self):
        return 'Your weight is {} kg'.format(self.weight)

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        self.__height = height

    @property
    def height_desc(self):
        return 'Your height is {} cm 📏'.format(self.height)

    @property
    def BMR(self):
        if self.sex == 'Female ♀️':
            self.BMR = round(655 + (9.6 * self.__weight) + (1.8 * self.__height) + (4.7 * self.__age), 2)
        elif self.sex == 'Male ♂️‍':
            self.BMR = round(66 + (13.7 * self.__weight) + (5 * self.__height) - (6.8 * self.__age), 2)
        return self.__BMR

    @BMR.setter
    def BMR(self, BMR):
        self.__BMR = BMR

    @property
    def BMR_desc(self):
        return 'Your Basic Metabolic Rate is {} 🍔'.format(round(self.BMR, 2))

    @property
    def TDEE(self):
        self.TDEE = round(self.__activity * self.__BMR, 2)
        return self.__TDEE

    @TDEE.setter
    def TDEE(self, TDEE):
        self.__TDEE = TDEE

    @property
    def TDEE_desc(self):
        return 'Total Daily Energy Expenditure is calculated by multiplying your Basic Metabolic Rate = {}' \
               ' by the activity level = {} 🍕 .\n' \
               'You need to consume {} kcal each day just to maintain your current weight.' \
            .format(round(self.BMR, 2), self.activity, round(self.TDEE, 2))

    @property
    def surplus(self):
        return (
            round((lambda energy: energy + 200)(self.TDEE), 2),
            round((lambda energy: energy + 300)(self.TDEE), 2)
        )

    @property
    def deficit(self):
        return round((lambda energy: 0.2 * energy)(self.TDEE), 2)

    @property
    def protein_gForFatLoss(self):
        return (round((lambda weight: 1.8 * weight)(self.weight)),
                (round((lambda weight: 2.2 * weight)(self.weight))))

    @property
    def fat_gForFatLoss(self):
        return (
            round((lambda energy: 0.15 * energy / 9)(self.TDEE - self.deficit)),
            round((lambda energy: 0.3 * energy / 9)(self.TDEE - self.deficit))
        )

    @property
    def carbohydrates_gForFatLoss(self):
        return (
            round((lambda proteins, fats, energy: (energy - (proteins * 4) - (fats * 9)) / 4)
                  (self.protein_gForFatLoss[0], self.fat_gForFatLoss[1], self.TDEE - self.deficit)),
            round((lambda proteins, fats, energy: (energy - (proteins * 4) - (fats * 9)) / 4)
                  (self.protein_gForFatLoss[1], self.fat_gForFatLoss[0], self.TDEE - self.deficit))
        )

    @property
    def protein_gForMuscleGain(self):
        return 1.6

    @property
    def fat_gForMuscleGain(self):
        return (
            round((lambda energy: 0.15 * energy / 9)(self.surplus[0])),
            round((lambda energy: 0.3 * energy / 9)(self.surplus[0]))
        )

    @property
    def carbohydrates_gForMuscleGain(self):
        return (
            round((lambda proteins, fats, energy: (energy - (proteins * 4) - (fats * 9)) / 4)
                  (self.protein_gForMuscleGain, self.fat_gForMuscleGain[1], self.surplus[0])),
            round((lambda proteins, fats, energy: (energy - (proteins * 4) - (fats * 9)) / 4)
                  (self.protein_gForMuscleGain, self.fat_gForMuscleGain[0], self.surplus[1]))
        )


# Here the minor functions are defined. They are parts of the major functions that are below.
#
#
#
def inputValidation(user_input):
    while True:
        if user_input.isdigit() and int(user_input) in (1, 2):
            return int(user_input)
        else:
            print('Your enter should be an integer: either 1 or 2')


def calculateAge(date_of_birth):
    today = date.today()
    try:
        birthday = date_of_birth.replace(year=today.year)
    # raised when birth date is February 29
    # and the current year is not a leap year
    except ValueError:
        birthday = date_of_birth.replace(year=today.year, month=date_of_birth.month + 1, day=1)
    if birthday > today:
        return today.year - date_of_birth.year - 1
    else:
        return today.year - date_of_birth.year


def isYearLeap(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    else:
        return False


def isMonth31or30(month, months, start, end):
    while True:
        day = input('Day: ')
        if day.isdigit() and start <= int(day) <= end:
            return int(day)
        else:
            print('In {} there are only positive numbers of days, up to {}'.format(months[month], end))


def getFebruary(year, month, months):
    while True:
        day = input('Day: ')
        if day.isdigit() and isYearLeap(year) and 1 <= int(day) <= 29:
            return int(day)
        else:
            print('{} is a leap year. '
                  'In {} there are only positive numbers of days, up to {}'.format(year, months[month], 29))
        if day.isdigit() and not isYearLeap(year) and 1 <= int(day) <= 28:
            return int(day)
        else:
            print('{} is not a leap year. '
                  'In {} there are only positive numbers of days, up to {}'.format(year, months[month], 28))


def getAge():
    while True:
        age = input('Please enter your age:\n')
        if age.isdigit() and 1 <= int(age) <= 150:
            return int(age)
        else:
            print('Your age should be an integer in the range from 1 to 150.')


def getYear():
    while True:
        year = input('Year: ')
        if year.isdigit() and date.today().year - 150 <= int(year) <= date.today().year:
            return int(year)
        else:
            print('Year should be given within range {} and {}'.
                  format(date.today().year - 150, date.today().year))


def getMonth():
    while True:
        month = input('Month: ')
        if month.isdigit() and 1 <= int(month) <= 12:
            return int(month)
        else:
            print('Month should be given within range 1 and 12')


def getDay(year, month):
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July',
              8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    if month in (1, 3, 5, 7, 8, 10, 12):
        return isMonth31or30(month, months, 1, 31)

    if month in (4, 6, 9, 11):
        return isMonth31or30(month, months, 1, 30)

    if month == 2:
        return getFebruary(year, month, months)


def weightValidation(weight):
    return 0.1 <= weight <= 400


def convertLbsToKg(lbs):
    return round((lambda x: x * 0.4535923)(lbs), 2)


def getWeightLbs():
    try:
        while True:
            weight_lbs = round(float(input('[lbs] = ')), 2)
            weight = convertLbsToKg(weight_lbs)
            if weightValidation(weight):
                print('Your weight given is {} lbs'.format(weight_lbs))
                return weight
            else:
                print('Your weight should have been given in the range between {} and {} lbs, '
                      'or passed'.format(round(convertLbsToKg(0.1), 2), round(convertLbsToKg(400), 2)))
    except ValueError:
        pass


def getWeight():
    try:
        weight = round(float(input('[kg] = ')), 2)
        if weightValidation(weight):
            return weight
    except ValueError:
        pass


def getHeight_M():
    user_input = str(input("[m] = ")).replace(' ', '')
    matcher_m = re.match(r'^(\d)((\.)(\d+))?$', user_input)
    if matcher_m:
        height_m = round(float(user_input), 2)
        print("Your given height is {} m".format(height_m))
        height = convert_MtoCm(height_m)
        if heightValidation(height):
            return height


def getHeight_US():
    user_input = str(input("[ft'in] = ")).replace(' ', '')
    matcher_us = re.match(r'^(\d)((\')(\d+))?$', user_input)
    if matcher_us:
        feet = int(matcher_us.group(1))
        inch = int(matcher_us.group(4))
        if inch is None:
            inch = 0
        print("You have given the height in the US format: {}'{}".format(feet, round(inch, 2)))
        height = convertHeight_UStoEU(feet, inch)
        if heightValidation(height):
            return height


def heightValidation(height):
    return 15 <= height <= 300


def getHeight():
    try:
        height = float(input('[cm] = '))
        if heightValidation(height):
            return height
    except ValueError:
        print('Enter another weight format.')


def convertHeight_UStoEU(feet, inch):
    if len(str(inch)) >= 2:
        # the max decimal length is 2 (regex)
        inch = float(inch) / 10 ** len(str(inch))
    return round((lambda ft, in_: 30.48 * float(ft) + 2.54 * float(in_))(feet, inch), 2)


def convert_MtoCm(meter):
    return (lambda x: x * 100)(meter)


def activity_table(**kwargs):
    return kwargs


#
#
#
# Here the major functions are defined

def userDefinedSex():
    while True:
        user_input = str(input('Please enter your gender: \n(F)emale\n(M)ale\n')).replace(' ', '')
        if user_input.lower() == 'f':
            return 'Female'
        elif user_input.lower() == 'm':
            return 'Male'
        else:
            print("You've entered incorrect gender 💑")


def userDefinedActivity():
    activities = activity_table(
        a=('Sedentary (little or no exercise)', 1.2),
        b=('Light exercise/sports 1-3 days/week', 1.375),
        c=('Moderately active (moderate exercise/sports 3-5 days/week', 1.55),
        d=('Very active (hard exercise/sports 6-7 days a week)', 1.725),
        e=('Extra active (very hard exercise/sports & a physical job', 1.9)
    )

    for key, value in activities.items():
        print(key, ' - ', value[0])

    activity = 0

    while not [True for key, value in activities.items() if activity == value[1]]:
        activity = input('Enter your activity level throughout a casual day: \n')
        if activity in activities.keys():
            activity_multiplier = activities[activity][1]
            return activity_multiplier
        else:
            print('Your activity level should be a letter in the range from {} to {}'.
                  format(list(activities)[0], list(activities)[len(activities) - 1]))


def userDefinedAge():
    print('Do you know your age?\n1) Yes\n2) No')
    user_input = input('Enter 1 or 2 to proceed further.\n')
    age = 0
    if inputValidation(user_input) == 1:
        print("Your answer is 'Yes'")
        age = getAge()
    elif inputValidation(user_input) == 2:
        print("Your answer is 'No'.\nEnter your date of birth")
        year = getYear()
        month = getMonth()
        day = getDay(year, month)
        age = calculateAge(date(year, month, day))
    return age


def userDefinedWeight():
    print('Please enter your weight either in pounds or kilograms.')
    while True:
        weight_lbs = getWeightLbs()
        if weight_lbs is not None:
            return weight_lbs
        weight = getWeight()
        if weight is not None:
            return weight
        else:
            print('Your weight should have been given in the range between {} and {} lbs, '
                  'or in the range from 0.1 to 400 kg'.format(round(convertLbsToKg(0.1), 2),
                                                              round(convertLbsToKg(400), 2)))


def userDefinedHeight():
    print("Please enter your height in [cm], [m] or [feet'inches]:")
    while True:
        height_m = getHeight_M()
        if height_m is not None:
            return height_m
        height_us = getHeight_US()
        if height_us is not None:
            return height_us
        height = getHeight()
        if height is not None:
            return height
        else:
            print("Your height should be a number in the range from 15 to 300 cm, "
                  "it may be also expressed in the range from 0.15 to 3.0 m or ft'in 0'59 to 9'99 .")


def dailyEnergyExpenditure(person):
    person.sex = userDefinedSex()
    print(person.sex_desc)

    person.age = userDefinedAge()
    print(person.age_desc)

    person.weight = userDefinedWeight()
    print(person.weight_desc)

    person.height = userDefinedHeight()
    print(person.height_desc)

    person.activity = userDefinedActivity()
    print(person.activity_desc)

    print(person.BMR_desc)
    print(person.TDEE_desc)


def forFatLoss(person):
    print('Daily calorie intake for weight loss: {} - {} = {} kcal daily 🥝'.
          format(person.TDEE, person.deficit, round(person.TDEE - person.deficit, 2)))
    print('By maintaining a {} daily kcal deficit, you would lose a little over {} kg per week, '
          'because 1kg of fat equals approximately 7700 kcal.'
          .format(person.deficit, round((7700 / (person.deficit * 7)), 2)))
    print('Now that we have the daily energy intake needed for fat loss,'
          '\nProtein: 1.6 gram per kg of bodyweight'
          '\nFat: 15 – 30% of TDEE'
          '\nCarbohydrates: The number of kcal remaining')
    print('Recommended Protein intake: 1.8g * {} = {} g (Kcal = {} g x 4 kcal / g of protein = {} kcal)'
          .format(person.weight, person.protein_gForFatLoss[0],
                  person.protein_gForFatLoss[0], person.protein_gForFatLoss[0] * 4))
    print('High Protein intake: 1.8g * {} = {} g (Kcal = {} g x 4 kcal / g of protein = {} kcal)'
          .format(person.weight, person.protein_gForFatLoss[1],
                  person.protein_gForFatLoss[1], person.protein_gForFatLoss[1] * 4))
    print('Note: Fat can range from 15-30% of your Total Dietary Energy Expenditure. '
          'Decrease of increase the fat intake based on your own dietary preferences.')
    print('Low Fat intake: 0.15 * {} / 9 = {} g (Calories = {} g x 9 kcal / g of fat = {} kcal)'
          .format(person.TDEE, person.fat_gForFatLoss[0], person.fat_gForFatLoss[0], person.fat_gForFatLoss[0] * 9))
    print('High Fat intake: 0.3 * {} / 9 = {} g (Calories = {} g x 9 kcal / g of fat = {})'
          .format(person.TDEE, person.fat_gForFatLoss[1], person.fat_gForFatLoss[1], person.fat_gForFatLoss[1] * 9))
    print('Low Carb intake: {} - {} - {} / 4 = {} g (Calories = {} g x 4 kcal / g of carbs = {} kcal)'
          .format(person.TDEE, round(((person.protein_gForFatLoss[1] - person.protein_gForFatLoss[0]) / 2)) * 4,
                  person.fat_gForFatLoss[1] * 9,
                  person.carbohydrates_gForFatLoss[0], person.carbohydrates_gForFatLoss[0],
                  person.carbohydrates_gForFatLoss[0] * 4))
    print('High Carb intake: {} - {} - {} / 4 = {} g (Calories = {} g x 4 kcal / g of carbs = {} kcal)'
          .format(person.TDEE, round(((person.protein_gForFatLoss[1] - person.protein_gForFatLoss[0]) / 2)) * 4,
                  person.fat_gForFatLoss[0] * 9,
                  person.carbohydrates_gForFatLoss[1], person.carbohydrates_gForFatLoss[1],
                  person.carbohydrates_gForFatLoss[1] * 4))
    print('Therefore, you may follow this nutrient profile '
          'in order to lose fat while preserving lean muscle mass:'
          '\nProtein: {} - {} g'
          '\nFats: {} - {} g'
          '\nCarbohydrates: {} - {} g'.format(person.protein_gForFatLoss[0], person.protein_gForFatLoss[1],
                                              person.fat_gForFatLoss[0], person.fat_gForFatLoss[1],
                                              person.carbohydrates_gForFatLoss[0], person.carbohydrates_gForFatLoss[1]))
    print("Remember that these calculations are just estimates. The highest accuracy will offer you"
          "a constant observation of your body: it's composition, weight and appearance changes.")


def forMuscleGain(person):
    print('Daily calorie intake for weight gain: {} + {} = {} - {} kcal daily 🍌'
          .format(person.TDEE, '(200 up to 300)', person.surplus[0], person.surplus[1]))
    print('Therefore, you may follow this nutrient profile '
          'in order to lose fat while preserving lean muscle mass:'
          '\nProtein: at least {} g'
          '\nFats: {} - {} g'
          '\nCarbohydrates: {} - {} g'.format(person.protein_gForMuscleGain, person.fat_gForMuscleGain[0],
                                              person.fat_gForMuscleGain[1],
                                              person.carbohydrates_gForMuscleGain[0],
                                              person.carbohydrates_gForMuscleGain[1]))
    print("Remember that these calculations are just estimates. The highest accuracy will offer you"
          "a constant observation of your body: it's composition, weight and appearance changes.")


def userNutritionalGoal(person):
    print('Choose what is your current goal:\n1) Lose weight\n2) Gain more weight\n3) Exit')
    while True:
        user_input = input('Enter a number corresponding to wanted action: ')
        if user_input.isdigit():
            choice = int(user_input)
            if choice == 1:
                forFatLoss(person)
                break
            elif choice == 2:
                forMuscleGain(person)
                break


def __main__():
    person = Person()
    dailyEnergyExpenditure(person)
    userNutritionalGoal(person)


__main__()
