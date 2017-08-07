from .test_selector import TestBase
from auxiclean import Selector
from unittest.mock import patch


@patch('auxiclean.user_input.get_user_input')
class TestCandidateNoGPA(TestBase):
    # two different courses
    courses = {"Electro": {"code": "1441",
                           "disponibilities": 1,
                           "discipline": "générale"}}
    # two candidates each applying for a different course.
    # they are equals. so we must choose 1
    candidates = {"Albert A": {"maximum": 2,
                               "scolarity": 2,
                               "courses given": [],
                               "nobels": 0,
                               "discipline": "générale",
                               "choices": ["1441", ],
                               "gpa": ""},  # no gpa
                  "Claude C": {"maximum": 2,
                               "scolarity": 2,
                               "courses given": [],
                               "nobels": 0,
                               "discipline": "générale",
                               "choices": ["1441", ],
                               "gpa": ""}, }  # no gpa

    def test_no_gpa(self, user_input):
        # test that gpa is not considered if it
        # is not given
        user_input.side_effect = ["1", "oui"]
        self.selector = Selector(self.data_path, loglevel=self.loglevel)
