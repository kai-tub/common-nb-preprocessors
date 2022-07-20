from enum import Enum

import nbformat

from .metadata_injector import (
    MetaDataListInjectorPreprocessor,
    MetaDataMapInjectorPreprocessor,
)

__all__ = [
    "MystNBCellTags",
    "MystNBCellConf",
    "myst_nb_metadata_injector",
]


class MystNBCellTags(str, Enum):
    """
    All different Myst-NB cell tag configuration options.
    """

    remove_input = "remove-input"
    """
    Removes the source code of the cell.
    See :ref:`sec/remove-input` for a visual example.
    """
    remove_stderr = "remove-stderr"
    """
    Only remove the standard error output of the code cell.
    See :ref:`sec/remove-stderr` for a visual example.
    """
    remove_output = "remove-output"
    """
    Remove the output of the code cell.
    See :ref:`sec/remove-output` for a visual example.
    """
    remove_cell = "remove-cell"
    """
    Remove the input as well as the output of the code cell.
    See :ref:`sec/remove-cell` for a visual example.
    """
    raises_exception = "raises-exception"
    """
    Continue execution normally if code cell raises exception.
    See :ref:`sec/raises-exception` for a visual example.
    """
    skip_execution = "skip-execution"
    """
    Do not execute code cell.
    See :ref:`sec/skip-execution` for a visual example.
    """

    def __str__(self) -> str:
        return self.value

    @classmethod
    def _validate(cls) -> None:
        """
        Internal use only!
        Requires the development dependency pandas with
        the html-dependencies.
        Will parse the values from the website and check them
        with the values from the current file.
        If they aren't identical, a RuntimeError will be raised.
        """
        from ._constant_builder import _read_unique_myst_nb_table

        _myst_nb_cell_tags = _read_unique_myst_nb_table(match="remove-cell")
        cell_tags = _myst_nb_cell_tags["Tag"].tolist()
        _nbclient_cell_tags = _read_unique_myst_nb_table(match="skip-execution")
        cell_tags.extend(_nbclient_cell_tags["Tag"].tolist())
        if set(cell_tags) != set(cls):
            raise RuntimeError(f"{cls} out-of-date!")


class MystNBCellConf(str, Enum):
    """
    All different Myst-NB cell metadata configuration options.
    These keys *must* be paired with a value.
    """

    remove_code_source = "remove_code_source"
    """
    Remove the code cell.
    Should be paired with a boolean: `true`/`false`.
    See :ref:`sec/remove_code_source` for a visual example.
    """

    remove_code_outputs = "remove_code_outputs"
    """
    Remove the output of the cell.
    Should be paired with a boolean: `true`/`false`.
    See :ref:`sec/remove_code_outputs` for a visual example.
    """

    number_source_lines = "number_source_lines"
    """
    Add source line numbering to the current cell.
    Should be paired with a boolean: `true`/`false`.
    See :ref:`sec/number_source_lines` for a visual example.
    """

    output_stderr = "output_stderr"
    """
    Define the behavior for standard error output.
    Should be paired with one of the following strings:

    - `show`: Show the standard error as a separate output
    - `remove`: Remove the standard error output
    - `remove-warn`: Remove the standard error output but log a warning to Sphinx
    - `warn`/`error`/`severe`: Log the error with a specific logging level to Sphinx

    See :ref:`sec/output_stderr` for a visual example.
    """

    merge_streams = "merge_streams"
    """
    Merge standard output and standard error into a single output cell.
    Should be paired with a boolean: `true`/`false`.

    See :ref:`sec/merge_streams` for a visual example.
    """

    text_lexer = "text_lexer"
    """
    Pygments lexer applied to standard out, standard error and text/plain outputs.
    Should be paired with a Pygments lexer string.

    See :ref:`sec/text_lexer` for a visual example.
    """

    error_lexer = "error_lexer"
    """
    Pygments lexer applied to the error/traceback outputs.
    Should be paired with a Pygments lexer string.

    See :ref:`sec/error_lexer` for a visual example.
    """

    markdown_format = "markdown_format"
    """
    The format to use for text/markdown rendering.
    Should be paired with one of the following strings:

    - `commonmark` (Default)
    - `gfm`
    - `myst`

    See :ref:`sec/markdown_format` for a visual example.
    """

    image = "image"
    """
    Options for image outputs.


    See :ref:`sec/image` for a visual example.
    """

    figure = "figure"
    """
    Options for figure outputs.
    To see a list of all possible configuration values,
    take a look at the `official figure documentation <https://myst-nb.readthedocs.io/en/latest/render/format_code_cells.html#images-and-figures>`_.

    See :ref:`sec/figure` for a visual example.
    """

    def __str__(self) -> str:
        return self.value

    @classmethod
    def _validate(cls) -> None:
        """
        Internal use only!
        Requires the development dependency pandas with
        the html-dependencies.
        Will parse the values from the website and check them
        with the values from the current file.
        If they aren't identical, a RuntimeError will be raised.
        """
        from ._constant_builder import _read_unique_myst_nb_table

        cell_tags = _read_unique_myst_nb_table("^markdown_format$")["Name"].tolist()
        if set(cell_tags) != set(cls):
            raise RuntimeError(f"{cls} out-of-date!")


# MYST_NB_CELL_CONF = [
#     "merge_streams",
#     "remove_code_source",
#     "remove_code_outputs",
#     "number_source_lines",
#     "output_stderr",
#     "text_lexer",
#     "error_lexer",
#     "image",
#     "figure",
#     "markdown_format",
# ]

# JUPYTER_BOOK_CODE_TAGS = [
#     "full-width",
#     "output_scroll",
#     "margin",
#     "hide-input",
#     "hide-output",
#     "hide-cell",
#     "remove-input",
#     "remove-output",
#     "remove-cell",
#     "raises-exception",
# ]


def myst_nb_metadata_injector(
    file_content: str, prefix: str = "#", remove_line: bool = True, delimiter: str = "="
) -> nbformat.NotebookNode:
    """
    The preprocessor will inject all the MyST-NB specific tags into the
    metadata `tags` and the cell level configuration to the `mystnb` field.
    For an in-depth explanation of the different values, see the
    `cell-config` and the `tag` section of the MyST-NB documentation.

    :param file_content: contents of an `ipynb` file
    :param prefix: Comment symbol that precedes the keys. Defaults to `#`.
    :param remove_line: Set if the metadata comment lines should be removed after injection. Defaults to `True`.

    Internally it calls `MetaDataListInjectorPrepreprocessor` and
    `MetaDataMapInjectorPreprocessor`.
    Refer to those classes for more details.
    """
    nb = nbformat.reads(file_content, as_version=4)
    # could be done in one preprocess step
    nb, _ = MetaDataListInjectorPreprocessor(
        metadata_group="tags",
        strings=list(MystNBCellTags),
        prefix=prefix,
        remove_line=remove_line,
    ).preprocess(nb, None)
    nb, _ = MetaDataMapInjectorPreprocessor(
        metadata_group="mystnb",
        keys=list(MystNBCellConf),
        prefix=prefix,
        remove_line=remove_line,
        delimiter=delimiter,
        value_to_yaml=True,
    ).preprocess(nb, None)
    return nb


# def jupyter_book_metadata_injector(
#     file_content: str, prefix: str = "#", remove_line: bool = True
# ):
#     """
#     The preprocessor will inject all the jupyter-book specific tags into the
#     metadata tags group of the code cells.
#     For extra information about the jupyter-book specific tags, see


#     By default, the `prefix` or `comment` symbol is assumed to be `#`
#     and the line containing the magic comment is removed.

#     Args:
#         file_content (str): contents of an `ipynb` file
#         prefix (str, optional): Comment symbol that preceeds the jupyter-book keys. Defaults to "#".
#         remove_line (bool, optional): Set if the metadata comment lines should be removed after injection. Defaults to True.
#     """
#     inp_nb = nbformat.reads(file_content, as_version=4)
#     nb, _ = MetaDataListInjectorPreprocessor(
#         strings=JUPYTER_BOOK_CODE_TAGS, prefix=prefix, remove_line=remove_line
#     ).preprocess(inp_nb, None)
#     return nb
