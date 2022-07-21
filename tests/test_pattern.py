import hypothesis.strategies as st
import pytest
from hypothesis import given, settings
from pydantic import ValidationError

from common_nb_preprocessors._patterns import (
    build_prefixed_regex_pattern,
    build_prefixed_regex_pattern_with_value,
)

allowed_pattern_st = st.text(
    alphabet=st.characters(
        blacklist_categories=("C", "Z"), blacklist_characters=("\n", "\r")
    ),
    min_size=1,
)
spacer_str = st.characters(whitelist_categories=("Z",), blacklist_characters=("\n"))


@given(
    spacer_str,
    allowed_pattern_st,
    spacer_str,
    allowed_pattern_st,
)
@settings(max_examples=250)
def test_metadata_list_injector_parsing(prefix_spacer, prefix, spacer, key_term):
    text = f"{prefix_spacer}{prefix}{spacer}{key_term}"
    pattern = build_prefixed_regex_pattern(prefix=prefix, key_term=key_term)
    assert pattern.search(text).group("key") == key_term


def test_pattern_builder():
    pattern = build_prefixed_regex_pattern(prefix="#", key_term="hide")
    assert "hide" == pattern.search("#hide").group("key")
    assert "hide" == pattern.search("# hide").group("key")
    assert "hide" == pattern.search("#  hide").group("key")


@pytest.mark.parametrize("invalid_kwargs", [{"prefix": ""}, {"key_term": ""}])
def test_prefixed_regex_pattern_invalid_inp(invalid_kwargs):
    with pytest.raises(ValidationError):
        build_prefixed_regex_pattern(**invalid_kwargs)


@given(
    allowed_pattern_st,
    spacer_str,
    allowed_pattern_st,
    allowed_pattern_st,
    allowed_pattern_st,
)
@settings(max_examples=250)
def test_metadata_map_injector_parsing(prefix, spacer, key_term, delimiter, value_term):
    text = f"{prefix}{spacer}{key_term}{delimiter}{value_term}"
    pattern = build_prefixed_regex_pattern_with_value(
        prefix=prefix, key_term=key_term, delimiter=delimiter
    )
    assert pattern.search(text).group("key") == key_term
    assert pattern.search(text).group("value") == value_term


@pytest.mark.parametrize(
    "text",
    [
        "# default_exp=export_name",
        "# default_exp= export_name",
        "# default_exp =export_name",
        "# default_exp\t= export_name",
        "#default_exp=export_name",
        "#\tdefault_exp=export_name",
    ],
)
def test_pattern_with_value_builder_whitespace_handling(text):
    pattern2 = build_prefixed_regex_pattern_with_value(
        prefix="#",
        key_term="default_exp",
        delimiter="=",
    )
    assert "default_exp" == pattern2.search(text).group("key")
    assert "export_name" == pattern2.search(text).group("value")


@pytest.mark.parametrize(
    "delimiter,text",
    [
        ("=", "# hide=true"),
        ("=", "# hide = true"),
        ("=", "# hide\t=\ttrue"),
        ("/ ", "# hide/ true"),
        (" ", "# hide true"),
        ("==", "# hide==true"),
        ("_-_", "# hide_-_true"),
        ("\\", r"# hide \ true"),
    ],
)
def test_pattern_with_value_delimiter_handling(delimiter, text):
    pattern = build_prefixed_regex_pattern_with_value(
        prefix="#", key_term="hide", delimiter=delimiter
    )
    assert "hide" == pattern.search(text).group("key")
    assert "true" == pattern.search(text).group("value")


# If I am bored, I could rewrite these with hypothesis
@pytest.mark.parametrize("delimiter", ["="])
# hide will always be key_term!
@pytest.mark.parametrize(
    "inp_key_text,matched_key",
    [
        ("hide", "hide"),
        ("hide ", "hide"),
        ("hide.", "hide."),
        ("hide. ", "hide."),
        ("hide.two", "hide.two"),
        ("hide.two ", "hide.two"),
    ],
)
def test_pattern_with_value_key_expansion(delimiter, inp_key_text, matched_key):
    prefix = "#"
    key = "hide"
    value = "true"
    text = f"{prefix} {inp_key_text}{delimiter}{value}"
    pattern = build_prefixed_regex_pattern_with_value(
        prefix=prefix, key_term=key, delimiter=delimiter, expand_key_term=True
    )
    assert matched_key == pattern.search(text).group("key")
    assert "true" == pattern.search(text).group("value")


@pytest.mark.parametrize(
    "invalid_kwargs", [{"prefix": ""}, {"key_term": ""}, {"delimiter": ""}]
)
def test_pattern_with_value_invalid_inp(invalid_kwargs):
    with pytest.raises(ValidationError):
        build_prefixed_regex_pattern_with_value(**invalid_kwargs)


def test_pattern_with_value_newline_matching():
    pattern = build_prefixed_regex_pattern_with_value(
        prefix="#", key_term="hide", delimiter="="
    )
    assert "import lib" == pattern.sub("", "# hide=true\nimport lib")
    assert "import lib" == pattern.sub("", "# hide=true\n\nimport lib")
