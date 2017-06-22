import nose
import os


common = "auxiclean.unittests."

mods = {"test_coding_standards": ["", ],
        "test_selector.": ["TestSelector",
                           "TestSortingSelector",
                           "TestMultiplePosition",
                           "TestSecondChoiceIsBetter",
                           "TestSecondChoiceIsBetterButNoMoreDispo",
                           "TestNoDispo",
                           "TestNoSpaceInClass",
                           "TestUserInput",
                           "TestSwitch",
                           "TestCourseGiven",
                           "TestScholarity",
                           "TestNobel",
                           "TestProgram",
                           "TestGPA", ],
        "test_excel_manager.": ["TestExcelManager",
                                "TestExcelCandidateChoiceError", ],
        "test_course.": ["TestCourseRaise",
                         "TestCourseNoName",
                         "TestCourseNoDiscipline", ],
        "test_candidate.": ["TestCandidateNoGPA", ],
        }

modules = []
for test_module, test_list in mods.items():
    for test_class in test_list:
        modules.append(common + test_module + test_class)


def run(tests):
    os.environ["NOSE_WITH_COVERAGE"] = "1"
    os.environ["NOSE_COVER_PACKAGE"] = "auxiclean"
    os.environ["NOSE_COVER_HTML"] = "1"
    os.environ["NOSE_COVER_ERASE"] = "1"
    os.environ["NOSE_COVER_TESTS"] = "1"
    nose.main(defaultTest=tests)


if __name__ == "__main__":
    run(modules)
