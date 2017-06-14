class Course:
    def __init__(self, name, code, positions, discipline):
        self.name = name
        self.code = code.zfill(2)
        self.positions = int(positions)
        self.discipline = discipline
        self.candidates = []
