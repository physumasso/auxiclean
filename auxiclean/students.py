class Students:
    def __init__(self, name, choix1, choix2, choix3, choix4, choix5,
                 dispos, tp,
                 scolarite, nobel, programme, cote):
        self.name = name
        self.choix = [choix1, choix2, choix3, choix4, choix5]
        self.dispos = int(dispos)
        self.tp = int(tp)
        self.scolarite = int(scolarite)
        self.nobel = int(nobel)
        self.programme = programme
        self.cote = float(cote)

    def __repr__(self):
        return self.name

    def __lt__(self, student2):
        # first criterion: the number of this tp given
        if int(self.choix[0][0]) < int(student2.choix[0][0]):
            return True
        # second criterion: the number of tp given
        if self.tp < student2.tp:
            return True
        # third criterion: scolarity
        if self.scolarite < student2.scolarite:
            return True
        # fourth criterion: number of nobel prize won
        if self.nobel < student2.nobel:
            return True
        # fifth criterion: is the same prog as the course?
        if self.programme < student2.programme:
            return True
        # sixth criterion: gpa
        if self.cote < student2.cote:
            return True
        return False

    def __eq__(self, student2):
        if int(self.choix[0][0]) != int(student2.choix[0][0]):
            return False
        if self.tp != student2.tp:
            return False
        if self.scolarite != student2.scolarite:
            return False
        if self.nobel != student2.nobel:
            return False
        if self.programme != student2.programme:
            return False
        if self.cote != student2.cote:
            return False
        return True
