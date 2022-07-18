from common_nb_preprocessors._constant_builder import *
from common_nb_preprocessors.myst_nb import MystNBCellConf, MystNBCellTags

# FUTURE: Figure out how to cache the pandas parsing


def test_mystnb_cell_tags_constant():
    assert set(myst_nb_cell_tags()) == set(str(e) for e in MystNBCellTags)


def test_mystnb_cell_conf_constant():
    assert set(myst_mystgroup_cell_conf()) == set(str(e) for e in MystNBCellConf)
