from common_nb_preprocessors._patterns import (
    build_prefixed_regex_pattern,
    build_prefixed_regex_pattern_with_value,
)


def test_pattern_builder():
    pattern = build_prefixed_regex_pattern("#", "hide")
    assert "hide" == pattern.search("#hide").group("key")
    assert "hide" == pattern.search("# hide").group("key")
    assert "hide" == pattern.search("#  hide").group("key")

    pattern2 = build_prefixed_regex_pattern_with_value("#", "default_exp")
    assert "default_exp" == pattern2.search("# default_exp export_name").group("key")
    assert "export_name" == pattern2.search("# default_exp export_name").group("value")
    assert "default_exp" == pattern2.search("#default_exp export_name").group("key")
    assert "default_exp" == pattern2.search("#  default_exp export_name").group("key")

    pattern3 = build_prefixed_regex_pattern_with_value("#", "default_exp", "=")
    assert "default_exp" == pattern3.search("# default_exp=export_name").group("key")
    assert "export_name" == pattern3.search("# default_exp=export_name").group("value")
