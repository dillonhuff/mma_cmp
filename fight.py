class Date:
    def __init__(self, month, day, year):
        self.month = month
        self.day = day
        self.year = year

    def month_num(self):
        return month_to_num(self.month)

    def to_string(self):
        return self.month + '-' + str(self.day) + '-' + str(self.year)

class Fighter:
    def __init__(self, name, date_of_birth):
        self.name = name
        self.date_of_birth = date_of_birth

class Fight:
    def __init__(self, f0, f1, result, cause, date):
        self.f0 = f0
        self.f1 = f1
        self.result = result
        self.cause = cause
        self.date = date

