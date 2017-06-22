from .test_selector import TestBase
from auxiclean import Selector


class TestCourseRaise(TestBase):
    courses = {"Electro": {"code": "",  # no code
                           "disponibilities": 1,
                           "discipline": "générale"}}
    candidates = {"Albert A": {"maximum": 2,
                               "scolarity": 2,
                               "courses given": ["1441", "2710", "2710",
                                                 "2710", "2710", "1620"],
                               "nobels": 0,
                               "discipline": "générale",
                               "choices": ["1441", ],
                               "gpa": 2.6}}

    def test_no_code(self):
        with self.assertRaises(ValueError):
            self.selector = Selector(self.data_path)


class TestCourseNoName(TestBase):
    courses = {"": {"code": "1441",  # no name
                    "disponibilities": 1,
                    "discipline": "générale"}}
    candidates = {"Albert A": {"maximum": 2,
                               "scolarity": 2,
                               "courses given": ["1441", "2710", "2710",
                                                 "2710", "2710", "1620"],
                               "nobels": 0,
                               "discipline": "générale",
                               "choices": ["1441", ],
                               "gpa": 2.6}}

    def test_no_name(self):
        self.selector = Selector(self.data_path)
        course = self.selector.excel_mgr.courses[0]
        self.assertEqual(course.name, course.code)


class TestCourseNoDiscipline(TestBase):
    courses = {"Electro": {"code": "1441",
                           "disponibilities": 1,
                           "discipline": ""}}  # no discipline
    candidates = {"Albert A": {"maximum": 2,
                               "scolarity": 2,
                               "courses given": ["1441", "2710", "2710",
                                                 "2710", "2710", "1620"],
                               "nobels": 0,
                               "discipline": "générale",
                               "choices": ["1441", ],
                               "gpa": 2.6}}

    def test_no_discipline(self):
        self.selector = Selector(self.data_path)
        course = self.selector.excel_mgr.courses[0]
        self.assertEqual(course.discipline, "générale")
