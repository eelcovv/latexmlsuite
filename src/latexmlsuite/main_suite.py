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
import datetime
import glob
import logging
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import path
import yaml

from latexmlsuite import __version__

MODES = ("all", "html", "latex", "clean", "xml", "none")
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
        "--make_exe", help="executable naam om Makefile te runnen. Default 'make'",
        default="make"
    )
    parser.add_argument(
        "--no_make", help="Sla het runnen van de makefiles over",
        action="store_false", default=True, dest="do_make"
    )
    parser.add_argument(
        "--test", help="Doe een droge run, dus laat alleen commando's zien",
        action="store_true", default=False
    )
    parser.add_argument(
        "--include_graphs", help="Plot ook de tabellen en grafieken in de html output",
        action="store_true", default=False
    )
    parser.add_argument(
        "--mode", help="Welke type document wil je maken?",
        choices=MODES, default=DEFAULT_MODE
    )
    parser.add_argument(
        "--no_overwrite", help="Schrijf de schoongemaakte html's naar een nieuwe file",
        action="store_false", default=True, dest="overwrite"
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


def update_target_compared_to_source(source_file: Path, target_file: Path):
    """
    Script om te kijken of een target file geupdated moet worden.

    Een update vindt plaats als target nog niet bestaat, of als target ouder is dan source

    Args:
        source_file: Path of str
            Naam van de bron file
        target_file: Path of str
            Naam van de target file file

    Returns: bool
        vlag als target geupdated moet worden
    """
    source_file = Path(source_file)
    target_file = Path(target_file)
    time0 = datetime.datetime.fromtimestamp(source_file.stat().st_mtime, tz=datetime.timezone.utc)
    update_target = True
    if target_file.exists():
        time1 = datetime.datetime.fromtimestamp(target_file.stat().st_mtime,
                                                tz=datetime.timezone.utc)
        update_target = time1 < time0
    return update_target


def copy_main_for_latexml(tex_input_file: Path, tex_output_file: Path,
                          include_graphics: bool = False):
    # lees de inhoud van main en pas de opties aan om grafieken en tabellen weg te laten
    _logger.debug(f"Reading {tex_input_file}")
    with open(tex_input_file, "r") as in_stream:
        tex_content = in_stream.read()

    _logger.debug(f"Writing {tex_output_file}")

    options = ""
    if not include_graphics:
        options += "nographs,notables,nohyperrefs"
    else:
        options += "nohyperrefs"
    cbsdocs = "]{cbsdocs}"

    tex_content_new = re.sub(cbsdocs, options + cbsdocs, tex_content)
    with open(tex_output_file, "w") as out_stream:
        out_stream.write(tex_content_new)


class LaTeXMLSuite:
    def __init__(self,
                 main_file_name="main",
                 make_exe="make",
                 do_make=True,
                 overwrite=True,
                 bibtex_file=None,
                 output_directory=None,
                 output_directory_html=None,
                 output_filename=None,
                 ccn_output_directory=None,
                 makefile_directories=None,
                 mode=None,
                 test=False,
                 merge_chapters=False,
                 include_graphs=False,
                 ):

        self.output_filename = output_filename
        if ccn_output_directory is not None:
            self.ccn_output_directory = Path(ccn_output_directory)
        else:
            self.ccn_output_directory = Path("ccn")
        self.ccn_html_dir = self.ccn_output_directory / Path("html")
        self.overwrite = overwrite
        self.ccn_tables_dir = self.ccn_output_directory / Path("tables")
        self.ccn_highcharts_dir = self.ccn_output_directory / Path("highcharts")
        self.makefile_directories = makefile_directories
        self.make_exe = make_exe
        self.include_graphs = include_graphs
        self.test = test
        self.do_make = do_make
        if main_file_name is None:
            self.main_file_name = Path("main.tex")
        else:
            self.main_file_name = Path(main_file_name)

        self.bibtex_file = bibtex_file

        if output_directory is None:
            self.output_directory = Path("out")
        else:
            self.output_directory = Path(output_directory)

        if output_directory_html is None:
            self.output_directory_html = Path("out_html")
        else:
            self.output_directory_html = Path(output_directory_html)

        self.xml_refs = None
        self.updated_references = False
        self.merge_chapters = merge_chapters

        if mode is None:
            self.mode = "all"
        else:
            self.mode = mode

    def run(self):

        if self.makefile_directories is not None and self.do_make:
            self.launch_makefiles()

        if self.mode == "none":
            # met none maken we de documenten niet, alleen de make files worden gerund
            return

        if self.mode in ("clean", "latex", "all"):
            self.launch_latexmk()
            if self.mode == "clean":
                self.clean_log()
        if self.mode in ("xml", "all"):
            self.launch_latexmk_for_html()
            self.copy_pdf()
            if self.bibtex_file is not None:
                self.launch_latexml_bibtex()
            self.launch_latexml()
        if self.mode in ("html", "all"):
            self.launch_latexml_post()
            self.rename_and_clean_html()
            self.clean_ccs()

    def clean_ccs(self):

        pattern = f"{self.ccn_html_dir.as_posix()}/*.css"
        css_files = glob.glob(pattern)
        if len(css_files) == 0:
            _logger.debug("No css files found.")
            return

        rm = []
        if self.test:
            rm.append("echo")
        if "win" in sys.platform.lower():
            rm.append("powershell.exe")
            rm.append("Remove-Item")
            rm.append("-recurse")
            rm.append("-force")
            rm.append(pattern)
        else:
            rm.append("rm")
            rm.append("-v")
            for file in css_files:
                rm.append(file)
        run_command(rm)

    def clean_log(self):
        pattern = f"*.css"
        log_files = glob.glob(pattern)
        if len(log_files) == 0:
            _logger.debug("No log files found.")
            return

        rm = []
        if self.test:
            rm.append("echo")
        if "win" in sys.platform.lower():
            rm.append("powershell.exe")
            rm.append("Remove-Item")
            rm.append("-recurse")
            rm.append("-force")
            rm.append(pattern)
        else:
            rm.append("rm")
            rm.append("-v")
            for file in log_files:
                rm.append(file)

        run_command(rm)

    def rename_and_clean_html(self):
        """
        Hernoem alle html files met een prefix
        """
        html_files = glob.glob(f"{self.ccn_html_dir.as_posix()}/*.html")
        for html_file in html_files:
            html = Path(html_file)

            if html.stem.startswith(self.main_file_name.stem):
                continue

            prefix = self.main_file_name.stem
            new_base = "_".join([prefix, html.stem + html.suffix])
            new_html = html.parent / Path(new_base)

            shutil.move(html.as_posix(), new_html.as_posix())

            cleaner = []
            if self.test:
                cleaner.append("echo")

            cleaner.append("htmlcleaner")
            cleaner.append(new_html.as_posix())

            if self.overwrite:
                cleaner.append("--overwrite")

            run_command(command=cleaner)

    def launch_makefiles(self):
        """
        Loop over alle directories die een Makefile bevatten en lanceer het make commando
        """

        for makefile_dir in self.makefile_directories:
            cmd = []
            if self.test:
                cmd.append("echo")
            cmd.append(self.make_exe)
            if self.mode == "clean":
                cmd.append("clean")
            with path.Path(makefile_dir):
                run_command(command=cmd)

    def launch_latexmk_for_html(self):
        """
        Run latexmk voor de tex file in de html output directory
        """
        cmd = []

        if self.test:
            cmd.append("echo")

        out_dir = Path(self.output_directory_html)
        out_dir.mkdir(exist_ok=True)
        main_file = out_dir / Path(self.main_file_name)
        cmd.append("latexmk")
        cmd.append(f"{main_file}")
        cmd.append("-xelatex")
        cmd.append("-shell-escape")
        cmd.append(f"-output-directory={out_dir}")

        # lees de inhoud van main en pas de opties aan om grafieken en tabellen weg te laten
        if update_target_compared_to_source(self.main_file_name, main_file):
            copy_main_for_latexml(tex_input_file=self.main_file_name, tex_output_file=main_file,
                                  include_graphics=self.include_graphs)
        else:
            _logger.debug(f"No update need for {self.main_file_name} compared to {main_file}")

        run_command(command=cmd)

    def copy_pdf(self):
        """
        Kopieer de volledige pdf voor ccn (dus met de plaatjes)
        """
        out_dir = Path(self.output_directory)
        main_file = out_dir / Path(self.main_file_name)

        pdf_file = main_file.with_suffix(".pdf")
        if not pdf_file.exists():
            self.launch_latexmk()
        ccn_pdf = self.ccn_output_directory / Path(self.output_filename)

        update_pdf = update_target_compared_to_source(pdf_file, ccn_pdf)

        if update_pdf:
            shutil.copy2(pdf_file.as_posix(), ccn_pdf.as_posix())
        else:
            _logger.debug(f"No update need for {ccn_pdf} compared to {pdf_file}")

    def launch_latexml_bibtex(self):
        cmd = []

        if self.test:
            cmd.append("echo")

        references = self.bibtex_file
        self.xml_refs = self.output_directory_html / Path(references + ".xml")

        if update_target_compared_to_source(references, self.xml_refs):
            cmd.append("latexml")
            if "win" in sys.platform:
                cmd[-1] += ".bat"
            cmd.append(f"--dest={self.xml_refs.as_posix()}")
            cmd.append(f"--preload=hyperref.sty")
            cmd.append(f"{references}")

            run_command(command=cmd)
            self.updated_references = True
        else:
            _logger.debug(f"No update need for {self.xml_refs} compared to {references}")
            self.updated_references = False

    def launch_latexml(self):
        cmd = []

        if self.test:
            cmd.append("echo")

        cmd.append("latexml")
        if "win" in sys.platform:
            cmd[-1] += ".bat"

        out_dir = Path(self.output_directory_html)
        main_file = out_dir / Path(self.main_file_name)
        xml_file = main_file.with_suffix(".xml")

        cmd.append(f"--dest={xml_file.as_posix()}")
        cmd.append(f"{main_file.as_posix()}")

        if update_target_compared_to_source(main_file, xml_file) or self.updated_references:
            run_command(command=cmd)
        else:
            _logger.debug(f"No update need for {xml_file} compared to {main_file}")

    def launch_latexml_post(self):
        cmd = []

        if self.test:
            cmd.append("echo")

        cmd.append("latexmlpost")
        if "win" in sys.platform:
            cmd[-1] += ".bat"

        out_dir = self.output_directory_html
        main_file = out_dir / Path(self.main_file_name)
        html_file = self.ccn_html_dir / Path(main_file.stem).with_suffix(".html")
        self.ccn_html_dir.mkdir(exist_ok=True, parents=True)
        xml_file = main_file.with_suffix("")

        cmd.append(f"--dest={html_file.as_posix()}")
        cmd.append(f"{xml_file}")

        if self.xml_refs is not None:
            cmd.append(f"--bibliography={self.xml_refs.as_posix()}")

        if not self.merge_chapters:
            cmd.append("--split")
            cmd.append("--splitat")
            cmd.append("chapter")

        run_command(command=cmd)

    def launch_latexmk(self):

        cmd = []

        main_base = self.main_file_name.stem
        if self.test:
            cmd.append("echo")

        cmd.append("latexmk")
        cmd.append(f"-output-directory={self.output_directory.as_posix()}")

        if self.mode in ("latex", "all"):
            cmd.append(f"{main_base}.tex")
            cmd.append("-xelatex")
            cmd.append("-shell-escape")

        elif self.mode == "clean":
            cmd.append("-c")
        else:
            raise AssertionError("Alleen aanroepen voor all en clean")

        run_command(command=cmd)


def run_command(command, shell=False):
    if command[0] != "echo":
        print(" ".join(command))
    try:
        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   env=os.environ,
                                   shell=shell)

    except FileNotFoundError as err:
        _logger.warning(f"Failed for '{command}' with error:\n{err}")
    else:
        for line in iter(process.stdout.readline, b''):
            print(line.decode().strip())


class Settings:
    def __init__(self, settings_filename=None):
        self.main_name = "main"
        self.bibtex_file = None
        self.mode = "all"
        self.output_filename = None
        self.ccn_output_directory = None
        self.makefile_directories = None
        self.output_directory = None
        self.output_directory_html = None

        if settings_filename is not None:
            self.read_settings_file(settings_filename)

    def read_settings_file(self, settings_filename):
        _logger.debug("Reading settings file {}".format(settings_filename))
        with codecs.open(settings_filename, "r", encoding="UTF-8") as stream:
            settings = yaml.load(stream=stream, Loader=yaml.Loader)
        general_settings = settings["general"]
        cache_settings = settings["cache"]
        self.main_name = general_settings.get("latex_main", self.main_name)
        self.bibtex_file = general_settings.get("bibtex_file", self.main_name)
        self.ccn_output_directory = general_settings.get("ccn_output_directory", "ccn")
        self.makefile_directories = settings.get("makefiles")
        out_def = Path(self.main_name).with_suffix(".pdf")
        self.output_filename = general_settings.get("output_filename", out_def)
        if cache_settings is not None:
            self.output_directory = cache_settings.get("output_directory", "out")
            self.output_directory_html = cache_settings.get("output_directory_html", "out_html")
        else:
            self.output_directory = "out"
            self.output_directory_html = "out_html"

    def report_settings(self):
        msgf = "{:40s} : {}"
        _logger.debug(msgf.format("main_file_name", self.main_name))
        _logger.debug(msgf.format("output_file_name", self.output_filename))
        _logger.debug(msgf.format("ccn_output_directory", self.ccn_output_directory))
        _logger.debug(msgf.format("makefile_directories", self.makefile_directories))


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
    _logger.debug("Start here")
    settings.report_settings()

    suite = LaTeXMLSuite(mode=args.mode,
                         test=args.test,
                         make_exe=args.make_exe,
                         do_make=args.do_make,
                         overwrite=args.overwrite,
                         main_file_name=settings.main_name,
                         bibtex_file=settings.bibtex_file,
                         output_directory=settings.output_directory,
                         output_directory_html=settings.output_directory_html,
                         output_filename=settings.output_filename,
                         ccn_output_directory=settings.ccn_output_directory,
                         makefile_directories=settings.makefile_directories,
                         include_graphs=args.include_graphs,
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
