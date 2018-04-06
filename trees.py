import random

########## Nodes.
# Nodes to be used in trees.

class TreeNode:
    '''A node in a binary tree.'''
    def __init__(self, n):
        self.data = n
        self.left = self.right = None

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return self.__str__()

    def num_children(self):
        '''N.num_children() -> int

        Returns the number of children of N that are not None.
        '''
        return sum([1 for child in [self.left, self.right] if child])

class TreapNode(TreeNode):
    '''A node in a treap.'''
    def __init__(self, data, priority):
        super().__init__(data)  # Parent constructor.
        self.priority = priority

    def __str__(self):
        return "({}, {})".format(self.data, self.priority)
        
class AvlNode(TreeNode):
    '''A node in an AVL tree.'''
    def __init__(self, data):
        super().__init__(data)  # Parent constructor.
        self.height = 0

    def __str__(self):
        return "({}, {})".format(self.data, self.height)

########## Trees. ##########
# Trees utilizing above nodes. Use helper functions defined outside
# the class to achieve functionality.

class Bst:
    '''A BST. Does not contain duplicates. Nodes are of type TreeNode.'''
    def __init__(self):
        self.root = None
        self.size = 0

    def __str__(self):
        return tree_string(self.root)
    
    def __repr__(self):
        return self.__str__()
        
    def add(self, n):
        self.root, added = bst_add(self.root, n)
        if added:
            self.size += 1
        return added
    
    def find(self, n):
        return bst_find(self.root, n)
    
    def remove(self, n):
        self.root, removed = bst_remove(self.root, n)
        if removed:
            self.size -= 1
        return removed

    def clear(self):
        self.__init__()
        
class Treap(Bst):
    '''A treap. Does not contain duplicates. Nodes are of type TreapNode.'''
    max_priority = 1 << 10
    def __init__(self):
        super().__init__()
        self.priorities = set()
        
    def add(self, n):
        priority = random.randint(0, Treap.max_priority)
        while priority in self.priorities:
            priority = random.randint(0, Treap.max_priority)
        self.root, added = treap_add(self.root, n, priority)
        if added:
            self.size += 1
            self.priorities.add(priority)
        return added

    def remove(self, n):
        self.root, removed = treap_remove(self.root, n)
        if removed:
            self.size -= 1
        return removed

class AvlTree(Bst):
    '''An AVL tree. Does not contain duplicates. Nodes are of type AvlNode.'''
    def __init__(self):
        super().__init__()
        
    def add(self, n):
        self.root, added = avl_add(self.root, n)
        if added:
            self.size += 1
        return added

    def remove(self, n):
        self.root, removed = avl_remove(self.root, n)
        if removed:
            self.size -= 1
        return removed
    
########## Tree helper functions. ##########
# Work for any type of node above.
    
def tree_string(node, level = 0):
    '''tree_string(node) -> str

    Returns a string representation of the subtree rooted at node.

    credit: https://stackoverflow.com/questions/20242479/printing-a-tree-data-structure-in-python
    '''
    if not node:
        return '\n'
    prefix = '   '*level
    str = repr(node) + '\n'
    if node.num_children():
        str += prefix + '|_ ' + tree_string(node.left, level+1)
        str += prefix + '|_ ' + tree_string(node.right, level+1)
    return str
    
def tree_size(node):
    '''tree_size(node) -> int

    Returns a string representation of the subtree rooted at node.
    '''
    pass

def tree_height(node):
    '''tree_height(node) -> int

    Returns the height of the subtree rooted at node. Returns -1 if
    node is None.

    A node's height is the value of its height attribute, if it
    exists. Otherwise it has to be computed.

    See
    - EAFP at https://docs.python.org/3.4/glossary.html
    - https://stackoverflow.com/questions/610883/how-to-know-if-an-object-has-an-attribute-in-python
    '''
    pass

def inorder(n):
    '''inorder(node) -> [node content]

    Returns an inorder traversal of the subtree rooted at node; empty
    list if n is None.
    '''
    pass

def preorder(n):
    '''preorder(node) -> [node content]

    Returns an preorder traversal of the subtree rooted at node; empty
    list if n is None.
    '''
    pass

def postorder(n):
    '''postorder(node) -> [node content]

    Returns an postorder traversal of the subtree rooted at node;
    empty list if n is None.
    '''
    pass

def update_height(node):
    '''update_height(node) -> None

    Updates the value of node's height attribute using the height of
    its children.

    Assumes that node has a height attribute.
    '''
    pass

def rotate_left(node):
    '''rotate_left(node) -> node

    Returns the root of the tree obtained by rotating node to the
    left. Updates the height attribute of nodes where necessary and if
    the attribute is present.
    '''
    pass

def rotate_right(node):
    '''rotate_right(node) -> node

    Returns the root of the tree obtained by rotating node to the
    right. Updates the height attribute of nodes where necessary and if
    the attribute is present.
    '''
    pass

########## BST helper functions. ##########

def bst_find(node, n):
    '''bst_find(node, int) -> bool

    Returns whether n is contained in the subtree rooted at
    node. Assumes the subtree to be a BST with no duplicates.
    '''
    pass

def bst_find_min(node):
    '''bst_find_min(node) -> int

    Returns the smallest value stored in the subtree rooted at
    node. Assumes the subtree to be a BST with no duplicates.
    '''
    pass

def bst_add(node, n):
    '''bst_add(node, int) -> (node, bool)

    Returns the result of adding n to the subtree rooted at
    node. Assumes the subtree to be a BST with no duplicates.

    The first returned value is the root of the tree obtained as a
    result of the addition. The second value indicates whether
    addition succeeded. Addition fails if n is already present in the
    subtree.
    '''
    pass

def bst_remove(node, n):
    '''bst_remove(node, int) -> (node, bool)

    Returns the result of removing n from the subtree rooted at
    node. Assumes the subtree to be a BST with no duplicates.

    The first returned value is the root of the tree obtained as a
    result of the removal. The second value indicates whether removal
    succeeded. Removal fails if n is not present in the subtree.
    '''
    pass

########## Treap helper functions. ##########

def treap_add(node, n, p):
    '''treap_add(node, int, int) -> (node, bool)

    Returns the result of adding n with priority, p, to the subtree
    rooted at node. Assumes the subtree to be a treap with no
    duplicate values.

    The first returned value is the root of the treap obtained as a
    result of the addition. The second value indicates whether
    addition succeeded. Addition fails if n is already present in the
    subtree.
    '''
    pass

def treap_remove(node, n):
    '''treap_remove(node, int) -> (node, bool)

    Returns the result of removing n from the subtree rooted at
    node. Assumes the subtree to be a treap with no duplicate values.

    The first returned value is the root of the treap obtained as a
    result of the removal. The second value indicates whether removal
    succeeded. Removal fails if n is not present in the subtree.
    '''
    pass

########## AVL helper functions. ##########
        
def avl_balanced(node):
    '''avl_balanced(node) -> bool

    Returns whether the AVL property is satisfied at node. Should work
    for any of the nodes defined above.
    '''
    pass

def avl_left_left(node):
    '''avl_left_left(node) -> node
    
    Returns the root of the tree obtained by resolving a left-left
    case at node.
    '''
    pass

def avl_right_right(node):
    '''avl_right_right(node) -> node
    
    Returns the root of the tree obtained by resolving a right_right
    case at node.
    '''
    pass

def avl_left_right(node):
    '''avl_left_right(node) -> node
    
    Returns the root of the tree obtained by resolving a left_right
    case at node.
    '''
    pass

def avl_right_left(node):
    '''avl_right_left(node) -> node
    
    Returns the root of the tree obtained by resolving a right_left
    case at node.
    '''
    pass

def avl_add(node, n):
    '''avl_add(node, int) -> (node, bool)

    Returns the result of adding n to the subtree rooted at
    node. Assumes the subtree to be a valid AVL tree with no
    duplicates.

    The first returned value is the root of the AVL tree obtained as a
    result of the addition. The second value indicates whether
    addition succeeded. Addition fails if n is already present in the
    subtree.
    '''
    pass

def avl_remove(node, n):
    '''avl_remove(node, int) -> (node, bool)

    Returns the result of removing n from the subtree rooted at
    node. Assumes the subtree to be a valid AVL tree with no
    duplicates.

    The first returned value is the root of the AVL tree obtained as a
    result of the removal. The second value indicates whether removal
    succeeded. Removal fails if n is not present in the subtree.
    '''
    pass        
