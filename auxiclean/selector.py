from .candidate import CourseCandidate
from .managers import ExcelFileManager
import auxiclean.user_input as user_input
import copy
import logging


class Selector:
    def __init__(self, path, master=None):
        self.logger = logging.getLogger("auxiclean.selector")
        self.logger.setLevel(logging.INFO)
        self.master = master  # if in a GUI
        # load courses and candidates from excel file
        self.excel_mgr = ExcelFileManager(path)
        courses = self.excel_mgr.courses
        candidates = self.excel_mgr.candidates
        # print courses and candidates
        self.print_courses(courses)
        self.print_candidates(candidates)
        # make distribution
        self.distribution = self.make_distribution(courses, candidates)
        # print distribution
        self.print_distribution(self.distribution)
        # write distribution into same excel file
        self.excel_mgr.write_distribution(self.distribution)

    def print_candidates(self, candidates_list):
        self.logger.info("\n#####  CANDIDATURES  #####")
        for candidate in candidates_list:
            self.logger.info("%s - %s" % (candidate.name, candidate.choices))

    def print_courses(self, courses_list):
        self.logger.info("\n#####  COURS A COMBLER  #####")
        for course in courses_list:
            self.logger.info("%s - %s" % (course.name, course.code))

    def print_distribution(self, distribution):
        self.logger.info("\n#####  DISTRIBUTION  #####")
        for course, candidates_list in distribution.items():
            self.logger.info("%s : %s" % (course, str(candidates_list)))

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
            choices = user_input.input_choices(eq_list, n, course,
                                               master=self.master)
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
        change = True
        while change:
            change = False
            for course in courses_list:
                for candidate in candidates_list:
                    if not len(candidate.choices):
                        # if candidates has no more choices, skip
                        continue
                    c = candidate
                    if c.choices[0] == course.code and c.disponibilities > 0:
                        change = True
                        # Deep copy of the candidate to compare
                        # with future candidates
                        cp = copy.deepcopy(candidate)
                        stored_candidate = CourseCandidate(cp, course)
                        course.candidates.append(stored_candidate)
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
                for chosen_candidate in course.candidates:
                    for candidate in candidates_list:
                        if candidate.name == chosen_candidate.name:
                            candidate.disponibilities -= 1
            if not change:
                break
        distribution = {}
        for course in courses_list:
            distribution[course.code] = course.candidates
        return distribution
