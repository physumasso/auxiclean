from tkinter import messagebox, scrolledtext
from .handler import TextHandler
import logging
import tkinter as tk


class EqualityBreaker:
    def __init__(self, candidates, nchoices, course, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.master.title("Auxiclean - EqualityBreaker")
        # Logging configuration
        self.logger = logging.getLogger("auxiclean.equalitybreaker")
        self.nchoices = nchoices
        self.choices = []
        self.createWindow(candidates, nchoices, course)
        self.frame.pack()

    def createWindow(self, candidates, nchoices, course):
        top = self.frame.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
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
            l = tk.Checkbutton(self.frame, text=candidate.name,
                               anchor="w",
                               variable=d["var"],
                               )
            l.deselect()
            l.grid(row=i + 1, column=0)
        # done button
        self.doneButton = tk.Button(self.frame, text="Terminé",
                                    command=self.compile_results)
        self.doneButton.grid()

        # create log box
        # adapted from this SO post:
        # https://stackoverflow.com/a/41959785/6362595
        # Add text widget to display logging info
        self.logBox = scrolledtext.ScrolledText(self.frame, state='disabled')
        self.logBox.configure(font='TkFixedFont')
        self.logBox.grid(sticky='w', columnspan=1)

        # Create textLogger
        self.text_handler = TextHandler(self.logBox)

        # Logging configuration
        self.logger.addHandler(self.text_handler)

    def compile_results(self):
        choices = self.get_checkboxes_results()
        if len(choices) == self.nchoices:
            confirm = messagebox.askquestion("Confirmer Choix",
                                             "Êtes-vous sûr(e) de ces choix?")
            if confirm == "yes":
                self.choices = choices
                self.master.destroy()
                return
            else:
                # confirm == "no"
                return
        self.logger.warn("Nombre de candidatures choisies invalide (%i/%i)" %
                         (len(choices), self.nchoices))

    def get_checkboxes_results(self):
        results = []
        for name, checkbox in self.checkbuttons.items():
            if int(checkbox["var"].get()):
                # if button is toggled, it will return 1. otherwise 0
                results.append(self.checkbuttons[name]["candidate"])
        return results


def input_choices(list_equalities, nchoices, course, master=None):
    if master is not None:
        newWindow = tk.Toplevel(master)
        equalitybreaker = EqualityBreaker(list_equalities, nchoices, course,
                                          master=newWindow)
        master.wait_window(newWindow)
        return equalitybreaker.choices
    return command_line_input(list_equalities, nchoices, course)


def command_line_input(list_equalities, nchoices, course):
    while True:
        logging.info("Des égalités sont présentes pour le cours %s." % course)
        logging.info("Il faut choisir %i candidat(e)s parmis:" % nchoices)
        for i, c in enumerate(list_equalities):
            logging.info("%i: %s" % (i + 1, c))
        choices_left = nchoices
        choices = []
        while choices_left:
            good_ans = False
            while not good_ans:
                ans = get_user_input("Choix #%i:" %
                                     (len(choices) + 1))
                try:
                    choix = int(ans) - 1
                except ValueError:
                    logging.warn("SVP, veuillez entrer un nombre entier.")
                    continue
                else:
                    if choix < 0:
                        logging.warn("SVP, veuillez entrer un nombre > 0.")
                        continue
                good_ans = True
                choices.append(list_equalities[choix])
                choices_left -= 1
        logging.info("Vous avez choisis:")
        for c in choices:
            logging.info(c)
        good_ans = False
        while not good_ans:
            yes = get_user_input("Est-ce OK? [Oui/Non]:")
            yes = yes.lower()
            if yes not in ("oui", "o", "y", "yes",
                           "non", "n", "no"):
                logging.warn("Veuillez entrer oui ou non SVP")
                continue
            else:
                good_ans = True
                if yes in ("oui", "o", "y", "yes"):
                    return choices
                # if No is entered here, the main loop will restart.


def get_user_input(text):  # pragma: no cover
    return input(text)
