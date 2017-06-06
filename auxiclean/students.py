class Students:
    def __init__(self, name, choix1, choix2, choix3, choix4, choix5,
                 dispos, tp,
                 scolarite, nobel, programme, cote):
        self.name = name
        self.choix = [choix1, choix2, choix3, choix4, choix5]
        self.dispos = dispos
        self.tp = tp
        self.scolarite = scolarite
        self.nobel = nobel
        self.programme = programme
        self.cote = cote

    def __getitem__(self, key):
        return self.choix[0][key]

    def __repr__(self) :
        return(self.name)

    def __lt__(self, Students2) :
        if int(str(self.choix[0])[0]) < int(str(Students2.choix[0])[0]) :
            return False
        if int(str(self.choix[0])[0]) > int(str(Students2.choix[0])[0]) :
            return True
        if int(str(self.choix[0])[0]) == int(str(Students2.choix[0])[0]) :
            if self.tp < Students2.tp :
                return False
            if self.tp > Students2.tp :
                return True
            if self.tp == Students2.tp :
                if self.scholarite < Students2.scholarite :
                    return False
                if self.scholarite > Students2.scholarite :
                    return True
                if self.scholarite == Students2.scholarite :
                    if self.nobel < Students2.nobel :
                        return False
                    if self.nobel > Students2.nobel :
                        return True
                    if self.nobel == Students2.nobel :
                        if self.programme < Students2.programme :
                            return False
                        if self.programme > Students2.programme :
                            return True
                        if self.programme == Students2.programme :
                            if self.cote < Students2.cote :
                                return False
                            if self.cote > Students2.cote :
                                return True
                            if self.cote == Students2.cote :
                                string = ("Choisir le"
                                            " perdant entre 1 : %s et"
                                            " 2 : %s : " % (
                                            self.name,
                                            Students2.name))
                                egalite = input(string)
                                if egalite == 1 :
                                    return True
                                if egalite == 2 :
                                    return False