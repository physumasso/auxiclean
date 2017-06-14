class Candidate:
    def __init__(self, name, choice1, choice2, choice3, choice4, choice5,
                 disponibilities, courses_given,
                 scolarity, nobels, program, gpa):
        self.name = name
        self.choices = [choice1, choice2, choice3, choice4, choice5]
        self.disponibilities = int(disponibilities)
        self.courses_given = int(courses_given)
        self.scolarity = int(scolarity)
        self.nobels = int(nobels)
        self.program = program
        self.gpa = float(gpa)

    def __repr__(self):
        return self.name

    def __lt__(self, candidate2):
        # first criterion: the number of this tp given
        if int(self.choices[0][0]) < int(candidate2.choices[0][0]):
            return True
        # second criterion: the number of tp given
        if self.courses_given < candidate2.courses_given:
            return True
        # third criterion: scolarity
        if self.scolarity < candidate2.scolarity:
            return True
        # fourth criterion: number of nobel prize won
        if self.nobels < candidate2.nobels:
            return True
        # fifth criterion: is the same prog as the course?
        if self.program < candidate2.program:
            return True
        # sixth criterion: gpa
        if self.gpa < candidate2.gpa:
            return True
        return False

    def __eq__(self, candidate2):
        if int(self.choices[0][0]) != int(candidate2.choices[0][0]):
            return False
        if self.courses_given != candidate2.courses_given:
            return False
        if self.scolarity != candidate2.scolarity:
            return False
        if self.nobels != candidate2.nobels:
            return False
        if self.program != candidate2.program:
            return False
        if self.gpa != candidate2.gpa:
            return False
        return True
