import nbformat
import pytest

from common_nb_preprocessors.metadata_injector import (
    MetaDataListInjectorPreprocessor,
    MetaDataMapInjectorPreprocessor,
    _nested_dict_updater,
    _nested_dict_updater_helper,
)


@pytest.mark.parametrize(
    "inp_dict,keys,value,out_dict",
    [
        ({}, ["a"], 1, {"a": 1}),
        ({}, ["a"], "1", {"a": "1"}),
        ({}, ["a", "b"], 1, {"a": {"b": 1}}),
        ({}, ["a", "b", "c"], 1, {"a": {"b": {"c": 1}}}),
        ({"a": 1}, ["a"], 2, {"a": 2}),
        ({"a": {"b": {"c": "z"}}}, ["a", "b", "c"], "1", {"a": {"b": {"c": "1"}}}),
        ({"a": 1}, ["b"], 2, {"a": 1, "b": 2}),
        (
            {"a": {"b": 1, "c": 2}, "d": 3},
            ["a", "b"],
            9,
            {"a": {"b": 9, "c": 2}, "d": 3},
        ),
    ],
)
def test_nested_dict_updater_helper(inp_dict, keys, value, out_dict):
    # works in-place!
    _nested_dict_updater_helper(inp_dict, keys, value)
    assert inp_dict == out_dict


@pytest.mark.parametrize(
    "inp_dict,keys",
    [
        (["not_dict"], ["a"]),
        ({"a": 1}, ["a", "b"]),
        ({"a": {"b": 1}}, ["a", "b", "c"]),
    ],
)
def test_nested_dict_updater_helper_invalid_nesting(inp_dict, keys):
    with pytest.raises(RuntimeError, match="Won't overwrite .* to set nested key"):
        _nested_dict_updater_helper(inp_dict.copy(), keys, {"b": 1})


@pytest.mark.parametrize(
    "inp_dict,keys,value",
    [
        ({"a": {"b": 1}}, ["a"], 1),
        ({"a": {"b": 1}}, ["a", "b"], "1"),
        ({"a": {"b": 1}}, ["a", "b"], [1]),
    ],
)
def test_nested_dict_updater_helper_invalid_type_setting(inp_dict, keys, value):
    with pytest.raises(TypeError, match="Will not overwrite"):
        _nested_dict_updater_helper(inp_dict.copy(), keys, value)


@pytest.mark.parametrize(
    "inp_dict,keys,value",
    [
        ({"a": {"b": 1}}, ["a"], {"b": 2, "c": 1}),
        ({"a": {"b": 1}}, ["a"], {"b": 1}),
        ({"a": [1]}, ["a"], [2]),
        ({"a": {1}}, ["a"], {2}),
    ],
)
def test_nested_dict_updater_helper_invalid_collection_setting(inp_dict, keys, value):
    with pytest.raises(RuntimeError, match="would overwrite collection"):
        _nested_dict_updater_helper(inp_dict.copy(), keys, value)


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


def test_metadata_list_injector_empty_metadata_group():
    nb = nbformat.v4.new_notebook()
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
    with pytest.raises(RuntimeError, match="Expected a dictionary!"):
        nb, _ = MetaDataMapInjectorPreprocessor(
            keys=["a"], metadata_group="mystnb"
        ).preprocess(nb, None)
