# PyTest
import sys
import pytest
import logging as log
import re
from treelib import Node, Tree

from docs_conda_jupyter_lab.dump_simple_str_to_tree import dump_str_to_tree

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
    tree = dump_str_to_tree(test_str)
    log.warning('\n' + str(tree))


if __name__ == '__main__':
    pytest.main(sys.argv)
