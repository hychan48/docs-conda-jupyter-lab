# PyTest
import sys
import pytest
import logging as log


def fn_abc(a: str, b: int, c: dict):
    # s_log = ' '.join([a,b,c])
    s_log = ' '.join([a, a, a])
    # s_log = ' '.join([a,b,c]) # does not work. needs cast
    # s_log = ' '.join([a,b,c]) # does not work
    log.warning(s_log)
    # log.warning(f"{a} {str(b)} {str(c)}")
    pass


import logging


def fn_abc_kwargs(a: str, b: int, c: dict, d: list, *args, b_stop: bool = False,
                  options: dict = None, **kwargs):
    defaults = {
        'hello': "there"
    }
    actual = defaults if options is None else {**defaults, **options}
    d_locals = locals()
    # log.warning(str(d_locals))
    d_locals.update(b_stop=True)
    if not b_stop:
        fn_abc_kwargs(**d_locals)
    # WARNING  root:python_function_params.py:15 {'a': 'a', 'b': 1, 'c': {'c': 3}, 'd': [], 'args': ('arg 4', 'arg 5'), 'kwargs': {}}
    # s_log = ' '.join([a,a,a])
    # kwargs.update(**a)
    # fn_locals = locals # need to print to a dict
    #
    # for key in ('a','b','c'): # this works. ok
    #     log.warning(key)
    # kwargs[key] = fn_locals()[key]
    # log.warning(kwargs)
    # log.warning(s_log)


# 1. create function with defaults. and auto-pass them without too much syntax
# probably want to default them as function parameters
# if kwargs (or just always assume) spread it or just pass it again in **
def fn_params_into_dict(a, b, *args, hi='world', **kwargs):
    # a, b are required, args is for placeholder, hi is defaulted as world and can be overwritten
    # kwargs is w/e maybe throw an error if conflicted keys but w/e for now

    d_locals = locals()
    _a, _k = 'args', 'kwargs'  # done right when function is called away for ease of use
    log.warning('input: ' + str(d_locals))
    # pop any you dont want... or just make a for loop to pop
    if not d_locals.get(_a): d_locals.pop(_a)  # empty pop args
    if d_locals.get(_k) is not None:  # delete and spread
        tmp_kwargs = d_locals.pop(_k)
        # if tmp_kwargs:
        # log.warning(tmp_kwargs)
        # log.warning(d_locals)
        if tmp_kwargs: d_locals = {**d_locals, **tmp_kwargs}
    return d_locals


def fn_params_into_dict_round_about(a, b, *args, hi='world', **kwargs):
    # a, b are required, args is for placeholder, hi is defaulted as world and can be overwritten
    # kwargs is w/e maybe throw an error if conflicted keys but w/e for now

    d_locals = locals()  # done right when function is called away for ease of use
    l_items = list(d_locals.items())  # optional delete: unwanted params del a[-1] or del a[2:4]
    t_kwargs = l_items.pop() if l_items[-1][0] == 'kwargs' else dict()
    # maybe just check if empty dict... basically check all that aren't empty...
    log.warning(t_kwargs)
    pass


def test_name():
    # fn_abc('a',1,dict(c=3))
    # fn_abc_kwargs('a',1,dict(c=3),[],False,'arg 0', 'arg 1',b_stop=True)
    fn_abc_kwargs('a', 1, dict(c=3), [], None, 'arg 0', 'arg 1', b_stop=False)
    fn_abc_kwargs('a', 1, dict(c=3), [], None, 'arg 0', 'arg 1', b_stop=False, options=dict(b='b'))
    # overrides hello
    fn_abc_kwargs('a', 1, dict(c=3), [], None, 'arg 0', 'arg 1', b_stop=False, options=dict(hello='b'))


def test_inspect_function():
    # apparently inspect takes heavy resources...
    import inspect
    log.warning(inspect.getfullargspec(fn_abc))


def test_fn_params_into_dict():
    log.warning('output:' + str(fn_params_into_dict('A', 'B')))
    log.warning('output:' + str(fn_params_into_dict('A', 'B', hi='general kenobi')))
    log.warning('output:' + str(fn_params_into_dict('A', 'B', hi='hello there', misc='misc var')))
    log.warning('output:' + str(fn_params_into_dict('A', 'B', 'arg1', 'arg2', hi='hello there', misc='misc var')))


def test_fn_params_into_dict_single():
    log.warning('output:' + str(fn_params_into_dict('A', 'B', hi='hello there', misc='misc var')))


@pytest.mark.parametrize("test_input,expected", [
    ("empty_tuple", False),
    ("empty_dict", False),
    ("empty_list", False),
    ("none_tuple", False),
    ("none_dict", False),
    ("none_list", False),
    ("o_none", False),
    ("some_tuple", True),
    ("some_dict", True),
    ("some_list", True),
    # pytest.param('skip', "skip", marks=pytest.mark.xfail(reason="but why")),
])
def test_empty_py_objs_multi(test_input, expected):
    dict_input = {
        "empty_tuple": (),
        "empty_dict": {},
        "empty_list": [],
        "o_none": None,
        "some_tuple": ('a', 'b'),
        "some_dict": dict(a='A'),
        "some_list": [1, 2, 3],
    }
    assert bool(dict_input.get(test_input)) == expected


from python_function_params import locals_into_dict


def fn_basic(a: str, b: str, c: str):
    return f"{a} {b} {c}"

def fn_args(*args):
    return locals()

@pytest.mark.parametrize("test_input,expected", [
    (['hello','e'], {'args': ('hello', 'e')}),
    (['hello'], {'args': ('hello',)}), # single tuple syntax? tuples are immutable
])
def test_fn_args_multi(test_input, expected):
    assert fn_args(*test_input) == expected
class TestUseCase():

    def test_new(self):
        # d_locals = locals()
        d_locals = {
            "self": "something",
            "cls": "something",
            "args": (),
            "kwargs": {},  # can defn be empty though...
        }
        log.warning('input: ' + str(d_locals))
        out = locals_into_dict(d_locals)
        log.warning(out)

    @pytest.mark.parametrize("test_input,expected", [
        ({
             "self": "something",
             "cls": "something",
             "args": (),
             "kwargs": {},  # can defn be empty though...
         }, {}),
        ({

         }, {}),
        ({
             'a': 'A'
         }, {'a': 'A'}),
        ({
             "self": "something",
             "cls": "something",
             "args": tuple('a'),
             "kwargs": {},  # can defn be empty though...
         }, {}),
        ({
             "self": "something",
             "cls": "something",
             "args": ('a','b'),
             "kwargs": {},  # can defn be empty though...
         }, {}),

    ])
    def test_locals_into_dict_multi(self, test_input, expected):
        log.warning('input: ' + str(test_input))
        out = locals_into_dict(test_input)
        log.warning(out)
        assert locals_into_dict(test_input) == expected


if __name__ == '__main__':
    pytest.main(sys.argv)
