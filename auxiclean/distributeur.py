from .students import Students
from .cours import Cours


def get_user_input(text):
    return input(text)

class Distributeur:
    def __init__(self, students_path, cours_path):

        liste_des_etudiants = self._get_etudiants(students_path)
        liste_des_cours = self._get_cours(cours_path)
        self.distribution = self.make_distribution(liste_des_cours,
                                                   liste_des_etudiants)
        self.print_distribution()

    def _get_etudiants(self, path):
        liste = []
        print("\n#####  CANDIDATURES  #####")
        with open(path) as students_data:
            lines = students_data.readlines()
            for line in lines[1:]:
                s = Students(*line.split(','))
                print(s.name, s.choix)
                liste.append(s)
        return liste

    def _get_cours(self, path):
        liste = []
        print("\n#####  COURS A COMBLER  #####")
        with open(path) as class_data:
            lines = class_data.readlines()
            for line in lines[1:]:
                c = Cours(*line.split(","))
                print(c.name, c.code)
                liste.append(c)
        return liste

    def input_choices(self, list_equalities, nchoices, cours):
        while True:
            print("Des égalités sont présentes pour le cours %s." % cours)
            print("Il faut choisir %i candidat(e)s parmis:" % nchoices)
            for i, c in enumerate(list_equalities):
                print("%i: %c" % (i + 1, c))
            choices_left = nchoices
            choices = []
            while choices_left:
                good_ans = False
                while not good_ans:
                    ans = get_user_input("Choix #%i:" % len(choices) + 1)
                    try:
                        choix = int(ans) - 1
                    except ValueError:
                        print("SVP, veuillez entrer un nombre entier.")
                        continue
                    else:
                        if choix <= 0:
                            print("SVP, veuillez entrer un nombre > 0.")
                            continue
                    good_ans = True
                    choices.append(list_equalities[choix])
                    choices_left -= 1
            print("Vous avez choisis:")
            for c in choices:
                print(c)
            good_ans = False
            while not good_ans:
                yes = get_user_input("Est-ce OK? [Oui/Non]:")
                yes = yes.lower()
                if yes not in ("oui", "o", "y", "yes",
                               "non", "n", "no"):
                    print("Veuillez entrer oui ou non SVP")
                    continue
                else:
                    good_ans = True
                    if yes in ("oui", "o", "y", "yes"):
                        return choices
                    # if No is entered here, the main loop will restart.

    def choose_candidates(self, nombre_de_poste, liste_de_candidats, cours):
        if not nombre_de_poste:
            # no candidate to choose.
            return []
        liste_provisoire = liste_de_candidats[-nombre_de_poste:]
        liste_eq = []
        if liste_provisoire[0] == liste_de_candidats[:-nombre_de_poste][-1]:
            # possible equalities, we need to choose them manually
            # first, find_equalities that might change the outcome
            for c in liste_de_candidats:
                if c == liste_provisoire[0]:
                    liste_eq.append(c)
            # now find the number of these equal candidates inside provisoire
            same = [x for x in liste_provisoire if x == liste_provisoire[0]]
            n = len(same)
            for s in same:
                liste_provisoire.remove(s)
            # n is the number of candidates to choose in liste_eq
            choix = self.input_choices(liste_eq, n, cours)
            return choix + liste_provisoire
        return liste_provisoire

    def filtre(self, nombre_de_poste, liste_de_candidats, liste_des_etudiants,
               cours):
        # sort the list of candidates in ordre of worst to best
        liste_de_candidats = sorted(liste_de_candidats)
        # choosed candidates
        candidats_choisis = self.choose_candidates(nombre_de_poste,
                                                   liste_de_candidats,
                                                   cours)
        return candidats_choisis

    def make_distribution(self, liste_des_cours, liste_des_etudiants):
        changement = False
        while not changement:
            changement = False
            for cours in liste_des_cours:
                for students in liste_des_etudiants:
                    if students.choix[0][1:] == cours.code:
                        if students.dispos:
                            changement = True
                            cours.etudiants.append(students)
                            # remove choice from student choices
                            students.choix.pop(0)

                # if number of candidates is greater than number of positions,
                # we need to sort them out
                if len(cours.etudiants) > cours.dispos:
                    candidats_choisis = self.filtre(cours.dispos,
                                                    cours.etudiants,
                                                    liste_des_etudiants,
                                                    cours.name)
                    cours.etudiants = candidats_choisis
                # for each chosen candidates, remove one from their dispos
                for candidat in cours.etudiants:
                    candidat.dispos -= 1
            if not changement:
                break
        distribution = {}
        for cours in liste_des_cours:
            distribution[cours.name] = [e.name for e in cours.etudiants]
        return distribution

    def print_distribution(self):
        print("\n#####  DISTRIBUTION  #####")
        for cours, liste_tpistes in self.distribution.items():
            print("%s : %s" % (cours, str(liste_tpistes)))
