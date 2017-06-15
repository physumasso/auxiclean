import unittest
import tempfile
import os
from unittest.mock import patch
from auxiclean import Selector
from collections import OrderedDict


class TestBase(unittest.TestCase):
    # Cours (nom),Cours (code),Dispo,Programme
    courses = {}
    # Nom,Premier Choix,Deuxieme Choix,Troisieme Choix,Quatrieme Choix,
    # Cinquieme Choix,Disponibilite,Tp_total,Schoplarite,Nobel,
    # Programme d'etude,Cote Z
    candidates = {}

    def setUp(self):
        # use temporary file to do the tests
        self.tempdir = tempfile.TemporaryDirectory()
        self.courses_path = os.path.join(self.tempdir.name, "cours.csv")
        self.candidates_path = os.path.join(self.tempdir.name, "students.csv")
        with open(self.courses_path, "w") as f:
            # write cours
            f.write("First line skipped\n")
            for c, v in self.courses.items():
                s = ",".join([c] + v) + "\n"
                f.write(s)
        with open(self.candidates_path, "w") as f:
            # write candidatures
            f.write("First line skipped\n")
            for name, v in self.candidates.items():
                s = ",".join([name] + v) + "\n"
                f.write(s)

    def tearDown(self):
        self.tempdir.cleanup()
        del self.tempdir
        del self.selector


class TestSelector(TestBase):
    # two different courses
    courses = {"Electro": ["1", "1", "1"],
               "Astro": ["10", "1", "1"]}
    # two candidates each applying for a different course. No conflict
    candidates = {"Albert A": ["101", "403", "0", "0", "0", "2",
                               "6", "2", "0", "2", "3"],
                  "Claude C": ["210", "211", "0", "0", "0", "2", "3", "3",
                               "0", "3", "3"]}

    def test_running(self):
        # simple test that checks that both candidates receive
        # their first choice.
        self.selector = Selector(self.candidates_path,
                                 self.courses_path)
        dist = self.selector.distribution
        self.assertEqual(dist["Electro"][0], "Albert A")
        self.assertEqual(dist["Astro"][0], "Claude C")
        # check that there is no other candidates in the distribution
        self.assertEqual(len(dist["Electro"]), 1)
        self.assertEqual(len(dist["Astro"]), 1)


class TestSortingSelector(TestBase):
    # One course with one place
    courses = {"Electro": ["1", "1", "1"]}
    # two candidates apply for the same course but Alice gave it one time
    # So Alice has more experience than Bob, she should win the position.
    candidates = {"Bob": ["001", "0", "0", "0", "0", "1",
                          "0", "1", "0", "2", "3"],
                  "Alice": ["101", "0", "0", "0", "0", "1",
                            "1", "1", "0", "2", "3"]}

    def test_sort_by_specific_tp_experience(self):
        self.selector = Selector(self.candidates_path,
                                 self.courses_path)
        # results
        dist = self.selector.distribution
        self.assertEqual(dist["Electro"][0], "Alice")


class TestMultiplePosition(TestBase):
    # two different courses for one person
    courses = {"Electro": ["1", "1", "1"],
               "Astro": ["10", "1", "1"]}
    # one candidate applying for two different course.
    # if the candidate is the best suited, he gets both choice
    # assuming he has two disponibilities
    candidates = {"Albert A": ["101", "410", "0", "0", "0", "2",
                               "6", "2", "0", "2", "3"]}

    def test_two_class_for_one_person(self):
        self.selector = Selector(self.candidates_path,
                                 self.courses_path)
        # results
        dist = self.selector.distribution
        self.assertEqual(dist["Electro"][0], "Albert A")
        self.assertEqual(dist["Astro"][0], "Albert A")


class TestSecondChoiceIsBetter(TestBase):
    # two different courses for two person
    courses = {"Electro": ["1", "1", "1"],
               "Astro": ["10", "1", "1"]}
    # both candidate have different first choice but one candidate
    # has the other class in his second choice and is better so
    # once his first choice hi passed, he also gets his second choice
    # assuming he has two disponibilities
    candidates = {"Albert A": ["101", "410", "0", "0", "0", "2",
                               "6", "2", "0", "2", "3"],
                  "Claude C": ["210", "211", "0", "0", "0", "2", "3", "3",
                               "0", "3", "3"]}

    def test_second_choice_beat_first_if_better(self):
        self.selector = Selector(self.candidates_path,
                                 self.courses_path)
        # results
        dist = self.selector.distribution
        self.assertEqual(dist["Electro"][0], "Albert A")
        self.assertEqual(dist["Astro"][0], "Albert A")


class TestSecondChoiceIsBetterButNoMoreDispo(TestBase):
    # two different courses for two person
    courses = {"Electro": ["1", "1", "1"],
               "Astro": ["10", "1", "1"]}
    # both candidate have different first choice but one candidate
    # has the other class in his second choice and is better but
    # no more disponibilities so the other students still gets it
    candidates = {"Albert A": ["101", "410", "0", "0", "0", "1",
                               "6", "2", "0", "2", "3"],
                  "Claude C": ["210", "211", "0", "0", "0", "2", "3", "3",
                               "0", "3", "3"]}

    def test_second_choice_beat_first_if_better_and_has_dispo(self):
        self.selector = Selector(self.candidates_path,
                                 self.courses_path)
        # results
        dist = self.selector.distribution
        self.assertEqual(dist["Electro"][0], "Albert A")
        self.assertEqual(dist["Astro"][0], "Claude C")


class TestNoDispo(TestBase):
    # two different courses for two person
    courses = {"Electro": ["1", "1", "1"],
               "Astro": ["10", "1", "1"]}
    # No more dispo for both students so nobody gets chosen
    candidates = {"Albert A": ["101", "410", "0", "0", "0", "0",
                               "6", "2", "0", "2", "3"],
                  "Claude C": ["210", "211", "0", "0", "0", "0", "3", "3",
                               "0", "3", "3"]}

    def test_no_more_dispo(self):
        self.selector = Selector(self.candidates_path,
                                 self.courses_path)
        # results
        dist = self.selector.distribution
        self.assertEqual(dist["Electro"], [])
        self.assertEqual(dist["Astro"], [])


class TestNoSpaceInClass(TestBase):
    # two different courses for two person
    courses = {"Electro": ["1", "0", "1"],
               "Astro": ["10", "0", "1"]}
    # no space in class so nobody gets chosen (for second showing)
    candidates = {"Albert A": ["101", "410", "0", "0", "0", "2",
                               "6", "2", "0", "2", "3"],
                  "Claude C": ["210", "211", "0", "0", "0", "2", "3", "3",
                               "0", "3", "3"]}

    def test_no_more_space(self):
        self.selector = Selector(self.candidates_path,
                                 self.courses_path)
        # results
        dist = self.selector.distribution
        self.assertEqual(dist["Electro"], [])
        self.assertEqual(dist["Astro"], [])


class TestSwitch(TestBase):
    # two different courses for two person
    courses = {"Electro": ["1", "1", "1"],
               "Astro": ["10", "1", "1"]}
    # no space in class so nobody gets chosen (for second showing)
    candidates = {"Albert A": ["101", "410", "0", "0", "0", "2",
                               "2", "2", "2", "2", "2"],
                  "Claude C": ["210", "201", "0", "0", "0", "2", "2", "2",
                               "2", "2", "2"]}

    def test_switch(self):
        self.selector = Selector(self.candidates_path,
                                 self.courses_path)
        # results
        dist = self.selector.distribution
        self.assertEqual(dist["Electro"], ["Claude C"])
        self.assertEqual(dist["Astro"], ["Albert A"])


@patch('auxiclean.user_input.get_user_input')
class TestUserInput(TestBase):
    # one course, two equal candidates
    courses = {"Electro": ["1", "1", "1"], }
    # ordered dict here because for python v < 3.6, dict order is not
    # guaranteed and we want to assign albert A as choice #1
    candidates = OrderedDict({"Albert A": ["101", "110", "0", "0", "0", "2",
                                           "6", "2", "0", "2", "3"],
                              "Bernard B": ["101", "110", "0", "0", "0", "2",
                                            "6", "2", "0", "2", "3"]})

    def test_user_input_simple(self, user_input_mock):
        # test that user input chooses first candidate over second.
        user_input_mock.side_effect = ["1", "oui"]
        self.selector = Selector(self.candidates_path,
                                 self.courses_path)
        dist = self.selector.distribution
        self.assertEqual(dist["Electro"][0], "Albert A")

    def test_user_input_NaN(self, user_input_mock):
        # test that the code still selects the good candidates
        # if user do not enter a number the first time
        user_input_mock.side_effect = ["not a number", "2", "oui"]
        self.selector = Selector(self.candidates_path,
                                 self.courses_path)
        dist = self.selector.distribution
        self.assertEqual(dist["Electro"][0], "Bernard B")

    def test_user_input_less_than_1(self, user_input_mock):
        # test that the code still selects the good candidates
        # if user enters a number less than 1
        user_input_mock.side_effect = ["0", "2", "oui"]
        self.selector = Selector(self.candidates_path,
                                 self.courses_path)
        dist = self.selector.distribution
        self.assertEqual(dist["Electro"][0], "Bernard B")

    def test_user_input_retry(self, user_input_mock):
        # test that the code still selects the good candidates
        # if user enters 'no' at the last step to retry selection
        # (test when user changes its mind)
        user_input_mock.side_effect = ["1", "no", "2", "yes"]
        self.selector = Selector(self.candidates_path,
                                 self.courses_path)
        dist = self.selector.distribution
        self.assertEqual(dist["Electro"][0], "Bernard B")

    def test_user_input_wrong_retry(self, user_input_mock):
        # test that the code still selects the good candidates
        # if user enters neither 'yes' or 'no' at the
        # last step to retry selection
        # (test when user changes its mind but makes a typo)
        user_input_mock.side_effect = ["1", "not yes or no", "N", "2", "y"]
        self.selector = Selector(self.candidates_path,
                                 self.courses_path)
        dist = self.selector.distribution
        self.assertEqual(dist["Electro"][0], "Bernard B")
