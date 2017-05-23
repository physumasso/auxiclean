from students import Students
from cours import Cours

#Commentaire

class Distributeur:
    def __init__(self, students_path, cours_path):

        liste_des_etudiants = self._get_etudiants(students_path)
        liste_des_cours = self._get_cours(cours_path)
        self.selection = self.selection(liste_des_cours, liste_des_etudiants)

    def _get_etudiants(self, path):
        liste = []
        with open(path) as students_data:
            lines = students_data.readlines()
            for line in lines[1:]:
                print(line.split(',')[1][1:])
                print(line.split(','))
                liste.append(Students(*line.split(',')))
        return liste

    def _get_cours(self, path):
        liste = []
        with open(path) as class_data:
            lines = class_data.readlines()
            for line in lines[1:]:
                liste.append(Cours(*line.split(',')))
        return liste

    def find_best(self, stat_1, stat_2):
        if stat_1 > stat_2:
            return True
        if stat_1 == stat_2:
            return None
        else:
            return False

    def bestmatch(self, nombre_de_poste, liste_de_candidats, nom_du_cours,
                  liste_des_etudiants):

        classement = []
        personnes_selectionnees = []

        for candidats in liste_de_candidats:
            he_is_placed = False
            if not len(classement):
                classement.append(candidats)
            else:
                index = 0
                for person in classement:
                    if he_is_placed is False:
                        for i in range(1, 7):
                            if he_is_placed is False:
                                results = self.find_best(candidats[i],
                                                         person[i])
                                if results is True:
                                    classement.insert(index, candidats)
                                    he_is_placed = True
                                if results is False:
                                    break
                                if results is None:
                                    if i == 6:
                                        string = ("Pour le cours %s,"
                                                  " choisir le"
                                                  " gagnant entre 1 : %s et"
                                                  " 2 : %s : " % (nom_du_cours,
                                                                  candidats[0],
                                                                  person[0]))
                                        egalite = input(string)
                                        print("Vous avez choisi %s" % egalite)
                                        if egalite == 1:
                                            classement.insert(index, candidats)
                                            he_is_placed = True
                        index = index + 1
                if he_is_placed is False:
                    classement.append(candidats)

        rang = 0

        for person in classement:
            if rang < nombre_de_poste:
                personnes_selectionnees.append(person)
            else:
                for etudiant in liste_des_etudiants:
                    if etudiant.name == person[0]:
                        etudiant.dispos = str(int(etudiant.dispos) + 1)
            rang += 1
        return personnes_selectionnees

    def selection(self, liste_des_cours, liste_des_etudiants):
        while True:
            changement = 0
            for cours in liste_des_cours:
                for students in liste_des_etudiants:
                    if students.choix[0][1:] == cours.code:
                        if students.dispos != "0":
                            changement = 1
                            students.dispos = str(int(students.dispos) - 1)
                            cours.etudiants.append([students.name,
                                                    int(students.choix[0][1]),
                                                    int(students.tp),
                                                    int(students.scolarite),
                                                    int(students.nobel),
                                                    int(students.programme),
                                                    int(students.cote)])
                            students.choix.pop(0)

                if (len(cours.etudiants)) > int(cours.dispos):
                    best = self.bestmatch(int(cours.dispos),
                                          cours.etudiants,
                                          cours.name,
                                          liste_des_etudiants)
                    cours.etudiants = []
                    for personne in best:
                        cours.etudiants.append(personne)
            if changement == 0:
                break

        for cours in liste_des_cours:
            print("\nPour le cours : %s, les etudiants sont :" % cours.name)
            for etudiants in cours.etudiants:
                print(etudiants[0])


if __name__ == "__main__":
    path_students = "../examples/students.csv"
    path_cours = "../examples/cours.csv"
    Distributeur(path_students, path_cours)
