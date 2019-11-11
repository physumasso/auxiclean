import unittest

from flake8.api import legacy as flake8


class CodeQualityTest(unittest.TestCase):
    def test_Flake8_conformance(self):
        style_guide = flake8.get_style_guide()
        report = style_guide.check_files()
        msg = "Found code syntax errors (and warnings)!\n"
        nerr = f"Number of errors = {report.total_errors}.\n"
        self.assertEqual(report.total_errors, 0, msg=msg + nerr)
