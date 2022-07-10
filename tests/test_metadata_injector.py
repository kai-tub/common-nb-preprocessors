import nbformat

from common_nb_preprocessors.metadata_injector import (
    GlobalMetaDataInjectorPreprocessor,
    MetaDataInjectorPreprocessor,
)

# TODO: Test GlobalMetaDataInjectorPreprocessor


def _make_tiny_nb():
    nb = nbformat.v4.new_notebook()
    nb.cells.append(nbformat.v4.new_code_cell("# hide\nimport os"))
    nb.cells.append(nbformat.v4.new_markdown_cell("# This is the actual title"))
    return nb


def test_metadata_injector():
    nb = _make_tiny_nb()
    nb, _ = MetaDataInjectorPreprocessor(strings=("hide",), prefix="#").preprocess(
        nb, None
    )
    assert nb.cells[0]["source"] == "import os"
    assert nb.cells[0]["metadata"]["tags"][0] == "hide"
    # check idempotency
    nb, _ = MetaDataInjectorPreprocessor(strings=("hide",), prefix="#").preprocess(
        nb, None
    )
    assert nb.cells[0]["metadata"]["tags"][0] == "hide"

    nb = _make_tiny_nb()
    nb, _ = MetaDataInjectorPreprocessor(
        strings=("hide",), prefix="#", remove_line=False
    ).preprocess(nb, None)
    assert nb.cells[0]["source"] == "# hide\nimport os"
    assert nb.cells[0]["metadata"]["tags"][0] == "hide"
