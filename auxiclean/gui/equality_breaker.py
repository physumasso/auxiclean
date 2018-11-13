from .auxiliary_window import AuxiliaryWindow
from ..handler import TextHandler
import tkinter as tk


class EqualityBreaker(AuxiliaryWindow):
    _title = "Auxiclean - EqualityBreaker"
    _loggername = "auxiclean.gui.equality_breaker"

    def __init__(self, candidates, nchoices, course, *args, **kwargs):
        # Logging configuration
        self.nchoices = nchoices
        self.choices = []
        self.course = course
        self.candidates = candidates
        super().__init__(*args, **kwargs)

    def create_window(self):
        candidates = self.candidates
        nchoices = self.nchoices
        course = self.course
        # instructions
        p = ("Des égalités sont présentes pour le cours: %s.\n"
             "Il faut choisir %i candidat(e)s parmis les choix suivants.\n"
             "SVP, cocher les candidatures désirées pour ce cours." %
             (course, nchoices))
        self.instructionsText = tk.Label(self.frame, text=p, anchor=tk.W,
                                         justify=tk.LEFT)
        self.instructionsText.grid(column=0, row=0)

        # candidates list, create checkboxes
        self.checkbuttons = {}
        for i, candidate in enumerate(candidates):
            d = {"var": tk.Variable(),
                 "candidate": candidate}
            self.checkbuttons[candidate.name] = d
            button = tk.Checkbutton(self.frame, text=candidate.name,
                                    anchor="w",
                                    variable=d["var"],
                                    )
            button.deselect()
            button.grid(row=i + 1, column=0)
        # done button
        self.doneButton = tk.Button(self.frame, text="Terminé",
                                    command=self.compile_results)
        self.doneButton.grid()

        # create log box
        # adapted from this SO post:
        # https://stackoverflow.com/a/41959785/6362595
        # Add text widget to display logging info
        self.logBox = tk.scrolledtext.ScrolledText(self.frame,
                                                   state='disabled')
        self.logBox.configure(font='TkFixedFont')
        self.logBox.grid(sticky='w', columnspan=1)

        # Create textLogger
        self.text_handler = TextHandler(self.logBox)

        # Logging configuration
        self._logger.addHandler(self.text_handler)

    def compile_results(self):
        choices = self.get_checkboxes_results()
        if len(choices) == self.nchoices:
            confirm = tk.messagebox.askquestion("Confirmer Choix",
                                                "Êtes-vous sûr(e)"
                                                " de ces choix?")
            if confirm == "yes":
                self.choices = choices
                self.quit()
                return
            else:
                # confirm == "no"
                return
        self._logger.warning("Nombre de candidatures choisies"
                             " invalide (%i/%i)" %
                             (len(choices), self.nchoices))

    def get_checkboxes_results(self):
        results = []
        for name, checkbox in self.checkbuttons.items():
            if int(checkbox["var"].get()):
                # if button is toggled, it will return 1. otherwise 0
                results.append(self.checkbuttons[name]["candidate"])
        return results
