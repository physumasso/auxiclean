import abc
import logging
import tkinter as tk


class AuxiliaryWindow(abc.ABC):
    _title = None
    _loggername = None

    def __init__(self, master, loglevel=logging.INFO):
        """Base class for auxiliary windows (for DRY code).
        """
        self.master = master
        self.frame = tk.Frame(self.master)
        logging.basicConfig()
        self._logger = logging.getLogger(self._loggername)
        self._logger.setLevel(loglevel)
        self.init_window()
        self.create_window()
        self.frame.pack()

    @abc.abstractmethod
    def create_window(self):  # pragma: no cover
        # to implement in each subclass
        pass

    def init_window(self):
        top = self.frame.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

    def quit(self):
        self.master.destroy()
        return
