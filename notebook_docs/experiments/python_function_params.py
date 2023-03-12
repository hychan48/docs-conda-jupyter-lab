import logging as log


# originally
# def fn_params_into_dict_round_about(a,b,*args,hi='world',**kwargs):
# maybe make a @dataclass instead of doing this... this is the lazy way
# maybe append remove
def locals_into_dict(d_locals: dict, ignore_keys: list = None, name_kwargs: str = 'kwargs', name_keys: list = None,
                     name_args: str = 'args', ):
    name_keys = ['self', 'cls'] if name_keys is None else name_keys
    ignore_keys = [] if ignore_keys is None else ignore_keys
    if d_locals.get(name_args) == ():
        d_locals.pop(name_args)  # can assume it's not empty, and if passed. don't remove
    for name_key in name_keys: # i think i can combine them with * spreading
        if d_locals.get(name_key): d_locals.pop(name_key)  # empty pop args
    for ignore_key in ignore_keys:
        if d_locals.get(ignore_key): d_locals.pop(ignore_key)  # empty pop args

    if d_locals.get(name_kwargs) is not None:  # delete and spread
        tmp_kwargs = d_locals.pop(name_kwargs)
        if tmp_kwargs != {}: d_locals = {**d_locals, **tmp_kwargs}
    return d_locals
