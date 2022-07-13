import nbformat

from common_nb_preprocessors.metadata_injector import (
    GlobalMetaDataInjectorPreprocessor,
    MetaDataListInjectorPreprocessor,
    MetaDataMapInjectorPreprocessor,
)

# TODO: Test GlobalMetaDataInjectorPreprocessor


def _make_tiny_nb():
    nb = nbformat.v4.new_notebook()
    nb.cells.append(nbformat.v4.new_code_cell("# hide\nimport os"))
    nb.cells.append(nbformat.v4.new_markdown_cell("# This is the actual title"))
    return nb


def test_metadata_injector():
    nb = _make_tiny_nb()
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

    nb = _make_tiny_nb()
    nb, _ = MetaDataListInjectorPreprocessor(
        strings=("hide",), prefix="#", remove_line=False
    ).preprocess(nb, None)
    assert nb.cells[0]["source"] == "# hide\nimport os"
    assert nb.cells[0]["metadata"]["tags"][0] == "hide"


def test_metadata_map_injector():
    nb = _make_tiny_nb()
    nb.cells.append(nbformat.v4.new_code_cell("# hide=true\nimport lib"))
    keys = ["hide"]
    nb, _ = MetaDataMapInjectorPreprocessor(
        keys=keys,
        prefix="#",
        metadata_group="mystnb",
        delimiter=r"=",
        remove_line=True,
    ).preprocess(nb, None)
    assert nb.cells[-1]["source"] == "import lib"
    injected_map = nb.cells[-1]["metadata"]["mystnb"]
    assert isinstance(injected_map, dict)
    assert list(injected_map.keys()) == keys
    assert injected_map[keys[0]] == "true"
