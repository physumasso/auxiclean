from ..selector import Selector
from ..handler import TextHandler
from tkinter import filedialog, scrolledtext
from auxiclean import MAINLOGGER
from timeit import default_timer as timer
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
        # browser logger
        self.logger = logging.getLogger("auxiclean.browser")
        self.createMainWindow()
        self.frame.pack()

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
        # create browse button
        self.browseButton = tk.Button(self.frame, text="Chercher",
                                      command=self.select_file)
        self.browseButton.grid(column=2, row=0)
        # create run button
        self.runButton = tk.Button(self.frame, text="Exécution",
                                   command=self.run_selector)
        self.runButton.grid()
        # create quit button
        self.quitButton = tk.Button(self.frame, text="Quitter",
                                    command=self.frame.quit)
        self.quitButton.grid()
        # create DEBUG button (for verbose option in GUI)
        self.debugCheckButton = tk.Variable()
        _actual_button = tk.Checkbutton(self.frame,
                                        text="Full traceback (DEBUG)",
                                        anchor="e",
                                        variable=self.debugCheckButton)
        _actual_button.deselect()
        _actual_button.grid(row=2, column=2)

        # create log box
        # adapted from this SO post:
        # https://stackoverflow.com/a/41959785/6362595
        # Add text widget to display logging info
        self.logBox = scrolledtext.ScrolledText(self.frame, state='disabled')
        self.logBox.configure(font='TkFixedFont')
        self.logBox.grid(sticky='w', columnspan=3)

        # Create textLogger
        self.text_handler = TextHandler(self.logBox)

        # Logging configuration
        MAINLOGGER.addHandler(self.text_handler)
        # bug report link (button)
        self.bug_report = tk.Label(self.frame,
                                   text="Il y a un bug? Écrivez le ici!",
                                   fg="blue",
                                   cursor="hand2")
        self.bug_report.grid(column=0)
        self.bug_report.bind("<Button-1>", self.bug_callback)

    def bug_callback(self, event):
        webbrowser.open_new(r"https://github.com/physumasso/auxiclean/issues")

    def run_selector(self):
        path = self.pathBox.get()
        if not len(path):
            self.logger.error("Veuiller entrer un fichier Excel.")
            return

        path = os.path.abspath(path)
        if not os.path.exists(path):
            self.logger.error("%s n'existe pas!" % path)
            return
        if not os.path.isfile(path):
            self.logger.error("%s n'est pas un fichier." % path)
            return
        if not path.endswith(".xlsx") and not path.endswith(".ods"):
            self.logger.error("%s doit être un fichier excel ou ods." % path)
            return

        start = None
        try:
            # warn user to close the excel file
            self.warn_user_excel(path)
            self.logger.info("Exécution ... ceci peut prendre"
                             " quelques minutes ...")
            # time process
            start = timer()
            Selector(path, master=self.master)
        except Exception as e:
            if not int(self.debugCheckButton.get()):
                self.logger.error("%s" % e)
            else:
                # print full traceback
                tb = traceback.format_exc()
                self.logger.error(tb)
            self.logger.info("STOP - ERREUR")
        else:
            self.logger.info("Succès!")
        finally:
            end = timer()
            if start is None:
                # an error occured before the call to the selector
                return
            self.logger.info("Temps d'exécution = %.3f secondes" %
                             (end - start))

    def select_file(self):
        data_file = filedialog.askopenfile(parent=self.master,
                                           mode='rb',
                                           title='Sélectioner Fichier Excel')
        if data_file is not None:
            path = data_file.name
            data_file.close()
        # delete previous text
        l = len(self.pathBox.get())
        self.pathBox.delete(0, last=l)
        self.pathBox.insert(0, path)

    def warn_user_excel(self, path):
        # create new window
        newWindow = tk.Toplevel(self.master)
        WarnExcelWindow(path, master=newWindow)
        self.master.wait_window(newWindow)


class WarnExcelWindow:
    def __init__(self, path, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.master.title("Attention")
        # logging config
        self.logger = logging.getLogger("auxiclean.gui.WarnExcelWindow")
        self.create_window(path)
        self.frame.pack()

    def create_window(self, path):
        top = self.frame.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        text = ("Attention!\n\n Veuillez vous assurer que \n"
                " la fenêtre Excel (ou"
                " OpenOffice) du"
                " fichier suivant est fermée:\n\n %s \n\n"
                "Si ce n'est pas le cas, la distribution ne pourra\n"
                " pas être écrite dans le fichier." % path)
        self.text = tk.Label(self.frame, text=text, anchor=tk.W,
                             justify=tk.CENTER)
        self.text.grid(column=0, row=0)
        self.okButton = tk.Button(self.frame, text="OK",
                                  command=self.quit)
        self.okButton.grid()

    def quit(self):
        self.master.destroy()
        return
