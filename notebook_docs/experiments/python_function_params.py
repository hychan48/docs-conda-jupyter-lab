# PyTest
import sys
import pytest
import logging as log

def fn_abc(a:str,b:int,c:dict):
    # s_log = ' '.join([a,b,c])
    s_log = ' '.join([a,a,a])
    # s_log = ' '.join([a,b,c]) # does not work. needs cast
    # s_log = ' '.join([a,b,c]) # does not work
    log.warning(s_log)
    # log.warning(f"{a} {str(b)} {str(c)}")
    pass
def fn_abc_kwargs(a:str,b:int,c:dict,*args,**kwargs):
    # s_log = ' '.join([a,a,a])
    # kwargs.update(**a)
    fn_locals = locals
    for key in ('a','b','c'): # this works. ok
        log.warning(key)
        log.warning(str(fn_locals()[key]))
        log.warning(str(locals()[key])) # both work so locals is function scope?
        # kwargs[key] = fn_locals()[key]
    # log.warning(kwargs)
    # log.warning(s_log)
def test_name():
    # fn_abc('a',1,dict(c=3))
    fn_abc_kwargs('a',1,dict(c=3))

def test_inspect_function():
    # apparently inspect takes heavy resources...
    import inspect
    log.warning(inspect.getfullargspec(fn_abc))


if __name__ == '__main__':
    pytest.main(sys.argv)
