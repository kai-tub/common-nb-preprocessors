import re

__all__ = ["build_prefixed_regex_pattern", "build_prefixed_regex_pattern_with_value"]


def build_prefixed_regex_pattern(prefix: str, key_term: str) -> re.Pattern:
    """
    A regular expression builder that returns a compiled
    regular expression that matches a string if:
    - An escaped `prefix` string (may have whitespaces before or after) is followed by
    - The escaped `key_term` to capture with the group name `key`
    - Followed only by whitespace characters and/or the end of the line

    It will also match all the following newlines.
    """
    prefix = re.escape(prefix)
    key_term = re.escape(key_term)
    pattern = re.compile(
        rf"""
        ^ # match start of each line
        \s*{prefix}\s* # allow whitespace before and after prefix
        (?P<key>{key_term}) # term to capture
        \s* # allow any number of whitespaces after command
        $ # match end of each line (excludes \n in MULTILINE)
        [\r\n]* # Capture current and all following empty newlines
        """,
        re.VERBOSE | re.MULTILINE,
    )
    return pattern


def build_prefixed_regex_pattern_with_value(
    prefix: str, key_term: str, delimiter=r"\s*"
) -> re.Pattern:
    """
    A regular expression builder that returns a compiled
    regular expression that matches a string if:
    - An escaped `prefix` string (may have whitespaces before or after)
    - The escape `key_term` to capture with the group name `key`
    - Followed by an *unescaped* `delimiter`
    - and captures the following line until the end of the line with the group name `value`
    """
    prefix = re.escape(prefix)
    key_term = re.escape(key_term)
    pattern = re.compile(
        rf"""
        ^ # match start of each line
        \s*{prefix}\s* # allow whitespace before and after prefix
        (?P<key>{key_term}) # term to capture
        {delimiter}
        (?P<value>[^\n\r]+)
        $ # match end of each line (excludes \n in MULTILINE)
        """,
        re.VERBOSE,
    )
    return pattern
