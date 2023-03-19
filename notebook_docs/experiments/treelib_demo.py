# PyTest
import sys
import pytest
import logging as log
import re
from treelib import Node, Tree
test_str = """
harry
  bill
  jane
    diane
      mary
    mark
"""



def test_name():
    """
    https://treelib.readthedocs.io/en/latest/
    ahh another horrible python package

    https://tree.nathanfriend.io/?s=(%27options!(%27fancy!true~fullPath!false~trailingSlash!true~rootDot!false)~.(%27.%27harry-bill-j0di02y-2k%27)~version!%271%27)*%20%20-%5Cn*.source!0ane-*2*mar%0120.-*
    https://yarnpkg.com/?q=%40nathanfriend%2Ftree-online
    """
    tree = Tree()
    tree.create_node("Harry", "harry")  # root node
    # tree.create_node("Harry", "harry",parent='harry')  # root node
    tree.create_node("Jane", "jane", parent="harry")
    tree.create_node("Bill", "bill", parent="harry")
    tree.create_node("Diane", "diane", parent="jane")
    tree.create_node("Mary", "mary", parent="diane")
    tree.create_node("Mark", "mark", parent="jane")
    log.warning('\n' + str(tree))


def test_recursive_try():
    delim: str = ' '  # space or tab
    delim_count: int = 2
    split_delim = delim
    for i in range(1,2):
        split_delim = split_delim + delim

    assert len(split_delim) == delim_count
    tree = Tree()
    lines = test_str.split('\n')

    treeRootNumOfSpaces:dict = dict()

    # Get root
    line = lines.pop(0)
    while re.match(r"^\s*$", line):
        line = lines.pop(0)
    # initialize
    re_matched = re.match(fr"^(\s*)(\S.*)",line)
    if(re_matched):
        spaces_in_front = re_matched.group(1) # None i guess
        num_of_spaces = len(spaces_in_front.split(split_delim)) - 1
        value = re_matched.group(2)
        tree.create_node(value,value) # value is key for 0
        treeRootNumOfSpaces[0] = value # i guess i can use value, 0


    for line in lines:
        if re.match(r"^\s*$", line):  # any one space
            continue
        # count number of spaces infront of first letter
        # re_matched = re.match(r"^( *)(\S.*)",line)
        re_matched = re.match(fr"^(\s*)(\S.*)",line)
        if(re_matched):
            spaces_in_front = re_matched.group(1) # None i guess
            num_of_spaces = len(spaces_in_front.split(split_delim)) - 1
            value = re_matched.group(2)
            # the last part is not - 1, but subtract until closest number. / largest but w/e for now
            tree.create_node(value, value,parent=treeRootNumOfSpaces[num_of_spaces - 1])  # value is key for 0
            treeRootNumOfSpaces[num_of_spaces] = value # i guess i can use value, 0
        else:
            log.critical(line)


    log.warning('\n' + str(tree))


if __name__ == '__main__':
    pytest.main(sys.argv)
