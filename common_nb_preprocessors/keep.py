from nbconvert.preprocessors import Preprocessor
from traitlets import Set, Unicode

__all__ = ["TagsKeepPreprocessor"]


class TagsKeepPreproccesor(Preprocessor):
    """
    Only keep *code* cells that have the given metadata
    """

    tags = Set(Unicode(), default_value=[]).tag(config=True)

    def preprocess(self, nb, resources):
        nb.cells = [
            cell
            for cell in nb.cells
            if self.tags.intersection(cell.get("metadata", {}).get("tags", []))
            or cell["cell_type"] != "code"
        ]
        return nb, resources
