import unittest
import tempfile
import os
from auxiclean import Distributeur


class TestBase(unittest.TestCase):
    # Cours (nom),Cours (code),Dispo,Programme
    cours = {}
    # Nom,Premier Choix,Deuxieme Choix,Troisieme Choix,Quatrieme Choix,
    # Cinquieme Choix,Disponibilite,Tp_total,Schoplarite,Nobel,
    # Programme d'etude,Cote Z
    candidatures = {}

    def setUp(self):
        # use temporary file to do the tests
        self.tempdir = tempfile.TemporaryDirectory()
        self.cours_path = os.path.join(self.tempdir.name, "cours.csv")
        self.stud_path = os.path.join(self.tempdir.name, "students.csv")
        with open(self.cours_path, "w") as f:
            # write cours
            f.write("First line skipped\n")
            for c, v in self.cours.items():
                s = ",".join([c] + v) + "\n"
                f.write(s)
        with open(self.stud_path, "w") as f:
            # write candidatures
            f.write("First line skipped\n")
            for name, v in self.candidatures.items():
                s = ",".join([name] + v) + "\n"
                f.write(s)
        self.distributeur = Distributeur(self.stud_path,
                                         self.cours_path)

    def tearDown(self):
        self.tempdir.cleanup()
        del self.tempdir
        del self.distributeur


class TestDistributeur(TestBase):
    cours = {"Electro": ["1", "1", "1"],
             "Astro": ["10", "1", "1"]}
    candidatures = {"Albert A": ["101", "403", "0", "0", "0", "2",
                                 "6", "2", "0", "2", "3"],
                    "Claude C": ["210", "211", "0", "0", "0", "2", "3", "3",
                                 "0", "3", "3"]}

    def test_running(self):
        # simple test that checks that both candidates receive
        # their first choice.
        dist = self.distributeur.distribution
        self.assertEqual(dist["Electro"][0], "Albert A")
        self.assertEqual(dist["Astro"][0], "Claude C")
