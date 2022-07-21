import nbformat
import pytest

from common_nb_preprocessors._nested_dict_updater import NestedDictUpdateError
from common_nb_preprocessors.metadata_injector import (
    MetaDataListInjectorPreprocessor,
    MetaDataMapInjectorPreprocessor,
)


def test_metadata_list_injector():
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


def test_metadata_list_injector_empty_metadata_group():
    with pytest.raises(ValueError, match="non-empty"):
        MetaDataListInjectorPreprocessor(strings=["a"], metadata_group="")


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
        allow_nested_keys=False,
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


def test_metadata_map_injector_multiple_matches():
    code_cell_text = f"# hide = true\n# hide = false\nimport lib"
    nb = nbformat.v4.new_notebook()
    nb.cells.append(nbformat.v4.new_code_cell(code_cell_text))
    nb, _ = MetaDataMapInjectorPreprocessor(
        keys=["hide"],
        prefix="#",
        metadata_group="mystnb",
        delimiter="=",
        remove_line=True,
        allow_nested_keys=False,
    ).preprocess(nb, None)
    injected_map = nb.cells[0]["metadata"]["mystnb"]
    assert list(injected_map.keys()) == ["hide"]
    assert len(nb.cells[0]["source"].splitlines()) == 1
    assert injected_map["hide"] == "false"


@pytest.mark.parametrize(
    "inp_comment, output_val",
    [
        ("hide = true", True),
        ("hide = false", False),
        ("hide = I am a string", "I am a string"),
        ("hide = 42", 42),
    ],
)
def test_metadata_map_injector_multiple_to_yaml(inp_comment, output_val):
    code_cell_text = f"# {inp_comment}\nimport lib"
    nb = nbformat.v4.new_notebook()
    nb.cells.append(nbformat.v4.new_code_cell(code_cell_text))
    nb, _ = MetaDataMapInjectorPreprocessor(
        keys=["hide"],
        prefix="#",
        metadata_group="mystnb",
        delimiter="=",
        remove_line=True,
        allow_nested_keys=False,
        value_to_yaml=True,
    ).preprocess(nb, None)
    injected_map = nb.cells[0]["metadata"]["mystnb"]
    assert list(injected_map.keys()) == ["hide"]
    assert injected_map["hide"] == output_val


def test_metadata_map_injector_multiple_nested_access():
    code_cell_text = f"# hide.nested = true\n# hide.other = false\nimport lib"
    nb = nbformat.v4.new_notebook()
    nb.cells.append(nbformat.v4.new_code_cell(code_cell_text))
    nb, _ = MetaDataMapInjectorPreprocessor(
        keys=["hide"],
        prefix="#",
        metadata_group="mystnb",
        delimiter="=",
        remove_line=True,
        allow_nested_keys=True,
    ).preprocess(nb, None)
    injected_map = nb.cells[0]["metadata"]["mystnb"]
    assert list(injected_map.keys()) == ["hide"]
    assert len(nb.cells[0]["source"].splitlines()) == 1
    assert injected_map["hide"] == {"nested": "true", "other": "false"}


def test_metadata_map_injector_empty_metadata_group():
    nb = nbformat.v4.new_notebook()
    with pytest.raises(ValueError, match="non-empty"):
        nb, _ = MetaDataMapInjectorPreprocessor(
            keys=["a"], metadata_group=""
        ).preprocess(nb, None)


def test_metadata_list_markdown():
    nb = nbformat.v4.new_notebook()
    source = "# a"
    nb.cells.append(
        nbformat.v4.new_markdown_cell(source),
    )
    nb.cells.append(
        nbformat.v4.new_code_cell(source),
    )
    nb, _ = MetaDataListInjectorPreprocessor(strings=["a"], prefix="#").preprocess(
        nb, None
    )
    assert nb.cells[0].source == source
    assert nb.cells[1].source == ""


def test_metadata_map_markdown():
    nb = nbformat.v4.new_notebook()
    source = "# a = true"
    nb.cells.append(
        nbformat.v4.new_markdown_cell(source),
    )
    nb.cells.append(
        nbformat.v4.new_code_cell(source),
    )
    nb, _ = MetaDataMapInjectorPreprocessor(
        keys=["a"],
        prefix="#",
        delimiter="=",
        metadata_group="mystnb",
    ).preprocess(nb, None)
    assert nb.cells[0].source == source
    assert nb.cells[1].source == ""


def test_metadata_list_type_clash():
    nb = nbformat.v4.new_notebook()
    nb.cells.append(
        nbformat.v4.new_code_cell("# a", metadata={"other": "single-value"})
    )
    with pytest.raises(RuntimeError, match="type"):
        nb, _ = MetaDataListInjectorPreprocessor(
            strings=["a"], metadata_group="other"
        ).preprocess(nb, None)


def test_metadata_map_type_clash():
    nb = nbformat.v4.new_notebook()
    nb.cells.append(
        nbformat.v4.new_code_cell("# a=false", metadata={"mystnb": "single-value"})
    )
    with pytest.raises(NestedDictUpdateError):
        nb, _ = MetaDataMapInjectorPreprocessor(
            keys=["a"], metadata_group="mystnb"
        ).preprocess(nb, None)
