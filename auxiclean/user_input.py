from .gui import EqualityBreaker
import logging
import tkinter as tk


def input_choices(list_equalities, nchoices, course, master=None,
                  loglevel=logging.INFO):
    if master is not None:
        newWindow = tk.Toplevel(master)
        equalitybreaker = EqualityBreaker(list_equalities, nchoices, course,
                                          master=newWindow, loglevel=loglevel)
        master.wait_window(newWindow)
        return equalitybreaker.choices
    return command_line_input(list_equalities, nchoices, course, loglevel)


def command_line_input(list_equalities, nchoices, course, loglevel):
    logging.basicConfig()
    logger = logging.getLogger("CMD_input")
    logger.setLevel(loglevel)
    while True:
        logger.info("Des égalités sont présentes pour le cours %s." % course)
        logger.info("Il faut choisir %i candidat(e)s parmis:" % nchoices)
        for i, c in enumerate(list_equalities):
            logger.info("%i: %s" % (i + 1, c))
        choices_left = nchoices
        choices = []
        while choices_left:
            good_ans = False
            while not good_ans:
                ans = get_user_input("Choix #%i:" %
                                     (len(choices) + 1), loglevel)
                logger.debug("user input: %s" % ans)
                try:
                    choix = int(ans) - 1
                except ValueError:
                    logger.warning("SVP, veuillez entrer un nombre entier.")
                    continue
                else:
                    if choix < 0:
                        logger.warning("SVP, veuillez entrer un nombre > 0.")
                        continue
                good_ans = True
                choices.append(list_equalities[choix])
                choices_left -= 1
        logger.info("Vous avez choisis:")
        for c in choices:
            logger.info(c)
        good_ans = False
        while not good_ans:
            yes = get_user_input("Est-ce OK? [Oui/Non]:", loglevel)
            logger.debug("user input: %s" % yes)
            yes = yes.lower()
            if yes not in ("oui", "o", "y", "yes",
                           "non", "n", "no"):
                logger.warning("Veuillez entrer oui ou non SVP")
                continue
            else:
                good_ans = True
                if yes in ("oui", "o", "y", "yes"):
                    return choices
                # if No is entered here, the main loop will restart.


def get_user_input(text):  # pragma: no cover
    return input(text)
