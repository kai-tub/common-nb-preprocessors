from typing import Dict, Tuple, Union

import traitlets
from nbconvert.preprocessors import Preprocessor
from nbformat import NotebookNode

__all__ = ["TagsKeepPreprocessor"]


class TagsKeepPreproccesor(Preprocessor):
    """
    Only keep *code* cells that have the given metadata
    """

    tags = traitlets.List(traitlets.Unicode()).tag(config=True)

    def preprocess(
        self, nb: NotebookNode, resources: Union[None, Dict]
    ) -> Tuple[NotebookNode, Union[Dict, None]]:
        nb.cells = [
            cell
            for cell in nb.cells
            if set(self.tags).intersection(
                set(cell.get("metadata", {}).get("tags", []))
            )
            or cell["cell_type"] != "code"
        ]
        return nb, resources
