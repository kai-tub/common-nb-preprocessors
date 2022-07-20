from nbformat.v4 import new_code_cell, new_notebook

from common_nb_preprocessors.keep import TagsKeepPreproccesor


def test_keep():
    nb = new_notebook()
    valid_data = "# keep code cell"
    keep_tag = "keep me"

    nb.cells.append(new_code_cell(valid_data, metadata={"tags": [keep_tag]}))
    nb.cells.append(new_code_cell("# not this one", metadata={"tags": ["empty"]}))

    nb, _ = TagsKeepPreproccesor(tags=[keep_tag]).preprocess(nb, None)
    assert len(nb.cells) == 1
    assert nb.cells[0]["source"] == valid_data


def test_keep2():
    valid_data = "# keep code cell"
    keep_tag = "keep me"
    nb = new_notebook()
    nb.cells.append(new_code_cell(valid_data, metadata={"tags": [keep_tag]}))
    nb.cells.append(new_code_cell("# not this one either"))

    nb, _ = TagsKeepPreproccesor(tags=[keep_tag]).preprocess(nb, None)
    assert nb.cells[0]["source"] == valid_data
    assert len(nb.cells) == 1
