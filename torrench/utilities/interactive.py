from sys import exit as _exit

import torrench.modules.distrowatch as distrowatch
import torrench.modules.kickasstorrent as kat
import torrench.modules.linuxtracker as linuxtracker
import torrench.modules.nyaa as nyaa_module
import torrench.modules.skytorrents as sky
import torrench.modules.thepiratebay as tpb_module
import torrench.modules.xbit as xbit_module
from torrench.utilities.Config import Config


class InteractiveMode:
    """
    This class deals with most of the functionality assigned to the interactive mode.
    It resolves the arguments, parses and calls their respective modules
    :params: None
    """
    def __init__(self):
        self._modules = {}

    def parser(self, query):
        """
        :query: String to query the module.
        """
        _available_modules = self._set_modules().keys()
        if query[:4] in ('!h', 'help'):
            self._interactive_help()
        elif query[:2] in _available_modules:
            self._caller(query[:2], query[3:])
        elif query[:4] in ('!q', 'quit'):
            print("Bye!")
            _exit(2)
        else:
            print('Invalid command! Try `!h` or `help` for help.')

    def _set_modules(self):
        """
        Map functions to commands and return dictionary.
        """
        if Config().file_exists():
            self._modules = {'!t': tpb_module,
                             '!n': nyaa_module,
                             '!k': kat,
                             '!x': xbit_module,
                             '!d': distrowatch,
                             '!l': linuxtracker,
                             '!s': sky
                            }
            return self._modules

        self._modules = {'!d': distrowatch,
                         '!l': linuxtracker
                        }

        return self._modules

    def _caller(self, module, query):
        """
        Send queries to their respective modules.

        :module: Module to use in query.
        :query: String to search for.
        """
        _modules = self._set_modules()
        if query and module in _modules and not query.isspace():
            if module in ['!t', '!k', '!s']:
                _modules[module].main(query, page_limit=1)
            else:
                _modules[module].main(query)
        else:
            print("You called an invalid module or provided an empty query.")

    @staticmethod
    def _interactive_help():
        """
        Display help
        """
        help_text = """
            Available commands:
        !h or help  - Help text (this)
        !n <string> - Search on nyaa.si for anime.
        !t <string> - Search on ThePirateBay.
        !k <string> - Search on KickAssTorrents.
        !s <string> - Search on SkyTorrents
        !x <string> - Search on XBit.pw
        !t <string> - Search on LinuxTorrents
        !q or quit  - Quit interactive mode

        Some commands are only available after a `config.ini` file has been set.
        See the documentation for more information.
        """
        print(help_text)


def inter():
    """
    Execution will start here.
    """
    try:
        i = InteractiveMode()
        while True:
            data = input('torrench > ')
            i.parser(data)
    except (KeyboardInterrupt, EOFError):
        print('Terminated.')

if __name__ == '__main__':
    print("Run torrench -i")
