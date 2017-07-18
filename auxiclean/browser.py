from .selector import Selector
from .handler import TextHandler
from tkinter import filedialog, scrolledtext
from auxiclean import MAINLOGGER
import tkinter as tk
import os
import logging


class Browser:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.grid(sticky=tk.E + tk.W)
        self.master.title("Auxiclean - GUI")
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

    def run_selector(self):
        path = self.pathBox.get()
        path = os.path.abspath(path)
        try:
            Selector(path, master=self.master)
        except Exception as e:
            self.logger.error("%s" % e)
        else:
            self.logger.info("Succès!")

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
