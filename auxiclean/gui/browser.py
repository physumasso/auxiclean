from ..handler import TextHandler
from auxiclean import MAINLOGGER, Selector
from timeit import default_timer as timer
from .settings_gui import SettingsGUI
from ..managers import ConfigManager
from tkinter import scrolledtext, filedialog, messagebox
import auxiclean
import tkinter as tk
import os
import logging
import traceback
import webbrowser


class Browser:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.grid(sticky=tk.E + tk.W)
        self.master.title("Auxiclean - GUI - version: %s" %
                          auxiclean.__version__)
        # load config
        self.config_manager = ConfigManager()
        # browser logger
        logging.basicConfig()
        self._logger = logging.getLogger("auxiclean.browser")
        self._logger.setLevel(self.config_manager.loglevel)
        self.createMainWindow()

    def createMainWindow(self):
        top = self.frame.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        # create text box to specify path
        self.pathBox = tk.Entry(self.frame)
        self.labelPathBox = tk.Label(self.frame, text="Fichier Excel:")
        self.labelPathBox.grid(column=0)
        self.pathBox.grid(column=1, row=0,
                          sticky=tk.E + tk.W)
        # insert last excel file used
        self.pathBox.insert(0, self.config_manager.last_excel_file)
        # create browse button
        self.browseButton = tk.Button(self.frame, text="Chercher",
                                      command=self.select_file)
        self.browseButton.grid(column=2, row=0)
        # create run button
        self.runButton = tk.Button(self.frame, text="Exécution",
                                   command=self.run_selector)
        self.runButton.grid(row=1, column=0)
        # creates settings button
        self.settingsButton = tk.Button(self.frame, text="Paramètres",
                                        command=self.settings_config)
        self.settingsButton.grid(row=1, column=2)
        # create quit button
        self.quitButton = tk.Button(self.frame, text="Quitter",
                                    command=self.frame.quit)
        self.quitButton.grid()
        # create DEBUG button (for verbose option in GUI)
        self.debugCheckButton = tk.Variable()
        _actual_button = tk.Checkbutton(self.frame,
                                        text=" Full traceback (DEBUG)",
                                        anchor="e",
                                        variable=self.debugCheckButton)
        _actual_button.deselect()
        _actual_button.grid(row=2, column=1, columnspan=2)

        # create log box
        # adapted from this SO post:
        # https://stackoverflow.com/a/41959785/6362595
        # Add text widget to display logging info
        self.logBox = scrolledtext.ScrolledText(self.frame,
                                                state='disabled')
        self.logBox.configure(font='TkFixedFont')
        self.logBox.grid(sticky=tk.W + tk.E + tk.S, columnspan=3)

        # Create textLogger
        self.text_handler = TextHandler(self.logBox)

        # Logging configuration
        MAINLOGGER.addHandler(self.text_handler)
        # bug report link (button)
        self.bug_report = tk.Label(self.frame,
                                   text="Il y a un bug? Écrivez le ici!",
                                   fg="blue",
                                   cursor="hand2")
        self.bug_report.grid(column=0, sticky=tk.W + tk.S, columnspan=3)
        self.bug_report.bind("<Button-1>", self.bug_callback)

    def bug_callback(self, event):
        webbrowser.open_new(r"https://github.com/physumasso/auxiclean/issues")

    def settings_config(self):
        newWindow = tk.Toplevel(self.master)
        SettingsGUI(self.config_manager, newWindow,
                    loglevel=self.config_manager.loglevel)
        self.master.wait_window(newWindow)
        # settup new loglevel if changed
        self._logger.setLevel(self.config_manager.loglevel)

    def run_selector(self):
        path = self.pathBox.get()
        if not len(path):
            self._logger.error("Veuiller entrer un fichier Excel.")
            return

        path = os.path.abspath(path)
        if not os.path.exists(path):
            self._logger.error("%s n'existe pas!" % path)
            return
        if not os.path.isfile(path):
            self._logger.error("%s n'est pas un fichier." % path)
            return
        if not path.endswith(".xlsx") and not path.endswith(".ods"):
            self._logger.error("%s doit être un fichier excel ou ods." % path)
            return
        # path is good, save it for next time user open program
        self.config_manager.last_excel_file = path
        self.config_manager.write_config()

        start = None
        try:
            # warn user to close the excel file
            self.warn_user_excel(path)
            self._logger.info("Exécution ... ceci peut prendre"
                              " quelques minutes ...")
            # time process
            start = timer()
            Selector(path, master=self.master,
                     loglevel=self.config_manager.loglevel)
        except Exception as e:
            if not int(self.debugCheckButton.get()):
                self._logger.error("%s" % e)
            else:
                # print full traceback
                tb = traceback.format_exc()
                self._logger.error(tb)
            self._logger.critical("STOP - ERREUR")
        else:
            self._forceprint("Succès!")
        finally:
            end = timer()
            if start is None:
                # an error occured before the call to the selector
                return
            self._forceprint("Temps d'exécution = %.3f secondes" %
                             (end - start))

    def _forceprint(self, text):
        # method to force print into the logging tag even though
        # the loglevel is higher
        # to force print this, adjust the level and set it back
        previous_level = self._logger.level
        self._logger.setLevel(logging.INFO)
        self._logger.info(text)
        self._logger.setLevel(previous_level)

    def select_file(self):
        data_file = filedialog.askopenfile(parent=self.master,
                                           mode='rb',
                                           title='Sélectioner'
                                                 ' Fichier Excel')
        if data_file is not None:
            path = data_file.name
            data_file.close()
        else:
            return
        # delete previous text
        text = len(self.pathBox.get())
        self.pathBox.delete(0, last=text)
        self.pathBox.insert(0, path)

    def warn_user_excel(self, path):
        if not self.config_manager.excel_file_open_warning:
            return
        text = ("Attention!\n\n Veuillez vous assurer que \n"
                " la fenêtre Excel (ou"
                " OpenOffice) du"
                " fichier suivant est fermée:\n\n %s \n\n"
                "Si ce n'est pas le cas, la distribution ne pourra\n"
                " pas être écrite dans le fichier." % path)
        messagebox.showinfo("Attention", text)
