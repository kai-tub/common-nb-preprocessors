from common_nb_preprocessors._constant_builder import *
from common_nb_preprocessors.myst_nb import (
    JUPYTER_BOOK_CODE_TAGS,
    MYST_NB_CELL_CONF,
    MYST_NB_CELL_TAGS,
)

# FUTURE: Figure out how to cache the pandas parsing


def test_mystnb_cell_tags_constant():
    assert myst_nb_cell_tags() == MYST_NB_CELL_TAGS


def test_mystnb_cell_conf_constant():
    assert myst_mystgroup_cell_conf() == MYST_NB_CELL_CONF


def test_jupyter_book_constant():
    assert jupyter_book_cell_tags() == JUPYTER_BOOK_CODE_TAGS
