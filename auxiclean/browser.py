from .selector import Selector
import tkinter
from tkinter import filedialog
root = tkinter.Tk()


class Browser:
    def __init__(self):
        path_file = self.select_path_file()
        Selector(path_file)

    def select_path_file(self):
        data_file = filedialog.askopenfile(parent=root, mode='rb',
                                           title='Choose the data file')
        if data_file is not None:
            path_file = data_file.name
            data_file.close()
        return path_file
