# -*- coding: utf-8 -*-
"""Module for managing a configuration INI file."""
__version__ = '0.5.0'
__status__ = 'Beta'
__author__ = 'Libor Gabaj'
__copyright__ = 'Copyright 2018-2020, ' + __author__
__credits__ = []
__license__ = 'MIT'
__maintainer__ = __author__
__email__ = 'libor.gabaj@gmail.com'


import logging
try:
    import configparser
except ModuleNotFoundError:
    from six.moves import configparser
from typing import List


###############################################################################
# Classes
###############################################################################
class Config():
    """Create a manager for a configuration INI file.

    Arguments
    ---------
    file : string | pointer
        Full path to a configuration file or file pointer of already opened
        file.

    Notes
    -----
    - A single class instance object manages just one configuration file.
    - If more configuration files are needed to manage, separate instances
      should be created.

    """

    def __init__(self, file):
        """Create the class instance - constructor."""
        self._parser = configparser.ConfigParser()
        self._file = None
        if isinstance(file, str):
            self._file = file
            self._parser.read(file)
        else:
            self._parser.read_file(file)
            self._file = file.name
        # Logging
        log = f'Instance of "{self.__class__.__name__}" created: {self}'
        self._logger = logging.getLogger(' '.join([__name__, __version__]))
        self._logger.debug(log)

    def __str__(self) -> str:
        """Represent instance object as a string."""
        log = \
            f'ConfigFile(' \
            f'{self.configfile})'
        return log

    def __repr__(self) -> str:
        """Represent instance object officially."""
        log = \
            f'{self.__class__.__name__}(' \
            f'file={repr(self.configfile)})'
        return log

    @property
    def configfile(self):
        """Configuration INI file."""
        return self._file

    def option(self, option: str, section: str, default: str = None) -> str:
        """Read configuration option's value.

        Arguments
        ---------
        option
            Configuration file option to be read.
            *The argument is mandatory and has no default value.*
        section
            Configuration file section where to search the option.
            *The argument is mandatory and has no default value.*
        default
            Default option value, if configuration file has neither
            the option nor the section.

        Returns
        -------
        Configuration option value or default one.

        """
        if not self._parser.has_option(section, option):
            return default
        return self._parser.get(section, option) or default

    def option_split(self,
                     option: str,
                     section: str,
                     appendix: List[str] = None,
                     separator: str = ',') -> List[str]:
        """Read configuration option, append to it, and split its value.

        Arguments
        ---------
        option
            Configuration file option to be read.
            *The argument is mandatory and has no default value.*
        section
            Configuration file section where to search the option.
            *The argument is mandatory and has no default value.*
        appendix
            List of additonal option value parts that should be added
            to the read option for splitting purposes.
        separator
            String used as a separator for spliting the option. It is used
            for glueing appendix list members with read option and at the same
            time for splitting the entire, composed option value.

        Returns
        -------
        List of a configuration option parts.

        """
        # Read option
        value = self.option(option, section)
        if value is None:
            return value
        # Append list to option
        separator = str(separator or '')
        if not isinstance(appendix, list):
            tmp = appendix
            appendix = []
            appendix.append(tmp)
        for suffix in appendix:
            value += separator + str(suffix)
        # Split, sanitize and list option parts
        result = []
        if separator:
            for part in value.split(separator):
                result.append(part.strip())
        else:
            result.append(value)
        return result

    def options(self, section: str) -> List[str]:
        """Read list of options in a section.

        Arguments
        ---------
        section
            Configuration section to be read from.
            *The argument is mandatory and has no default value.*

        Returns
        -------
        List of configuration option names.

        """
        options = []
        for config_key in self._parser.options(section):
            if config_key in self._parser.defaults():
                continue
            options.append(config_key)
        return options
