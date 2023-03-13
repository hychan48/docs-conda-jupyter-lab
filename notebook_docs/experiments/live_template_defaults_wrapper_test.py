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
    def fn_class_single_function(self,a='a', b='b'):
        return a + b

    @pytest.mark.parametrize("test_input,expected", dict_tests_defaults)
    def test_fn_defaults_wrapper_multi_dict(self, test_input, expected):
        def fn_defaults_wrapper_class(b='B', **kwargs):
            d_locals = locals()
            for name_key in ['self','expected']:  # cls, etc.
                if d_locals.get(name_key) is not None:
                    d_locals.pop(name_key)
            tmp_kwargs = d_locals.pop("kwargs")
            if tmp_kwargs != {}: d_locals = {**d_locals, **tmp_kwargs}
            log.warning(d_locals)
            assert self.fn_class_single_function(**d_locals) == expected
        fn_defaults_wrapper_class(**test_input)
    @pytest.mark.parametrize("test_input,expected", dict_tests_defaults)
    def test_fn_defaults_wrapper_multi_dict_test_input(self, test_input, expected):
        d_locals_pass = locals()['test_input']
        log.warning(d_locals_pass.keys())
        # nested is interesting... might cause more problems
        def fn_defaults_wrapper_class(b='B', **kwargs):
            d_locals = locals()
            log.warning(d_locals)
            # d_locals = locals()['d_locals_pass']
            for name_key in ['self']:  # cls, etc.
                if d_locals.get(name_key) is not None:
                    d_locals.pop(name_key)
            tmp_kwargs = d_locals.pop("kwargs")
            if tmp_kwargs != {}: d_locals = {**d_locals, **tmp_kwargs}
            log.warning(d_locals)
            assert self.fn_class_single_function(**d_locals) == expected
        log.warning(d_locals_pass)
        fn_defaults_wrapper_class(**d_locals_pass)



if __name__ == '__main__':
    pytest.main(sys.argv)
