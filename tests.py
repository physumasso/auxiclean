import sys
import nose
import os


modules = ["auxiclean.unittests.test_coding_standards",
           "auxiclean.unittests.test_selector.TestSelector",
           "auxiclean.unittests.test_selector.TestSortingSelector",
           "auxiclean.unittests.test_selector.TestMultiplePosition",
           "auxiclean.unittests.test_selector.TestSecondChoiceIsBetter",
           "auxiclean.unittests.test_selector.TestSecondChoiceIsBetterButNoMoreDispo",
           "auxiclean.unittests.test_selector.TestNoDispo",
           "auxiclean.unittests.test_selector.TestNoSpaceInClass",
           "auxiclean.unittests.test_selector.TestUserInput"]


def run(tests):
    os.environ["NOSE_WITH_COVERAGE"] = "1"
    os.environ["NOSE_COVER_PACKAGE"] = "auxiclean"
    os.environ["NOSE_COVER_HTML"] = "1"
    os.environ["NOSE_COVER_ERASE"] = "1"
    os.environ["NOSE_COVER_TESTS"] = "1"
    nose.main(defaultTest=tests)

if __name__ == "__main__":
    run(modules)
