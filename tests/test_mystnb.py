from typing import List, Union

import nbformat
import pytest

from common_nb_preprocessors.myst_nb import (
    MystNBCellConf,
    MystNBCellTags,
    myst_nb_metadata_injector,
)


@pytest.mark.parametrize("StrEnum", [MystNBCellConf, MystNBCellTags])
def test_cell_conf_enum_str(StrEnum):
    manual_value_str = {str(e.value) for e in StrEnum}
    implicit_value_str = {str(e) for e in StrEnum}
    assert manual_value_str == implicit_value_str


@pytest.mark.parametrize("prefix", ["/", "#", "###"])
@pytest.mark.parametrize("remove_line", [True, False])
@pytest.mark.parametrize("delimiter", ["|", "___"])
def test_myst_nb_metadata_injector(prefix: str, remove_line: bool, delimiter: str):
    tag_inp = tag_value = MystNBCellTags.remove_input
    cell_conf_inp = MystNBCellConf.remove_code_source
    cell_conf_value_inp = "true"
    cell_conf_value_output = True  # parsed as yaml
    nb = nbformat.v4.new_notebook()
    src = f"""\
        {prefix}{tag_inp}
        code line
        {prefix}{cell_conf_inp}{delimiter}{cell_conf_value_inp}
        other code line\
    """
    nb.cells.append(nbformat.v4.new_code_cell(src))
    new_nb = myst_nb_metadata_injector(
        nbformat.writes(nb), prefix=prefix, remove_line=remove_line, delimiter=delimiter
    )
    assert new_nb.cells[0].hasattr("metadata")
    assert new_nb.cells[0].metadata.hasattr("tags")
    assert new_nb.cells[0].metadata.tags == [tag_value]
    assert new_nb.cells[0].metadata.hasattr("mystnb")
    assert new_nb.cells[0].metadata.mystnb == {cell_conf_inp: cell_conf_value_output}
    len_source_lines = len(new_nb.cells[0].source.splitlines())
    if remove_line:
        assert len_source_lines == 2
    else:
        assert len_source_lines == 4


# test extra tags configurator
@pytest.mark.parametrize(
    "inp_tags,extra_tags",
    [
        (["tag_inp1"], None),
        (["tag_inp1", "tag_inp2"], None),
        (["tag_inp1"], ["tag_inp1"]),
        (["tag-inp1", "tag-inp2"], ["tag-inp1", "tag-inp2"]),
    ],
)
def test_myst_nb_metadata_injector_extra_tags(
    inp_tags: List[str], extra_tags: Union[List[str], None]
):
    # assumption: extra_tags always matches inp for all if not None
    nb = nbformat.v4.new_notebook()
    src_tmpl = """\
        # {inp_tag}
        code line
    """
    src_txt = "\n".join(src_tmpl.format(inp_tag=inp_tag) for inp_tag in inp_tags)
    nb.cells.append(nbformat.v4.new_code_cell(src_txt))
    new_nb = myst_nb_metadata_injector(
        nbformat.writes(nb), prefix="#", remove_line=True, extra_tags=extra_tags
    )
    if extra_tags is not None:
        assert new_nb.cells[0].metadata.hasattr("tags")
        assert set(new_nb.cells[0].metadata.tags) == set(extra_tags)
    else:
        assert not new_nb.cells[0].metadata.hasattr("tags")


def test_myst_nb_metadata_injector_syntax_sugar():
    nb = nbformat.v4.new_notebook()
    src = f"""\
        # figure.caption = I am a string
        # figure.caption_before = true
        other code line\
    """
    nb.cells.append(nbformat.v4.new_code_cell(src))
    new_nb = myst_nb_metadata_injector(
        nbformat.writes(nb),
        prefix="#",
        delimiter="=",
        remove_line=True,
    )
    assert new_nb.cells[0].hasattr("metadata")
    assert new_nb.cells[0].metadata.hasattr("mystnb")
    assert new_nb.cells[0].metadata.mystnb == {
        "figure": {"caption": "I am a string", "caption_before": True}
    }
    len_source_lines = len(new_nb.cells[0].source.splitlines())
    assert len_source_lines == 1
