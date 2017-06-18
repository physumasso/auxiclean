from openpyxl import load_workbook
from .sheet_managers import (CoursesSheetManager, CandidatesSheetManager,
                             DistributionSheetManager)


class ExcelFileManager:
    def __init__(self, path):
        self.path = path
        self.wb = load_workbook(path)
        self._courses = None
        self._candidates = None
        self._distribution = None

    @property
    def courses(self):
        if self._courses is None:
            self._courses = CoursesSheetManager(self.wb)
        return self._courses.courses

    @property
    def candidates(self):
        if self._candidates is None:
            self._candidates = CandidatesSheetManager(self.wb)
        return self._candidates.candidates

    def write_distribution(self, distribution):
        if self._distribution is None:
            self._distribution = DistributionSheetManager(self.wb)
        self._distribution.write_distribution(distribution)
        self.save()

    def save(self):
        self.wb.save(self.path)
