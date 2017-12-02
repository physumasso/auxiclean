from .managers import ExcelFileManager, DEFAULT_PARAMETERS
import auxiclean.user_input as user_input
import logging


DEFAULT_PRIORITIES = DEFAULT_PARAMETERS["priorities"]


class Selector:
    def __init__(self, path, master=None,
                 priorities=DEFAULT_PRIORITIES,
                 loglevel=logging.INFO):
        """Class that makes a selection of candidates for some courses
        given a list of priorities. Candidates and courses list are read
        from a file.

        Parameters
        ----------
        path : str
               The excel file.
        master : If in a GUI, this would be the master window for this object.
        priorities : list, tuple
                     The list of priorities to compare two candidates (gives
                     the comparison order).
        loglevel : int, optional
                   Gives the level of the logging.
        """
        self.logger = logging.getLogger("auxiclean.selector")
        self.logger.setLevel(loglevel)
        self.master = master  # if in a GUI
        # load courses and candidates from excel file
        self.excel_mgr = ExcelFileManager(path)
        self.courses = self.excel_mgr.courses
        self.candidates = self.excel_mgr.candidates
        # print courses and candidates
        self.print_courses(self.courses)
        self.print_candidates(self.candidates)
        # make distribution
        self._priorities = priorities
        self.distribution = self.make_distribution(self.courses,
                                                   self.candidates,
                                                   self._priorities)
        # print distribution
        self.print_distribution(self.distribution)
        # write distribution into same excel file
        self.excel_mgr.write_distribution(self.distribution)

    def print_candidates(self, candidates_list):
        self.logger.info("\n#####  CANDIDATURES  #####")
        for candidate in candidates_list:
            self.logger.info(str(candidate))

    def print_courses(self, courses_list):
        self.logger.info("\n#####  COURS A COMBLER  #####")
        for course in courses_list:
            self.logger.info(str(course))

    def print_distribution(self, distribution):
        self.logger.info("\n#####  DISTRIBUTION  #####")
        for course, candidates_list in distribution.items():
            self.logger.info("%s : %s" % (course, str(candidates_list)))

    def choose_candidates(self, number_of_positions, candidates_list, course):
        self.logger.debug("Choosing %i candidates from %s." %
                          (number_of_positions, str(candidates_list)))
        if not number_of_positions:
            # no candidate to choose.
            return [], []
        temp_list = candidates_list[-number_of_positions:]
        eq_list = []
        if temp_list[0] == candidates_list[:-number_of_positions][-1]:
            self.logger.debug("Two or more candidates are equals.")
            # possible equalities, we need to choose them manually
            # first, find_equalities that might change the outcome
            for c in candidates_list:
                if c == temp_list[0]:
                    eq_list.append(c)

            # now find the number of these equal candidates inside templist
            same = [x for x in temp_list if x == temp_list[0]]
            n = len(same)
            self.logger.debug("need to choose %s candidates." % n)
            for s in same:
                temp_list.remove(s)
            # n is the number of candidates to choose in liste_eq
            choices = user_input.input_choices(eq_list, n, course,
                                               master=self.master,
                                               loglevel=self.logger.level)
            if len(choices) != n:
                # something went wrong, raise error.
                raise ValueError("We were expecting %i choices but"
                                 " received %i instead..." % (n, len(choices)))
            temp_list = choices + temp_list
        dismissed = self.get_dismissed(candidates_list, temp_list)
        self.logger.debug("Candidates chosen: %s" % str(temp_list))
        self.logger.debug("Dismissed candidates: %s" % str(dismissed))
        return temp_list, dismissed

    def get_dismissed(self, full_list, end_list):
        """Return the list of dismissed candidates.

        This method is implemented since equal candidates are only distinct by
        their name which is not considered by the logic operators.
        """
        # full_list = all the initial candidates (some of them are equals)
        # end_list = chosen candidates
        end_names = [c.name for c in end_list]
        return [c for c in full_list if c.name not in end_names]

    def sort(self, number_of_positions, candidates_list, course_name):
        """Sort a list of eligible candidates for a specific course in order
        of worst candidate to best candidate according to a given list of
        priorities.
        """
        # sort the list of candidates in ordre of worst to best
        self.logger.debug("Sorting candidates for course %s: %s" %
                          (course_name, str(candidates_list)))
        candidates_list = sorted(candidates_list)
        self.logger.debug("Sorted candidates (ascending): %s" %
                          str(candidates_list))
        # choosed candidates
        (candidates_chosen,
         dismissed) = self.choose_candidates(number_of_positions,
                                             candidates_list,
                                             course_name)
        return candidates_chosen, dismissed

    def make_distribution(self, courses_list, candidates_list, priorities):
        """Makes the distribution from a list of candidates and a list
        of courses. The distribution is based on the priorities list which
        gives the order of parameters to compare 2 candidates.
        """
        self.logger.debug("\n#####  MAKING DISTRIBUTION  #####")
        change = True
        i = 0
        while change:
            # loop until no changes is done to the distribution.
            self.logger.debug("--Iter %i: %s" %
                              (i, str({c.code: c.candidates
                                       for c in courses_list})))
            change = False
            for course in courses_list:
                # loop over all courses.
                self.logger.debug("Treating course %s" % str(course))
                if not course.positions:
                    # empty course, go to the next one
                    self.logger.debug("Course has no positions left.")
                    continue
                for candidate in candidates_list:
                    # loop over all candidates
                    c = candidate
                    self.logger.debug("Treating candidate %s" % c)
                    if not c.still_eligible or c.next_choice != course.code:
                        # if candidates has no more choices or dispos, skip
                        self.logger.debug("Candidate not eligible"
                                          " for this course.")
                        continue
                    # this candidate is elgible for the course.
                    # there will be a change in the distribution.
                    change = True
                    course.add_candidate(c, priorities)
                    self.logger.debug("Candidate eligible.")

                # if number of candidates is greater than number of positions,
                # we need to sort them out
                if len(course.candidates) > course.positions:
                    self.logger.debug("More candidates than positions.")
                    candidates_chosen, dismissed = self.sort(course.positions,
                                                             course.candidates,
                                                             course.name)
                    self.update_dismissed_choices(dismissed, course)
                    course.candidates = candidates_chosen
                self.logger.debug("Course candidates at the end of candidates"
                                  " iteration: %s" % str(course.candidates))
                # for each chosen candidates, update the eligible courses
                self.update_eligible_courses(course, candidates_list)
            if not change:
                break
        # left main loop => distribution stable => write distribution
        distribution = {}
        for course in courses_list:
            distribution[course.code] = course.candidates
        self.logger.debug("Distribution done.")
        return distribution

    def update_eligible_courses(self, course, candidates_list):
        """update eligible courses attributes of candidates with
        selected course"""
        # here, the full list of candidates is given because we provide a deep
        # copy of the candidate to the course
        chosen_names = [c.name for c in course.candidates]
        for candidate in candidates_list:
            eli = candidate.courses_eligible
            if candidate.name in chosen_names and course not in eli:
                # newly chosen candidate
                eli.append(course)
                continue
            if candidate.name not in chosen_names and course in eli:
                # candidate was bumped out
                eli.remove(course)
                continue

    def update_dismissed_choices(self, dismissed, course):
        # after a sorting has been done, we need to pop out the course
        # in the choices of the dismissed candidates
        for c in dismissed:
            # here, candidate is a CourseCandidate object.
            realCandidate = self._find_candidate_from_coursecandidate(c)
            realCandidate.remove_course(course)

    def _find_candidate_from_coursecandidate(self, candidate):
        for c in self.candidates:
            if c.name == candidate.name:
                return c
