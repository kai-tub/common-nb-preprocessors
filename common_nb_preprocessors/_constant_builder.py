try:
    import pandas
except ImportError:
    raise ImportError(
        "This module is only used during development and requires pandas."
    )
from typing import List


def _read_unique_pd_table(url: str, match: str) -> pandas.DataFrame:
    dfs = pandas.read_html(url, match=match)
    if len(dfs) > 1:
        raise ValueError("Match does not provide a unique table for url: ", url)
    return dfs[0]


def _read_unique_myst_nb_table(match: str) -> pandas.DataFrame:
    return _read_unique_pd_table(
        url="https://myst-nb.readthedocs.io/en/latest/configuration.html", match=match
    )


def _read_unique_jupyter_book_table(match: str) -> pandas.DataFrame:
    return _read_unique_pd_table(
        url="https://jupyterbook.org/en/latest/reference/cheatsheet.html#myst-cheatsheet-code-cell-tags",
        match=match,
    )


def _myst_nb_cell_tags() -> List[str]:
    _myst_nb_cell_tags = _read_unique_myst_nb_table("remove-cell")
    return _myst_nb_cell_tags["Tag"].tolist()


def _nbclient_cell_tags() -> List[str]:
    _nbclient_cell_tags = _read_unique_myst_nb_table("skip-execution")
    return _nbclient_cell_tags["Tag"].tolist()


def myst_nb_cell_tags() -> List[str]:
    """
    Return MyST-NB tags and nbclient tags, as both
    are used within MyST-NB.
    """
    return _myst_nb_cell_tags() + _nbclient_cell_tags()


def jupyter_book_cell_tags() -> List[str]:
    """
    Return Jupyter-Book tags.
    """
    df = _read_unique_jupyter_book_table("hide-input")
    tag_col = df["Tag option"].astype(str).str.strip("'\"")
    return tag_col.tolist()


def myst_mystgroup_cell_conf() -> List[str]:
    return _read_unique_myst_nb_table("^markdown_format$")["Name"].tolist()
