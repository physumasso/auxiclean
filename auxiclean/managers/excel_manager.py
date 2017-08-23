from openpyxl import load_workbook
from .sheet_managers import (CoursesSheetManager, CandidatesSheetManager,
                             DistributionSheetManager, ExcelError)


class ExcelFileManager:
    def __init__(self, path):
        self.path = path
        self.wb = load_workbook(path)
        self._courses = CoursesSheetManager(self.wb)
        self._candidates = CandidatesSheetManager(self.wb)
        self._checkup()
        self._distribution = None

    @property
    def courses(self):
        return self._courses.courses

    @property
    def candidates(self):
        return self._candidates.candidates

    def write_distribution(self, distribution):
        if self._distribution is None:
            self._distribution = DistributionSheetManager(self.wb)
        self._distribution.write_distribution(distribution)
        self.save()

    def save(self):
        self.wb.save(self.path)

    def _checkup(self):
        all_courses_disciplines = []
        all_candidates_disciplines = []
        # check that all candidates choices exists in the courses list
        for candidate in self.candidates:
            if candidate.discipline not in all_candidates_disciplines:
                all_candidates_disciplines.append(candidate.discipline.lower())
            for choice in candidate.choices:
                if not self._choice_in_courses(choice):
                    raise ExcelError("Le choix %s de %s n'est pas dans la"
                                     " liste de cours." %
                                     (choice, candidate.name))

        # check for duplicate candidates
        for j, candidate in enumerate(self.candidates):
            for candidate2 in self.candidates[j + 1:]:
                if candidate.name == candidate2.name:
                    raise ExcelError("Candidature %s dupliquée." %
                                     candidate.name)

        # check for duplicate courses
        for j, course in enumerate(self.courses):
            if course.discipline not in all_courses_disciplines:
                all_courses_disciplines.append(course.discipline.lower())
            for course2 in self.courses[j + 1:]:
                if course.code == course2.code:
                    raise ExcelError("Cours %s dupliqué." % course.code)

        # check for disciplines
        for candidate in self.candidates:
            d = candidate.discipline.lower()
            if d is None or d.lower() == "générale":
                continue
            if d not in all_courses_disciplines:
                raise ExcelError("La discipline '%s' de %s n'est pas dans"
                                 " la liste de toutes les"
                                 " disciplines des cours." %
                                 (d, candidate.name))
        for course in self.courses:
            d = course.discipline.lower()
            if d is None or d.lower() == "générale":
                continue
            if d not in all_candidates_disciplines:
                raise ExcelError("La discipline '%s' du cours %s n'es pas dans"
                                 " la liste de toutes les disciplines des"
                                 " candidatures." % (d, course.code))

    def _choice_in_courses(self, choice):
        for course in self.courses:
            if course.code == choice:
                return True
        return False
