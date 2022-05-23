"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = latexmlsuite.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This skeleton file can be safely removed if not needed!

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import codecs
import yaml
from pathlib import Path
import path
import subprocess
import logging
import sys

from latexmlsuite import __version__

MODES = ("all", "html", "tex", "clean")
DEFAULT_MAIN = "main"
DEFAULT_MODE = "all"

__author__ = "Eelco van Vliet"
__copyright__ = "Eelco van Vliet"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from latexmlsuite.main_suite import main`,
# when using this Python module as a library.


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Compile your latex project")
    parser.add_argument(
        "--version",
        action="version",
        version="latexmlsuite {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--debug",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    parser.add_argument(
        "--settings_filename", help="Extra input yaml file to pass extra parameters",
        default="rapport_settings.yml"
    )
    parser.add_argument(
        "--test", help="Doe een droge run, dus laat alleen commando's zien",
        action="store_true", default=False
    )
    parser.add_argument(
        "--mode", help="Welke type document wil je maken?",
        choices=MODES, default=DEFAULT_MODE
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


class LatexXMLSuite:
    def __init__(self,
                 main_file_name=None,
                 output_directory=None,
                 output_filename=None,
                 ccn_output_directory=None,
                 makefile_directories=None,
                 mode=None,
                 test=False):

        self.output_filename = output_filename
        self.ccn_output_directory = ccn_output_directory
        self.makefile_directories = makefile_directories
        self.test = test
        if main_file_name is None:
            self.main_file_name = Path("main.tex")
        else:
            self.main_file_name = Path(main_file_name)

        if output_directory is None:
            self.output_dirctory = "out"
        else:
            self.output_dirctory = output_directory

        if mode is None:
            self.mode = "all"
        else:
            self.mode = mode

    def run(self):

        if self.makefile_directories is not None:
            self.launch_makefiles()

        self.launch_latexmk()

    def launch_makefiles(self):

        for makefile_dir in self.makefile_directories:
            cmd = []
            if self.test:
                cmd.append("echo")
            cmd.append("make")
            if self.mode == "clean":
                cmd.append("clean")
            with path.Path(makefile_dir):
                run_command(command=cmd)

    def launch_latexmk(self):

        cmd = []

        main_base = self.main_file_name.stem
        if self.test:
            cmd.append("echo")

        if self.mode == "all":
            _logger.debug("Building pdf with latexmk")

            cmd.append("latexmk")
            cmd.append(f"{main_base}.tex")
            cmd.append("-xelatex")
            cmd.append(f"-output-directory={self.output_dirctory}")
            cmd.append("-shell-escape")

        elif self.mode == "clean":
            cmd.append("latexmk")
            cmd.append("-c")
            cmd.append(f"{main_base}")

        run_command(command=cmd)


def run_command(command):
    print(" ".join(command))
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

    for line in iter(process.stdout.readline, b''):
        print(line.decode().strip())


class Settings:
    def __init__(self, settings_filename=None):
        self.main_name = "main"
        self.mode = "all"
        self.output_filename = None
        self.output_directory = None
        self.ccn_output_directory = None
        self.makefile_directories = None

        if settings_filename is not None:
            self.read_settings_file(settings_filename)

    def read_settings_file(self, settings_filename):
        _logger.info("Reading settings file {}".format(settings_filename))
        with codecs.open(settings_filename, "r", encoding="UTF-8") as stream:
            settings = yaml.load(stream=stream, Loader=yaml.Loader)
        self.main_name = settings.get("main_tex_file", self.main_name)
        out_def = Path(self.main_name).with_suffix(".pdf")
        self.output_filename = settings.get("output_filename", out_def)
        self.output_directory = settings.get("output_directory", "out")
        self.makefile_directories = settings.get("makefile_directories")
        self.ccn_output_directory = settings.get("ccn_output_directory", "ccn")

    def report_settings(self):
        msgf = "{:40s} : {}"
        _logger.info(msgf.format("main_file_name", self.main_name))
        _logger.info(msgf.format("output_file_name", self.output_filename))
        _logger.info(msgf.format("ccn_output_directory", self.ccn_output_directory))
        _logger.info(msgf.format("makefile_directories", self.makefile_directories))


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    settings = Settings(settings_filename=args.settings_filename)
    _logger.info("Start here")
    settings.report_settings()

    suite = LatexXMLSuite(mode=args.mode,
                          test=args.test,
                          output_directory=settings.output_directory,
                          output_filename=settings.output_filename,
                          ccn_output_directory=settings.ccn_output_directory,
                          makefile_directories=settings.makefile_directories
                          )

    suite.run()

    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m latexmlsuite.skeleton 42
    #
    run()
