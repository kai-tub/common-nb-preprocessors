from typing import Dict

import hypothesis.strategies as st
import nbformat
import pytest
from hypothesis import assume, given
from traitlets import TraitError

from common_nb_preprocessors.metadata_injector import (
    MetaDataListInjectorPreprocessor,
    MetaDataMapInjectorPreprocessor,
)


def test_metadata_injector():
    nb = nbformat.v4.new_notebook()
    nb.cells.append(nbformat.v4.new_code_cell("# hide\nimport os"))
    nb.cells.append(nbformat.v4.new_markdown_cell("# This is the actual title"))
    nb, _ = MetaDataListInjectorPreprocessor(strings=("hide",), prefix="#").preprocess(
        nb, None
    )
    assert nb.cells[0]["source"] == "import os"
    assert nb.cells[0]["metadata"]["tags"][0] == "hide"
    # check idempotency
    nb, _ = MetaDataListInjectorPreprocessor(strings=("hide",), prefix="#").preprocess(
        nb, None
    )
    assert nb.cells[0]["metadata"]["tags"][0] == "hide"


@pytest.mark.parametrize(
    "cell_source_inp,cell_source_output,remove_line",
    [
        ("# hide\nimport os", "import os", True),
        ("# hide\nimport os", "# hide\nimport os", False),
    ],
)
def test_metadata_list_injector_remove_line(
    cell_source_inp, cell_source_output, remove_line
):
    strings = ["hide"]
    prefix = "#"
    nb = nbformat.v4.new_notebook()
    nb.cells.append(nbformat.v4.new_code_cell(cell_source_inp))
    nb, _ = MetaDataListInjectorPreprocessor(
        strings=strings, prefix=prefix, remove_line=remove_line
    ).preprocess(nb, None)
    assert nb.cells[0]["source"] == cell_source_output
    # check that parsing works as expected
    assert nb.cells[0]["metadata"]["tags"][0] == "hide"


@pytest.mark.parametrize(
    "inp_kwargs",
    [
        {"metadata_group": ""},
        {"strings": []},
    ],
)
def test_metadata_injector_empty_inp(inp_kwargs: Dict):
    nb = nbformat.v4.new_notebook()
    inp_kwargs.setdefault("strings", ["a"])
    with pytest.raises(TraitError):
        nb, _ = MetaDataListInjectorPreprocessor(**inp_kwargs).preprocess(nb, None)


@pytest.mark.parametrize(
    "cell_source_inp,cell_source_output,remove_line",
    [
        ("# hide=true\nimport os", "import os", True),
        ("# hide=true\nimport os", "# hide=true\nimport os", False),
    ],
)
def test_metadata_map_injector_remove_line(
    cell_source_inp, cell_source_output, remove_line
):
    keys = ["hide"]
    prefix = "#"
    delimiter = "="
    metadata_group = "mystnb"
    nb = nbformat.v4.new_notebook()
    nb.cells.append(nbformat.v4.new_code_cell(cell_source_inp))
    nb, _ = MetaDataMapInjectorPreprocessor(
        keys=keys,
        prefix=prefix,
        remove_line=remove_line,
        delimiter=delimiter,
        metadata_group=metadata_group,
    ).preprocess(nb, None)
    assert nb.cells[0]["source"] == cell_source_output
    # check that parsing works as expected
    assert nb.cells[0]["metadata"][metadata_group] == {"hide": "true"}


@pytest.mark.parametrize(
    "delimiter,cell_comment",
    [
        ("=", "# hide=true"),
        ("\\", r"# hide \ true"),
    ],
)
def test_metadata_map_injector_delimiter(delimiter, cell_comment):
    keys = ["hide"]
    prefix = "#"
    metadata_group = "mystnb"
    code_cell_text = f"{cell_comment}\nimport lib"
    nb = nbformat.v4.new_notebook()
    nb.cells.append(nbformat.v4.new_code_cell(code_cell_text))
    nb, _ = MetaDataMapInjectorPreprocessor(
        keys=keys,
        prefix=prefix,
        metadata_group=metadata_group,
        delimiter=delimiter,
        remove_line=True,
    ).preprocess(nb, None)
    injected_map = nb.cells[-1]["metadata"]["mystnb"]
    assert list(injected_map.keys()) == keys
    assert injected_map[keys[0]] == "true"
