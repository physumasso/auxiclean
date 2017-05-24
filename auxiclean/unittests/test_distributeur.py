import unittest
import tempfile
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
        self.liste_cours = tempfile.NamedTemporaryFile(mode="a")
        self.liste_candidatures = tempfile.NamedTemporaryFile(mode="a")
        # write cours
        self.liste_cours.write("First line skipped\n")
        for c, v in self.cours.items():
            s = ",".join([c] + v) + "\n"
            self.liste_cours.write(s)
        self.liste_cours.seek(0)  # return at beginning of file to read
        # write candidatures
        self.liste_candidatures.write("First line skipped\n")
        for name, v in self.candidatures.items():
            s = ",".join([name] + v) + "\n"
            self.liste_candidatures.write(s)
        self.liste_candidatures.seek(0)
        self.distributeur = Distributeur(self.liste_candidatures.name,
                                         self.liste_cours.name)

    def tearDown(self):
        del self.liste_cours
        del self.liste_candidatures
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
