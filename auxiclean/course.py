class Course:
    def __init__(self, name, code, positions, discipline):
        self.code = code
        if self.code is None:
            raise ValueError("Course has no code!")
        self.name = name if name is not None else self.code
        self.positions = int(positions)
        self.discipline = discipline if discipline is not None else "générale"
        self.candidates = []

    def __repr__(self):  # pragma: no cover
        return self.name
