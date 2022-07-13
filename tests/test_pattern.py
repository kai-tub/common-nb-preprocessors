from common_nb_preprocessors._patterns import (
    build_prefixed_regex_pattern,
    build_prefixed_regex_pattern_with_value,
)

# TODO: Make these real pytests


def test_pattern_builder():
    pattern = build_prefixed_regex_pattern("#", "hide")
    assert "hide" == pattern.search("#hide").group("key")
    assert "hide" == pattern.search("# hide").group("key")
    assert "hide" == pattern.search("#  hide").group("key")


def test_pattern_with_value_builder():
    pattern2 = build_prefixed_regex_pattern_with_value("#", "default_exp")
    assert "default_exp" == pattern2.search("# default_exp export_name").group("key")
    assert "export_name" == pattern2.search("# default_exp export_name").group("value")
    assert "default_exp" == pattern2.search("#default_exp export_name").group("key")
    assert "default_exp" == pattern2.search("#  default_exp export_name").group("key")

    pattern3 = build_prefixed_regex_pattern_with_value("#", "default_exp", "=")
    assert "default_exp" == pattern3.search("# default_exp=export_name").group("key")
    assert "export_name" == pattern3.search("# default_exp=export_name").group("value")

    pattern4 = build_prefixed_regex_pattern_with_value(
        prefix="#", key_term="hide", delimiter="="
    )
    assert "hide" == pattern4.search("# hide=true\nimport lib").group("key")
    assert "true" == pattern4.search("# hide=true\nimport lib").group("value")
    assert "import lib" == pattern4.sub("", "# hide=true\nimport lib")
