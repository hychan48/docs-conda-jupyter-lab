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


def fn_abc_kwargs(a: str, b: int, c: dict, d: list, *args, b_stop: bool = False, **kwargs):
    d_locals = locals()
    log.warning(str(d_locals))
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


def test_name():
    # fn_abc('a',1,dict(c=3))
    # fn_abc_kwargs('a',1,dict(c=3),[],False,'arg 0', 'arg 1',b_stop=True)
    fn_abc_kwargs('a', 1, dict(c=3), [], None, 'arg 0', 'arg 1', b_stop=False)


def test_inspect_function():
    # apparently inspect takes heavy resources...
    import inspect
    log.warning(inspect.getfullargspec(fn_abc))


if __name__ == '__main__':
    pytest.main(sys.argv)
