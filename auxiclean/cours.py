class Cours:
    def __init__(self, name, code, dispos, programme):
        self.name = name
        self.code = code.zfill(2)
        self.dispos = int(dispos)
        self.programme = programme
        self.etudiants = []
