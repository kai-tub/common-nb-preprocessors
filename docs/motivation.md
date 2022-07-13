# Preprocessors

This library provides a collection of useful [Preprocessors](/nbconvert_library.ipynb#custom-preprocessors) for {external+nbconvert:doc}`nbconvert <index>`:
- [](metadata_injector)
- [](global_metadata_injector)


(metadata_list_injector)=
## MetaDataListInjector
:::{eval-rst}
.. autoclass:: common_nb_preprocessors.metadata_injector.MetaDataListInjectorPreprocessor
    :members:
:::


(global_metadata_injector)=
## Global MetaDataInjector
:::{eval-rst}
.. autoclass:: common_nb_preprocessors.metadata_injector.GlobalMetaDataInjectorPreprocessor
    :members:
:::


Could explain function in more detail.
```python
# from rich import print
import nbformat
nb = nbformat.v4.new_notebook()
print(f"Empty notebook:", nb)
```
