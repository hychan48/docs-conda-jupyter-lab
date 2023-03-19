import re
import logging as log
from treelib import Tree


def dump_str_to_tree(input_str: str, delim: str = ' ', delim_count: int = 2):
    """
    https://treelib.readthedocs.io/en/latest/

    damn.. useless. because it sorted
    :param input_str:
    :param delim:
    :param delim_count:
    :return:
    """
    # delim: str = ' '  # space or tab
    # delim_count: int = 2
    split_delim = delim
    for i in range(1, 2):
        split_delim = split_delim + delim

    assert len(split_delim) == delim_count
    tree = Tree()
    lines = input_str.split('\n')

    lazy_tree_dict_spaces_to_key: dict = dict()

    # get rid of prepended spaces
    line = lines.pop(0)
    while re.match(r"^\s*$", line):
        line = lines.pop(0)
    # # Get / initialize root
    re_matched = re.match(fr"^(\s*)(\S.*)", line)
    if re_matched:
        spaces_in_front = re_matched.group(1)  # None i guess
        num_of_spaces = len(spaces_in_front.split(split_delim)) - 1
        value = re_matched.group(2)
        tree.create_node(value, value)  # value is key for 0
        lazy_tree_dict_spaces_to_key[0] = value  # i guess i can use value, 0

    for line in lines:
        if re.match(r"^\s*$", line):  # any one space
            continue
        # count number of spaces infront of first letter
        # re_matched = re.match(r"^( *)(\S.*)",line)
        re_matched = re.match(fr"^(\s*)(\S.*)", line)
        if re_matched:
            spaces_in_front = re_matched.group(1)  # None i guess
            num_of_spaces = len(spaces_in_front.split(split_delim)) - 1
            value = re_matched.group(2)
            # the last part is not - 1, but subtract until closest number. / largest but w/e for now
            tree.create_node(value, value, parent=lazy_tree_dict_spaces_to_key[num_of_spaces - 1])  # value is key for 0
            lazy_tree_dict_spaces_to_key[num_of_spaces] = value  # i guess i can use value, 0
        else:
            log.critical(line)

    return tree
