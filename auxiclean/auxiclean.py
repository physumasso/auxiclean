from students import Students
from cours import Cours
import numpy as np

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
                liste.append(Students(*line.split(',')))
        return liste

    def _get_cours(self, path):
        liste = []
        with open(path) as class_data:
            lines = class_data.readlines()
            for line in lines[1:]:
                liste.append(Cours(*line.split(',')))
        return liste

    def Filtre(self, nombre_de_poste, liste_de_candidats, liste_des_etudiants):

        np.sort(liste_de_candidats)

        Candidats_Choisis = liste_de_candidats[:nombre_de_poste]
        Candidats_Refuses = liste_de_candidats[nombre_de_poste:]

        print(Candidats_Choisis)

        for Candidats in Candidats_Refuses :
            Candidats.dispos = str(int(Candidats.dispos) + 1)

        return(Candidats_Choisis)

    def selection(self, liste_des_cours, liste_des_etudiants):
        while True:
            changement = 0
            for cours in liste_des_cours:
                for students in liste_des_etudiants:
                    if students.choix[0][1:] == cours.code :
                        if students.dispos != "0":
                            changement = 1
                            students.dispos = str(int(students.dispos) - 1)
                            cours.etudiants.append(students)
                            students.choix.pop(0)
                            print(students.choix)

                if (len(cours.etudiants)) > int(cours.dispos):
                    cours.etudiants = self.Filtre(int(cours.dispos),
                                                    cours.etudiants,
                                                    liste_des_etudiants)

            if changement == 0:
                break

        for cours in liste_des_cours:
            print("\nPour le cours : %s, les etudiants sont :" % cours.name)
            for etudiants in cours.etudiants:
                print(etudiants.name)

if __name__ == "__main__":
    path_students = "../examples/students.csv"
    path_cours = "../examples/cours.csv"
    Distributeur(path_students, path_cours)
