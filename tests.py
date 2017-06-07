import sys
import nose
import os


modules = ["auxiclean.unittests.test_coding_standards",
           "auxiclean.unittests.test_distributeur.TestDistributeur",
           "auxiclean.unittests.test_distributeur.TestSortingDistributeur"]


def run(tests):
    os.environ["NOSE_WITH_COVERAGE"] = "1"
    os.environ["NOSE_COVER_PACKAGE"] = "auxiclean"
    os.environ["NOSE_COVER_HTML"] = "1"
    os.environ["NOSE_COVER_ERASE"] = "1"
    nose.main(defaultTest=tests)

if __name__ == "__main__":
    run(modules)
