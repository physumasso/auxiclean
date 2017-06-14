from .candidate import Candidate
from .course import Course
import auxiclean.user_input as user_input


class Selector:
    def __init__(self, candidates_path, courses_path):

        candidates_list = self._get_candidates(candidates_path)
        courses_list = self._get_courses(courses_path)
        self.distribution = self.make_distribution(courses_list,
                                                   candidates_list)
        self.print_distribution()

    def _get_candidates(self, path):
        candidates = []
        print("\n#####  CANDIDATURES  #####")
        with open(path) as students_data:
            lines = students_data.readlines()
            for line in lines[1:]:
                s = Candidate(*line.split(','))
                print(s.name, s.choices)
                candidates.append(s)
        return candidates

    def _get_courses(self, path):
        courses = []
        print("\n#####  COURS A COMBLER  #####")
        with open(path) as class_data:
            lines = class_data.readlines()
            for line in lines[1:]:
                c = Course(*line.split(","))
                print(c.name, c.code)
                courses.append(c)
        return courses

    def input_choices(self, list_equalities, nchoices, course):
        while True:
            print("Des égalités sont présentes pour le cours %s." % course)
            print("Il faut choisir %i candidat(e)s parmis:" % nchoices)
            for i, c in enumerate(list_equalities):
                print("%i: %s" % (i + 1, c))
            choices_left = nchoices
            choices = []
            while choices_left:
                good_ans = False
                while not good_ans:
                    ans = user_input.get_user_input("Choix #%i:" %
                                                    (len(choices) + 1))
                    try:
                        choix = int(ans) - 1
                    except ValueError:
                        print("SVP, veuillez entrer un nombre entier.")
                        continue
                    else:
                        if choix < 0:
                            print("SVP, veuillez entrer un nombre > 0.")
                            continue
                    good_ans = True
                    choices.append(list_equalities[choix])
                    choices_left -= 1
            print("Vous avez choisis:")
            for c in choices:
                print(c)
            good_ans = False
            while not good_ans:
                yes = user_input.get_user_input("Est-ce OK? [Oui/Non]:")
                yes = yes.lower()
                if yes not in ("oui", "o", "y", "yes",
                               "non", "n", "no"):
                    print("Veuillez entrer oui ou non SVP")
                    continue
                else:
                    good_ans = True
                    if yes in ("oui", "o", "y", "yes"):
                        return choices
                    # if No is entered here, the main loop will restart.

    def choose_candidates(self, number_of_positions, candidates_list, course):
        if not number_of_positions:
            # no candidate to choose.
            return []
        temp_list = candidates_list[-number_of_positions:]
        eq_list = []
        if temp_list[0] == candidates_list[:-number_of_positions][-1]:
            # possible equalities, we need to choose them manually
            # first, find_equalities that might change the outcome
            for c in candidates_list:
                if c == temp_list[0]:
                    eq_list.append(c)
            # now find the number of these equal candidates inside provisoire
            same = [x for x in temp_list if x == temp_list[0]]
            n = len(same)
            for s in same:
                temp_list.remove(s)
            # n is the number of candidates to choose in liste_eq
            choices = self.input_choices(eq_list, n, course)
            return choices + temp_list
        return temp_list

    def sort(self, number_of_positions, candidates_list, course):
        # sort the list of candidates in ordre of worst to best
        candidates_list = sorted(candidates_list)
        # choosed candidates
        candidates_chosen = self.choose_candidates(number_of_positions,
                                                   candidates_list,
                                                   course)
        return candidates_chosen

    def make_distribution(self, courses_list, candidates_list):
        change = False
        while not change:
            change = False
            for course in courses_list:
                for candidate in candidates_list:
                    if candidate.choices[0][1:] == course.code:
                        if candidate.disponibilities:
                            change = True
                            course.candidates.append(candidate)
                            # remove choice from student choices
                            candidate.choices.pop(0)

                # if number of candidates is greater than number of positions,
                # we need to sort them out
                if len(course.candidates) > course.positions:
                    candidates_chosen = self.sort(course.positions,
                                                  course.candidates,
                                                  course.name)
                    course.candidates = candidates_chosen
                # for each chosen candidates, remove one from their dispos
                for candidate in course.candidates:
                    candidate.disponibilities -= 1
            if not change:
                break
        distribution = {}
        for course in courses_list:
            distribution[course.name] = [c.name for c in course.candidates]
        return distribution

    def print_distribution(self):
        print("\n#####  DISTRIBUTION  #####")
        for course, candidates_list in self.distribution.items():
            print("%s : %s" % (course, str(candidates_list)))
