from .auxiliary_window import AuxiliaryWindow
from ..managers.config_manager import (NonUniquePriority, NonValidPriority,
                                       MissingPriority)
import logging
import tkinter as tk


logdict = {"DEBUG": logging.DEBUG,
           "INFO": logging.INFO,
           "WARNING": logging.WARNING,
           "ERROR": logging.ERROR,
           "CRITICAL": logging.CRITICAL}


priorities_traduction = {"course_given": "Nombre de fois le cours a été donné",
                         "total_courses_given": "Nombre total de cours donné",
                         "scolarity": "Cycle d'étude",
                         "nobels": "Nombre de prix d'enseignement",
                         "gpa": "Moyenne globale (notes)"}


def key_dict(value, dictionary):
    for k, v in dictionary.items():
        if v == value:
            return k
    raise KeyError("There is no key for %s." % str(value))


class SettingsGUI(AuxiliaryWindow):
    _title = "Configuration"
    _loggername = "auxiclean.gui.settings"

    def __init__(self, config_manager, *args, **kwargs):
        self.config_manager = config_manager
        super().__init__(*args, **kwargs)

    def create_window(self):
        # == config tools ==
        info = ("Fenêtre de configurations. Cliquer sur <<Appliquer>> pour"
                " sauvegarder.")
        self.infotext = tk.Label(self.frame, text=info)
        self.infotext.grid(column=0, row=0)
        # loglevel
        self.create_loglevel_setter()
        # Priorities order.
        self.create_priorities_orderer()
        # excel open file warning check box
        self.create_excel_warning_checkbox()
        # Apply button
        self.create_apply_button()
        # quit button
        self.create_ok_button()

    def create_excel_warning_checkbox(self):
        # description
        text = ("Avertissement fenêtre ouverte:\n"
                " Si cette case est cochée, un avertissement survient pour\n"
                " rappeler de fermer la fenêtre excel.")
        self.excelwarninglabel = tk.Label(self.frame, text=text,
                                          justify=tk.LEFT)
        self.excelwarninglabel.grid(column=0)
        self.excelwarningvar = tk.Variable()
        checkbox = tk.Checkbutton(self.frame,
                                  variable=self.excelwarningvar)

        if self.config_manager.excel_file_open_warning:
            checkbox.select()
        else:
            checkbox.deselect()
        self.excelwarningcheckbox = checkbox
        row = int(self.excelwarninglabel.grid_info()["row"])
        self.excelwarningcheckbox.grid(row=row, column=1)

    def create_priorities_orderer(self):
        # description
        text = ("Ordonnanceur de priorités:\n choisir l'ordre des critères"
                " à considérer\n lorsque deux candidatures sont comparées.")
        self.orderertext = tk.Label(self.frame, text=text, justify=tk.LEFT)
        self.orderertext.grid(column=0, row=3)
        # orderer
        self.priority_choices = []
        row = 4
        for i, priority in enumerate(self.config_manager.priorities):
            text = "Critère #%i" % (i + 1)
            label = tk.Label(self.frame, text=text)
            label.grid(column=0, row=row + i)
            orderervar = tk.StringVar(self.master)
            orderervar.set(priorities_traduction[priority])
            orderermenu = tk.OptionMenu(self.frame, orderervar,
                                        *list(priorities_traduction.values()))
            orderermenu.grid(column=1, row=row + i)
            self.priority_choices.append(orderervar)

    def apply_new_settings(self):
        # get loglevel setting
        self.config_manager.loglevel = logdict[self.loglevelvar.get()]
        # get excel open file warning setting
        checked = self.excelwarningvar.get()
        self.config_manager.excel_file_open_warning = checked == "1"
        # get priorities settings
        priorities = [key_dict(x.get(), priorities_traduction)
                      for x in self.priority_choices]
        try:
            self.config_manager.priorities = tuple(priorities)
        except MissingPriority as e:
            self._logger.error("There is a missing priority.")
            self._logger.error(str(e))
            return
        except NonValidPriority as e:
            self._logger.error("There is a non valid priority.")
            self._logger.error(str(e))
            return
        except NonUniquePriority as e:
            self._logger.error("There is non unique priorities.")
            self._logger.error(str(e))
            return
        self.config_manager.write_config()

    def create_ok_button(self):
        self.okbutton = tk.Button(self.frame, text="Quitter",
                                  command=self.quit)
        self.okbutton.grid(column=1,
                           row=int(self.applybutton.grid_info()["row"]))

    def create_apply_button(self):
        self.applybutton = tk.Button(self.frame, text="Appliquer",
                                     command=self.apply_new_settings,
                                     anchor=tk.W)
        self.applybutton.grid(column=0)

    def create_loglevel_setter(self):
        logleveltext = ("Niveau du log : contrôle la quantité"
                        " d'informations affichées.\n"
                        "DEBUG=toutes les infos sont affichées.\n"
                        "CRITICAL=seules les infos critiques sont affichées.")
        self.logleveltext = tk.Label(self.frame, text=logleveltext,
                                     justify=tk.LEFT)
        self.logleveltext.grid(column=0, row=1, rowspan=2)
        self.loglevel_boxtext = tk.Label(self.frame, text="Niveau du log:",
                                         anchor=tk.W)
        self.loglevel_boxtext.grid(column=1,
                                   row=1)
        # loglevel dropdown menu
        self.loglevelvar = tk.StringVar(self.master)
        self.loglevelvar.set(key_dict(self.config_manager.loglevel, logdict))
        self.loglevelmenu = tk.OptionMenu(self.frame, self.loglevelvar,
                                          *list(logdict.keys()))
        self.loglevelmenu.grid(column=1, row=2)
