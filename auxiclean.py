class Students:
    def __init__(self, line):
        self.Name = line[0]
        self.Choix = [line[1], line[2], line[3], line[4], line[5]]
        self.Dispo = line[6]
        self.Tp = line[7]
        self.Scholarite = line[8]
        self.Nobel = line[9]
        self.Programme = line[10]
        self.Cote = line[11]


class Cours:
    def __init__(self, line):
        self.Name = line[0]
        self.Code = line[1].zfill(2)
        self.Dispo = line[2]
        self.Programme = line[3]
        self.Etudiants = []


Liste_des_etudiants = []
Liste_des_cours = []

with open('examples/students.csv') as students_data:
    next(students_data)
    for line in students_data:
        print(line.split(',')[1][1:])
        print(line.split(','))
        Liste_des_etudiants.append(Students(line.split(',')))

with open('examples/cours.csv') as class_data:
    next(class_data)
    for line in class_data:
        Liste_des_cours.append(Cours(line.split(',')))


def find_best(Stat_1, Stat_2):
    if Stat_1 > Stat_2:
        return True
    if Stat_1 == Stat_2:
        return None
    else:
        return False


def Bestmatch(Nombre_De_Poste, Liste_De_Candidats, Nom_du_cours):

    Classement = []
    Personnes_Selectionnees = []

    for Candidats in Liste_De_Candidats:
        he_is_placed = False
        if Classement == []:
            Classement.append(Candidats)
        else:
            index = 0
            for person in Classement:
                if he_is_placed is False:
                    for i in range(1, 7):
                        if he_is_placed is False:
                            results = find_best(Candidats[i], person[i])
                            if results is True:
                                Classement.insert(index, Candidats)
                                he_is_placed = True
                            if results is False:
                                break
                            if results is None:
                                if i == 6:
                                    string = ("Pour le cours %s, choisir le"
                                              " gagnant entre 1 : %s et"
                                              " 2 : %s : " % (Nom_du_cours,
                                                              Candidats[0],
                                                              person[0]))
                                    egalite = input(string)
                                    print("Vous avez choisi %s" % egalite)
                                    if egalite == 1:
                                        Classement.insert(index, Candidats)
                                        he_is_placed = True
                    index = index + 1
            if he_is_placed is False:
                Classement.append(Candidats)

    Rang = 0

    for person in Classement:
        if Rang < Nombre_De_Poste:
            Personnes_Selectionnees.append(person)
        else:
            for Etudiant in Liste_des_etudiants:
                if Etudiant.Name == person[0]:
                    Etudiant.Dispo = str(int(Etudiant.Dispo) + 1)
        Rang = Rang + 1
    return Personnes_Selectionnees


while True:
    Changement = 0
    for Cours in Liste_des_cours:
        for Students in Liste_des_etudiants:
            if Students.Choix[0][1:] == Cours.Code:
                if Students.Dispo != "0":
                    Changement = 1
                    Students.Dispo = str(int(Students.Dispo) - 1)
                    Cours.Etudiants.append([Students.Name,
                                            int(Students.Choix[0][1]),
                                            int(Students.Tp),
                                            int(Students.Scholarite),
                                            int(Students.Nobel),
                                            int(Students.Programme),
                                            int(Students.Cote)])
                    Students.Choix.pop(0)

        if (len(Cours.Etudiants)) > int(Cours.Dispo):
            Best = Bestmatch(int(Cours.Dispo), Cours.Etudiants, Cours.Name)
            Cours.Etudiants = []
            for Personne in Best:
                Cours.Etudiants.append(Personne)
    if Changement == 0:
        break

for Cours in Liste_des_cours:
    print("\nPour le cours : %s, les etudiants sont :" % Cours.Name)
    for Etudiants in Cours.Etudiants:
        print("%s") % Etudiants[0]
