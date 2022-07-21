from collections.abc import Collection, MutableMapping
from functools import singledispatch
from typing import Any, Dict, List, Union


class NestedDictUpdateError(Exception):
    """Exception raised for errors while setting a nested dict value."""


class NestedDictTypeChangeError(NestedDictUpdateError):
    """Exception raised if setting of nested dict would change the type."""


class NestedDictCollectionOverwriteError(NestedDictUpdateError):
    """Exception raised if setting value of nested dict would overwrite collection."""


class NestedDictInvalidDictError(NestedDictUpdateError):
    """Exception raised if a dictionary is expected but other type is found during traversal."""


@singledispatch
def _nested_dict_updater_helper(d: object, keys: List[str], _value) -> None:
    raise NestedDictInvalidDictError(
        f"Expected a dictionary! Won't overwrite entry {d} to set nested keys {keys}"
    )


@_nested_dict_updater_helper.register
def _(d: MutableMapping, keys: List[str], value) -> None:
    if len(keys) == 1:
        final_key = keys[0]
        # should also check for other 'nested' types => always fail
        # also check if Type changes, if it does, also raise an Exception
        if final_key in d.keys():
            if not isinstance(d[final_key], type(value)):
                raise NestedDictTypeChangeError(
                    f"Will not overwrite value: {value} of type {type(value)} with {d[final_key]} of type: {type(d[final_key])}"
                )
            if isinstance(d[final_key], Collection) and not isinstance(
                d[final_key], str
            ):
                raise NestedDictCollectionOverwriteError(
                    f"Setting the value of entry '{final_key}' with value {value} would overwrite collection: {d[final_key]}"
                    + "\n"
                    + "Overwriting of collections is not allowed, even if the same collection type is used!"
                )
        d[keys[0]] = value
        return
    d = d.setdefault(keys[0], {})
    _nested_dict_updater_helper(d, keys[1:], value)


def nested_dict_updater(d: Union[Dict, Any], keys: List[str], value: Any) -> None:
    """**Inplace** nested dictionary updater."""
    try:
        _nested_dict_updater_helper(d, keys, value)
    except NestedDictUpdateError as e:
        raise NestedDictUpdateError(
            f"Error while setting nested dict {d} with key-nesting {keys} to value {value}"
        ) from e
