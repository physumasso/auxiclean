from openpyxl import load_workbook
from .sheet_managers import (CoursesSheetManager, CandidatesSheetManager,
                             DistributionSheetManager)


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
        for candidate in self.candidates:
            for choice in candidate.choices:
                if not self._choice_in_courses(choice):
                    raise ValueError(" Choice %s of %s not in courses list." %
                                     (choice, candidate))

    def _choice_in_courses(self, choice):
        for course in self.courses:
            if course.code == choice:
                return True
        return False
