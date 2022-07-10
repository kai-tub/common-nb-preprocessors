import nbformat

from .metadata_injector import MetaDataInjectorPreprocessor

__all__ = [
    "JUPYTER_BOOK_CODE_TAGS",
    "MYST_NB_CELL_TAGS",
    "MYST_NB_CELL_CONF",
    "jupyter_book_metadata_injector",
    "myst_nb_metadata_injector",
]


MYST_NB_CELL_TAGS = [
    "remove-cell",
    "remove-input",
    "remove-output",
    "remove-stderr",
    "skip-execution",
    "raises-exception",
]

MYST_NB_CELL_CONF = [
    "merge_streams",
    "remove_code_source",
    "remove_code_outputs",
    "number_source_lines",
    "output_stderr",
    "text_lexer",
    "error_lexer",
    "image",
    "figure",
    "markdown_format",
]

JUPYTER_BOOK_CODE_TAGS = [
    "full-width",
    "output_scroll",
    "margin",
    "hide-input",
    "hide-output",
    "hide-cell",
    "remove-input",
    "remove-output",
    "remove-cell",
    "raises-exception",
]


def myst_nb_metadata_injector(
    file_content: str, prefix: str = "#", remove_line: bool = True
):
    """
    The preprocessor will inject all the myst-nb specific tags into the
    metadata `tags` and the cell level configuration to the `mystnb` field.
    For an in-depth explanation of the different values, see the
    `cell-config` and the `tag` section of the MyST-NB documentation.

    By default, the `prefix` or `comment` symbol is assumed to be `#`
    and the line containing the magic comment is removed.

    Args:
        file_content (str): contents of an `ipynb` file
        prefix (str, optional): Comment symbol that preceeds the jupyter-book keys. Defaults to "#".
        remove_line (bool, optional): Set if the metadata comment lines should be removed after injection. Defaults to True.
    """
    nb = nbformat.reads(file_content, as_version=4)
    for metadata_group, magic_strings in (
        ("tags", MYST_NB_CELL_TAGS),
        ("mystnb", MYST_NB_CELL_CONF),
    ):
        nb, _ = MetaDataInjectorPreprocessor(
            metadata_group=metadata_group,
            strings=magic_strings,
            prefix=prefix,
            remove_line=remove_line,
        ).preprocess(nb, None)
    return nb


def jupyter_book_metadata_injector(
    file_content: str, prefix: str = "#", remove_line: bool = True
):
    """
    The preprocessor will inject all the jupyter-book specific tags into the
    metadata tags group of the code cells.
    For extra information about the jupyter-book specific tags, see


    By default, the `prefix` or `comment` symbol is assumed to be `#`
    and the line containing the magic comment is removed.

    Args:
        file_content (str): contents of an `ipynb` file
        prefix (str, optional): Comment symbol that preceeds the jupyter-book keys. Defaults to "#".
        remove_line (bool, optional): Set if the metadata comment lines should be removed after injection. Defaults to True.
    """
    inp_nb = nbformat.reads(file_content, as_version=4)
    nb, _ = MetaDataInjectorPreprocessor(
        strings=JUPYTER_BOOK_CODE_TAGS, prefix=prefix, remove_line=remove_line
    ).preprocess(inp_nb, None)
    return nb
