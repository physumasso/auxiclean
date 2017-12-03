class Candidate:
    def __init__(self, name,
                 disponibilities, courses_given,
                 scolarity, nobels, discipline, gpa, *choices):
        self.name = name.strip()
        self.choices = [c.strip() for c in list(choices)]
        self.disponibilities = int(disponibilities)
        self.courses_given = [c.strip() for c in courses_given]
        self.courses_eligible = []  # list of course the candidate is eligible
        self.scolarity = int(scolarity)
        self.nobels = int(nobels) if nobels is not None else 0
        self.discipline = (discipline.lower().strip() if discipline is not None
                           else "générale")
        self.gpa = float(gpa) if gpa is not None else None

    @property
    def next_choice(self):
        # gives the next choice of the candidate for a given
        # eligible courses list
        lce = len(self.courses_eligible)
        if lce >= self.disponibilities or lce >= len(self.choices):
            # already have filled all dispos or used all choices
            return None
        return self.choices[lce]

    @property
    def still_eligible(self):
        still_choices = len(self.choices)
        still_dispo = self.disponibilities > len(self.courses_eligible)
        return still_choices and still_dispo

    def remove_course(self, course):
        """Remove a course from the choices."""
        if course.code not in self.choices:
            raise ValueError("%s not in choices." % course)
        self.choices.remove(course.code)

    def __repr__(self):  # pragma: no cover
        return str(self)

    def __str__(self):
        s = ("%s: max=%i, choix=%s, scol=%i, donnés=%s,"
             " nobels=%i, gpa=%s, eligible=%s" %
             (self.name, self.disponibilities, str(self.choices),
              self.scolarity, str(self.courses_given), self.nobels,
              str(self.gpa), str(self.courses_eligible)))
        return s


class CourseCandidate:
    def __init__(self, candidate, course, priorities):
        """Class that is used to compare multiple candidates for a course.

        Parameters
        ----------
        candidate : the candidate object
        course : course object
        priorities : list, tuple
                     A list of strings which is the priority order to compare
                     two candidates.
        """
        self.name = candidate.name
        self.course_given = self._get_course_given(candidate.courses_given,
                                                   course.code)
        self.total_courses_given = len(candidate.courses_given)
        self.scolarity = candidate.scolarity
        self.nobels = candidate.nobels
        self.same_discipline = self._discipline_matches(candidate.discipline,
                                                        course.discipline)
        self.gpa = candidate.gpa
        self._priorities = priorities

    def _discipline_matches(self, candidate_discipline, course_discipline):
        if course_discipline.lower() in ("générale", "generale", "general"):
            # if it is a general course, discipline will always be the same
            return True
        return candidate_discipline == course_discipline

    def _get_course_given(self, list_course_given, code):
        # count number of time code is in the list
        count = 0
        for course in list_course_given:
            if course == code:
                count += 1
        return count

    def __lt__(self, candidate2):
        for attribute in self._priorities:
            attr1 = getattr(self, attribute)
            attr2 = getattr(candidate2, attribute)
            if attr1 is None or attr2 is None:
                # don't compare if something is missing
                continue
            if attr1 < attr2:
                # lesser
                return True
            if attr1 > attr2:
                # greater
                return False
            # if we are here, attributes are equal, continue in the priorities
        # if we are here, candidates are perfectly equals
        return False

    def __eq__(self, candidate2):
        for attribute in self._priorities:
            attr1 = getattr(self, attribute)
            attr2 = getattr(candidate2, attribute)
            if attr1 != attr2:
                return False
        return True

    def __repr__(self):
        return self.name
