import re
import sys

from pydantic import Field, validate_arguments

__all__ = ["build_prefixed_regex_pattern", "build_prefixed_regex_pattern_with_value"]

# Package only support >= 3.8
if sys.version_info[:2] == (3, 8):
    from typing import Pattern
else:
    from re import Pattern


@validate_arguments
def build_prefixed_regex_pattern(
    *,
    prefix: str = Field(..., min_length=1),
    key_term: str = Field(..., min_length=1),
) -> Pattern[str]:
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


@validate_arguments
def build_prefixed_regex_pattern_with_value(
    *,
    prefix: str = Field(..., min_length=1),
    key_term: str = Field(..., min_length=1),
    delimiter: str = Field("=", min_length=1),
    expand_key_term: bool = False,
) -> Pattern[str]:
    """
    A regular expression builder that returns a compiled
    regular expression that matches a string with:
    - The (escaped) `prefix` string (may have whitespaces before or after)
    - The (escaped) `key_term` to capture with the group name `key`
        - If `expand_key_term` is set, the `key_term` will be seen as a *key-prefix*
            and the matched key will be lazily expanded.
    - Followed by an (escaped) `delimiter` (may have whitespaces before or after)
    - and captures the following line until the end of the line with the group name `value`
    """
    prefix = re.escape(prefix)
    key_term = re.escape(key_term)
    delimiter = re.escape(delimiter)
    key_expansion_suffix = ".*?" if expand_key_term else ""
    pattern = re.compile(
        rf"""
        ^ # match start of each line
        \s*{prefix}\s* # allow whitespace before and after prefix
        (?P<key>{key_term}{key_expansion_suffix}) # term to capture
        \s*{delimiter}\s* # allow whitespace before and after delimiter
        (?P<value>[^\n\r]+)
        $ # match end of each line (excludes \n in MULTILINE)
        [\r\n]* # Capture current and all following empty newlines
        """,
        re.VERBOSE | re.MULTILINE,
    )
    return pattern
