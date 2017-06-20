# priority attributes in order of most important to least important
# DO NOT CHANGE THIS LIST AS IT WAS DECIDED BY A COMITEE
PRIORITIES = ("course_given",
              "total_courses_given",
              "scolarity",
              "nobels",
              "same_discipline",
              "gpa")


class Candidate:
    def __init__(self, name,
                 disponibilities, courses_given,
                 scolarity, nobels, discipline, gpa, *choices):
        self.name = name
        self.choices = list(choices)
        self.disponibilities = int(disponibilities)
        self.courses_given = courses_given
        self.scolarity = int(scolarity)
        self.nobels = int(nobels)
        self.discipline = discipline
        self.gpa = float(gpa)

    def __repr__(self):  # pragma: no cover
        return self.name


class CourseCandidate:
    def __init__(self, candidate, course):
        self.name = candidate.name
        self.course_given = self._get_course_given(candidate.courses_given,
                                                   course.code)
        self.total_courses_given = len(candidate.courses_given)
        self.scolarity = candidate.scolarity
        self.nobels = candidate.nobels
        self.same_discipline = self._discipline_matches(candidate.discipline,
                                                        course.discipline)
        self.gpa = candidate.gpa

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
        for attribute in PRIORITIES:
            attr1 = getattr(self, attribute)
            attr2 = getattr(candidate2, attribute)
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
        for attribute in PRIORITIES:
            attr1 = getattr(self, attribute)
            attr2 = getattr(candidate2, attribute)
            if attr1 != attr2:
                return False
        return True

    def __repr__(self):
        return self.name
