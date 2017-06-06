from students import Students
from cours import Cours
import numpy as np
#Commentaire

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

    def Filtre(self, nombre_de_poste, liste_de_candidats, liste_des_etudiants):

        np.sort(liste_de_candidats)
        Candidats_Choisis = liste_de_candidats[:nombre_de_poste]
        Candidats_Refuses = liste_de_candidats[nombre_de_poste:]

        for Candidats in Candidats_Refuses :
            Candidats.dispos = str(int(Candidats.dispos) + 1)

        return(Candidats_Choisis)

    def make_distribution(self, liste_des_cours, liste_des_etudiants):
        while True:
            changement = 0
            for cours in liste_des_cours:
                for students in liste_des_etudiants:
                    if students.choix[0][1:] == cours.code:
                        if students.dispos != "0":
                            changement = 1
                            students.dispos = str(int(students.dispos) - 1)
                            cours.etudiants.append(students)
                            students.choix.pop(0)

                if (len(cours.etudiants)) > int(cours.dispos):
                    Candidats_Choisis = self.Filtre(int(cours.dispos),
                                            cours.etudiants,
                                            liste_des_etudiants)
                    cours.etudiants = Candidats_Choisis
            if changement == 0:
                break
        distribution = {}
        for cours in liste_des_cours:
            distribution[cours.name] = [e.name for e in cours.etudiants]
        return distribution

    def print_distribution(self):
        print("\n#####  DISTRIBUTION  #####")
        for cours, liste_tpistes in self.distribution.items():
            print("%s : %s" % (cours, str(liste_tpistes)))

if __name__ == "__main__":
    path_students = "../examples/students.csv"
    path_cours = "../examples/cours.csv"
    Distributeur(path_students, path_cours)