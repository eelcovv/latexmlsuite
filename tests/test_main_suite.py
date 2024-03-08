import pytest

from latexmlsuite.main_suite import check_make_was_clean, main

__author__ = "Eelco van Vliet"
__copyright__ = "Eelco van Vliet"
__license__ = "MIT"


def test_check_make_was_clean():
    """API Tests"""
    clean_example = ["make: Nothing to be done for 'sidn'"]
    assert check_make_was_clean(clean_example)