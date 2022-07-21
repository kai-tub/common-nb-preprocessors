import pytest

from common_nb_preprocessors._nested_dict_updater import (
    NestedDictCollectionOverwriteError,
    NestedDictInvalidDictError,
    NestedDictTypeChangeError,
    NestedDictUpdateError,
    nested_dict_updater,
)


@pytest.mark.parametrize(
    "inp_dict,keys,value,out_dict",
    [
        ({}, ["a"], 1, {"a": 1}),
        ({}, ["a"], "1", {"a": "1"}),
        ({}, ["a", "b"], 1, {"a": {"b": 1}}),
        ({}, ["a", "b", "c"], 1, {"a": {"b": {"c": 1}}}),
        ({"a": 1}, ["a"], 2, {"a": 2}),
        ({"a": {"b": {"c": "z"}}}, ["a", "b", "c"], "1", {"a": {"b": {"c": "1"}}}),
        ({"a": 1}, ["b"], 2, {"a": 1, "b": 2}),
        (
            {"a": {"b": 1, "c": 2}, "d": 3},
            ["a", "b"],
            9,
            {"a": {"b": 9, "c": 2}, "d": 3},
        ),
    ],
)
def testnested_dict_updater(inp_dict, keys, value, out_dict):
    # works in-place!
    nested_dict_updater(inp_dict, keys, value)
    assert inp_dict == out_dict


@pytest.mark.parametrize(
    "inp_dict,keys",
    [
        (["not_dict"], ["a"]),
        ({"a": 1}, ["a", "b"]),
        ({"a": {"b": 1}}, ["a", "b", "c"]),
    ],
)
def testnested_dict_updater_invalid_nesting(inp_dict, keys):
    with pytest.raises(NestedDictUpdateError) as exc_info:
        nested_dict_updater(inp_dict.copy(), keys, {"b": 1})
    assert type(exc_info.value.__cause__) == NestedDictInvalidDictError


@pytest.mark.parametrize(
    "inp_dict,keys,value",
    [
        ({"a": {"b": 1}}, ["a"], 1),
        ({"a": {"b": 1}}, ["a", "b"], "1"),
        ({"a": {"b": 1}}, ["a", "b"], [1]),
    ],
)
def testnested_dict_updater_invalid_type_setting(inp_dict, keys, value):
    with pytest.raises(NestedDictUpdateError) as exc_info:
        nested_dict_updater(inp_dict.copy(), keys, value)
    assert type(exc_info.value.__cause__) is NestedDictTypeChangeError


@pytest.mark.parametrize(
    "inp_dict,keys,value",
    [
        ({"a": {"b": 1}}, ["a"], {"b": 2, "c": 1}),
        ({"a": {"b": 1}}, ["a"], {"b": 1}),
        ({"a": [1]}, ["a"], [2]),
        ({"a": {1}}, ["a"], {2}),
    ],
)
def testnested_dict_updater_invalid_collection_setting(inp_dict, keys, value):
    with pytest.raises(NestedDictUpdateError) as exc_info:
        nested_dict_updater(inp_dict.copy(), keys, value)
    assert type(exc_info.value.__cause__) is NestedDictCollectionOverwriteError
