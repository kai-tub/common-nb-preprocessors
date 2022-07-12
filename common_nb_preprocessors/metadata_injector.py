import nbformat
from nbconvert.preprocessors import Preprocessor
from traitlets import Bool, List, Unicode

from ._patterns import (
    build_prefixed_regex_pattern,
    build_prefixed_regex_pattern_with_value,
)

__all__ = [
    "MetaDataInjectorPreprocessor",
    "GlobalMetaDataInjectorPreprocessor",
]


class MetaDataInjectorPreprocessor(Preprocessor):
    """
    Parse all *code* cells and convert the matched `strings` with the
    `prefix` to the `metadata_group`, which is the `tags` list by default.
    These `strings` must be on their own line and only contain the `prefix`
    a `string` from `strings` and whitespace characters.

    With `remove_line=True` (default) the matched line will be removed from
    the output.

    With the `Preprocessor` configured as:

    - `metadata_group="tags"`
    - `strings=["hide"]`
    - `remove_line=True`

    the code cell with the contents:

    .. code-block:: python

        # hide
        import os

    and the following notebook metadata json:

    .. code-block:: json

        {"metadata": {}}

    Will be transformed to the code-cell with the contents:

    .. code-block:: python

        import os

    and the metadata set as:

    .. code-block:: json

        {"metadata": {"tags": ["hide"]}}

    All matched `strings` (also sometimes called *magic* comments)
    will be *appended* to the `metadata_group` list if it already exists.
    """

    metadata_group = Unicode(default_value="tags").tag(config=True)
    """Metadata group into which the matched `strings` will be written."""
    strings = List(Unicode(), default_value=[]).tag(config=True)
    """List of strings (magic comments) that define the text that will be matched and injected into the selected metadata group."""
    prefix = Unicode(default_value="#").tag(config=True)
    """The prefix that indicates the possible start of a magic comment line. Should be comment character of the language."""
    remove_line = Bool(default_value=True).tag(config=True)
    """By default remove the matching line in the code-cell."""

    def _write_tag(self, tag, cell):
        tags = cell.setdefault("metadata", {}).setdefault(self.metadata_group, [])
        if tag not in tags:
            tags.append(tag)
        cell["metadata"][self.metadata_group] = tags
        return cell

    def preprocess_cell(self, cell, resource, index):
        """Inject metadata to code-cell if match is found"""
        if cell["cell_type"] == "markdown":
            return cell, resource
        for string in self.strings:
            pattern = build_prefixed_regex_pattern(self.prefix, string)
            m = pattern.search(cell.source)
            if m is not None:
                tag = m.group("key")
                cell = self._write_tag(tag, cell)
            if self.remove_line:
                cell.source = pattern.sub("", cell.source)
        return cell, resource


class GlobalMetaDataInjectorPreprocessor(Preprocessor):
    """
    Parse all *code* cells and convert the given `prefix`ed `keys`
    and the following *value* to the global `metadata` field.

    To clean up the output, the lines containing any `string` may be removed
    by setting `remove_line=True` (default).

    The provided list of `keys` will be used to access the *global* `metadata` field
    and insert the value that is followed by the `key` in the code cell.
    Note that the global metadata field will be overwritten if multiple cells define the
    field's value.

    ```python
    # publish true
    import os
    ```

    Will be transformed to:

    ```python
    import os
    ```

    where the _notebooks_ cell metadata `publish` field may be created and contain the additional entry `true`.

    To only add a specific value to a metadata field (usually `tags`) look at `MetaDataInjectorPreprocessor`.
    """

    keys = List(Unicode()).tag(config=True)
    prefix = Unicode(default_value="#").tag(config=True)
    delimiter = Unicode(default_value=r"\s*").tag(config=True)

    def preprocess(self, nb, resources):
        if len(self.keys) == 0:
            return nb, resources

        for cell in nb.cells:
            if cell["cell_type"] == "markdown":
                continue
            for key in self.keys:
                pattern = build_prefixed_regex_pattern_with_value(
                    self.prefix, key, delimiter=self.delimiter
                )
                m = pattern.search(cell.source)
                if m is not None:
                    value = m.group("value")
                    nb.setdefault("metadata", {})
                    nb["metadata"][key] = value
        return nb, resources
