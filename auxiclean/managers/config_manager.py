import configparser
import logging
import os


DEFAULT_CONFIG_PATH = os.path.join(os.path.expanduser("~"),
                                   ".config", "auxiclean")


# the priorities key should match the attributes name of a Candidate object
DEFAULT_PARAMETERS = {"last_excel_file": "",
                      "priorities": ("is_graduate",
                                     "course_given",
                                     "total_courses_given",
                                     "scolarity",
                                     "nobels",
                                     "gpa",
                                     ),
                      "loglevel": logging.ERROR,
                      "excel_file_open_warning": True,
                      }

PARAMETERS = DEFAULT_PARAMETERS.keys()
PRIORITY_PARAMS = DEFAULT_PARAMETERS["priorities"]


class NonUniquePriority(Exception):
    pass


class NonValidPriority(Exception):
    pass


class MissingPriority(Exception):
    pass


class ConfigManager:
    def __init__(self, path=DEFAULT_CONFIG_PATH, loglevel=logging.INFO):
        logging.basicConfig()
        self._logger = logging.getLogger("auxiclean.managers.config_manager")
        self._logger.setLevel(loglevel)

        self._config = configparser.ConfigParser()
        self._priorities = None
        self._last_excel_file = None
        self._loglevel = None
        self._excel_file_open_warning = None
        # For now, this file is only at one place possible.
        if os.path.exists(path):
            self._logger.info("Loading config from %s" % path)
            self.load_config(path)
        else:
            self._logger.info("Setting config for first time.")
            self.setdefaults()
            self.write_config(path)

    @property
    def priorities(self):
        if self._priorities is None:
            raise ValueError("Priorities not loaded...")
        return self._priorities

    @priorities.setter
    def priorities(self, value):
        if isinstance(value, str):
            value = tuple(eval(value))  # convert string tuple to real tuple
        # check that all the priorities are in the default list
        for v in value:
            if v not in PRIORITY_PARAMS:
                raise NonValidPriority("%s not a valid priority." % v)
        # check that all priorities are there
        for v in PRIORITY_PARAMS:
            if v not in value:
                raise MissingPriority("%s should be set as a priority." % v)
        # check that every priority is unique
        uniques = []
        for v in value:
            if v not in uniques:
                uniques.append(v)
            else:
                raise NonUniquePriority("%s appears multiple times." % v)
        self._priorities = tuple(value)

    @property
    def excel_file_open_warning(self):
        if self._excel_file_warning is None:
            raise ValueError("Excel File warning not loaded.")
        return self._excel_file_warning

    @excel_file_open_warning.setter
    def excel_file_open_warning(self, value):
        if isinstance(value, str):
            value = eval(value)
        if not isinstance(value, bool):
            raise TypeError("excel file warning should be a boolean.")
        self._excel_file_warning = value

    @property
    def loglevel(self):
        if self._loglevel is None:
            raise ValueError("Loglevel not loaded")
        return self._loglevel

    @loglevel.setter
    def loglevel(self, value):
        self._loglevel = int(value)

    @property
    def last_excel_file(self):
        if self._last_excel_file is None:
            raise ValueError("Last excel file not loaded.")
        return self._last_excel_file

    @last_excel_file.setter
    def last_excel_file(self, value):
        self._last_excel_file = value

    def load_config(self, path=DEFAULT_CONFIG_PATH):
        self._config.read(path)
        write_new_config = False
        for param in PARAMETERS:
            try:
                setattr(self, param, self._config["PARAMETERS"][param])
            except (KeyError, MissingPriority):
                # there is a missing parameter in config file => set default
                # or missing priority (changing to a new version)
                self._logger.error("Missing parameter in config file : %s" %
                                   param)
                self._logger.error("Setting to default.")
                st = str(DEFAULT_PARAMETERS[param])
                self._config["PARAMETERS"][param] = st
                setattr(self, param, self._config["PARAMETERS"][param])
                write_new_config = True
        if write_new_config:
            self.write_config(path=path)

    def setdefaults(self):
        self._logger.info("Setting default parameters.")
        for param, value in DEFAULT_PARAMETERS.items():
            self._logger.debug("Setting %s as %s" % (param, str(value)))
            setattr(self, param, value)

    def write_config(self, path=DEFAULT_CONFIG_PATH):
        self._logger.debug("Prepare to write config file.")
        params = {}
        for param in PARAMETERS:
            toset = str(getattr(self, param))
            self._logger.debug("Saving %s as %s" % (param, toset))
            params[param] = toset
        self._config["PARAMETERS"] = params
        with open(path, "w") as configfile:
            self._logger.info("Writing config at %s" % path)
            self._config.write(configfile)
