import copy
from .candidate import CourseCandidate


class Course:
    def __init__(self, name, code, positions, discipline):
        self.code = code
        if self.code is None:
            raise ValueError("Course has no code!")
        self.name = name.strip() if name is not None else self.code
        self.positions = int(positions)
        self.discipline = (discipline.lower().strip() if discipline is not None
                           else "générale")
        self.candidates = []

    def add_candidate(self, candidate, priorities):
        """Add candidate to course as a CourseCandidate object.
        """
        # make a deep copy of the candidate to not lose infos
        cp = copy.deepcopy(candidate)
        # use course candidate for comparision between candidates for the
        # specific course
        storedcandidate = CourseCandidate(cp, self, priorities)
        self.candidates.append(storedcandidate)

    def __repr__(self):  # pragma: no cover
        return "%s - %s" % (self.code, self.name)

    def __str__(self):
        s = ("%s - %s: max=%i" % (self.code, self.name, self.positions))
        return s
