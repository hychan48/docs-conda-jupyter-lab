# PyTest
import sys
import pytest
import logging as log


# Functions that are not in a class
def fn_defaults_wrapper(b='B', **kwargs):
    d_locals = locals()
    for name_key in ['self']:  # cls, etc.
        if d_locals.get(name_key) is not None:
            d_locals.pop(name_key)
    tmp_kwargs = d_locals.pop("kwargs")
    if tmp_kwargs != {}: d_locals = {**d_locals, **tmp_kwargs}
    log.warning(d_locals)
    return fn_single_function(**d_locals)


def fn_single_function(a='a', b='b'):
    return a + b


@pytest.mark.parametrize("test_input,expected", [
    ((), "ab"),
    (('a',), "ab"),
    (('A',), "Ab"),
])
def test_single_function_multi_tuples(test_input, expected):
    assert fn_single_function(*test_input) == expected


dict_tests = [
    ({}, "ab"),
    (dict(a='a', b='b'), "ab"),
    (dict(a='A', b='b'), "Ab"),
    (dict(a='A'), "Ab"),
]
# no b defined. should be capital. as ooposed to lower cas
dict_tests_defaults = [
    ({}, "aB"),
    (dict(a='a', b='b'), "ab"),
    (dict(a='A', b='b'), "Ab"),
    (dict(a='A'), "AB"),
    # (dict(a='A', b=None), "AB"), # will crash because non
    (dict(a='A'), "AB"), # b is undefined
]


@pytest.mark.parametrize("test_input,expected", dict_tests)
def test_single_function_multi_dict(test_input, expected):
    assert fn_single_function(**test_input) == expected


@pytest.mark.parametrize("test_input,expected", dict_tests_defaults)
def test_fn_defaults_wrapper_multi_dict(test_input, expected):
    assert fn_defaults_wrapper(**test_input) == expected


class TestForLiveTemplate:
    # all i need is to assume kwargs only
    #
    @pytest.mark.parametrize("test_input,expected", dict_tests_defaults)
    def test_fn_defaults_wrapper_multi_dict(self, test_input, expected):
        assert fn_defaults_wrapper(**test_input) == expected


if __name__ == '__main__':
    pytest.main(sys.argv)
