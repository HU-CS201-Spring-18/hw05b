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
        num = 0
        for child in [self.left, self.right]:
            if child:
                num += 1
        return num
    
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
    '''A BST that does not contain duplicates.'''
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
    '''A treap that does not contain duplicate values.'''
    max_priority = 1 << 32
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
    '''An AVL tree that does not contain duplicate values.'''
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
    string = repr(node) + '\n'
    if node.num_children():
        string += prefix + '|_ ' + tree_string(node.left, level+1)
        string += prefix + '|_ ' + tree_string(node.right, level+1)
    return string
    
def tree_size(node):
    '''tree_size(node) -> int

    Returns a string representation of the subtree rooted at node.
    '''
    if not node:
        return 0
    return 1 + tree_size(node.left) + tree_size(node.right)

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
    if not node:
        return -1
    try:
        return node.height
    except AttributeError:
        return 1 + max(tree_height(node.left), tree_height(node.right))

def inorder(n):
    '''inorder(node) -> [node content]

    Returns an inorder traversal of the subtree rooted at node; empty
    list if n is None.
    '''
    if not n:
        return []
    return inorder(n.left) + [repr(n)] + inorder(n.right)

def preorder(n):
    '''preorder(node) -> [node content]

    Returns an preorder traversal of the subtree rooted at node; empty
    list if n is None.
    '''
    if not n:
        return []
    return [repr(n)] + preorder(n.left) + preorder(n.right)

def postorder(n):
    '''postorder(node) -> [node content]

    Returns an postorder traversal of the subtree rooted at node;
    empty list if n is None.
    '''
    if not n:
        return []
    return postorder(n.left) + postorder(n.right) + [repr(n)]

def update_height(node):
    '''update_height(node) -> None

    Updates the value of node's height attribute using the height of
    its children.

    Assumes that node has a height attribute.
    '''
    if node:
        node.height = 1 + max(tree_height(node.left), tree_height(node.right))

def rotate_left(node):
    '''rotate_left(node) -> node

    Returns the root of the tree obtained by rotating node to the
    left. Updates the height attribute of nodes where necessary and if
    the attribute is present.
    '''
    new_parent = node.right
    assert(new_parent)
    node.right = new_parent.left
    new_parent.left = node
    try:
        update_height(node)
        update_height(new_parent)
    except AttributeError:
        pass
    return new_parent

def rotate_right(node):
    '''rotate_right(node) -> node

    Returns the root of the tree obtained by rotating node to the
    right. Updates the height attribute of nodes where necessary and if
    the attribute is present.
    '''
    new_parent = node.left
    assert(new_parent)
    node.left = new_parent.right
    new_parent.right = node
    try:
        update_height(node)
        update_height(new_parent)
    except AttributeError:
        pass
    return new_parent

########## BST helper functions. ##########
    
def bst_find(node, n):
    '''bst_find(node, int) -> bool

    Returns whether n is contained in the subtree rooted at
    node. Assumes the subtree to be a BST with no duplicates.
    '''
    if not node:
        return False
    data = node.data
    if n < data:
        return bst_find(node.left, n)
    if n > data:
        return bst_find(node.right, n)
    return True

def bst_find_min(node):
    '''bst_find_min(node) -> int

    Returns the smallest value stored in the subtree rooted at
    node. Assumes the subtree to be a BST with no duplicates.
    '''
    if not node:
        return
    if node.left:
        return bst_find_min(node.left)
    return node.data

def bst_add(node, n):
    '''bst_add(node, int) -> (node, bool)

    Returns the result of adding n to the subtree rooted at
    node. Assumes the subtree to be a BST with no duplicates.

    The first returned value is the root of the tree obtained as a
    result of the addition. The second value indicates whether
    addition succeeded. Addition fails if n is already present in the
    subtree.
    '''
    if not node:
        node = TreeNode(n)
        added = True
    elif n < node.data:
        node.left, added = bst_add(node.left, n)
    elif n > node.data:
        node.right, added = bst_add(node.right, n)
    else:
        added = False
    return (node, added)

def bst_remove(node, n):
    '''bst_remove(node, int) -> (node, bool)

    Returns the result of removing n from the subtree rooted at
    node. Assumes the subtree to be a BST with no duplicates.

    The first returned value is the root of the tree obtained as a
    result of the removal. The second value indicates whether removal
    succeeded. Removal fails if n is not present in the subtree.
    '''
    if not node:
        removed = False
    elif n < node.data:
        node.left, removed = bst_remove(node.left, n)
    elif n > node.data:
        node.right, removed = bst_remove(node.right, n)
    else:
        if node.num_children() == 2:
            succ = bst_find_min(node.right)
            node.data = succ
            node.right, _ = bst_remove(node.right, succ)
        elif node.left:
            node = node.left
        elif node.right:
            node = node.right
        else:
            node = None
        removed = True
    return (node, removed)

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
    if not node:
        node = TreapNode(n, p)
        added = True
    elif n < node.data:
        node.left, added = treap_add(node.left, n, p)
        if added and p < node.priority:
            node = rotate_right(node)
    elif n > node.data:
        node.right, added = treap_add(node.right, n, p)
        if added and p < node.priority:
            node = rotate_left(node)
    else:
        added = False
    return (node, added)

def treap_remove(node, n):
    '''treap_remove(node, int) -> (node, bool)

    Returns the result of removing n from the subtree rooted at
    node. Assumes the subtree to be a treap with no duplicate values.

    The first returned value is the root of the treap obtained as a
    result of the removal. The second value indicates whether removal
    succeeded. Removal fails if n is not present in the subtree.
    '''
    if not node:
        removed = False
    elif n < node.data:
        node.left, removed = treap_remove(node.left, n)
    elif n > node.data:
        node.right, removed = treap_remove(node.right, n)
    else:
        if node.num_children() == 2:
            if node.left.priority < node.right.priority:
                node = rotate_right(node)
            else:
                node = rotate_left(node)
            node = treap_remove(node, n)[0]
        elif node.left:
            node = node.left
        elif node.right:
            node = node.right
        else:
            node = None
        removed = True
    return (node, removed)

########## AVL helper functions. ##########

def avl_balanced(node):
    '''avl_balanced(node) -> bool

    Returns whether the AVL property is satisfied at node. Should work
    for any of the nodes defined above.
    '''
    return abs(tree_height(node.left) - tree_height(node.right)) <= 1

def avl_left_left(node):
    '''avl_left_left(node) -> node
    
    Returns the root of the tree obtained by resolving a left-left
    case at node.
    '''
    return rotate_right(node)

def avl_right_right(node):
    '''avl_right_right(node) -> node
    
    Returns the root of the tree obtained by resolving a right_right
    case at node.
    '''
    return rotate_left(node)

def avl_left_right(node):
    '''avl_left_right(node) -> node
    
    Returns the root of the tree obtained by resolving a left_right
    case at node.
    '''
    node.left = rotate_left(node.left)
    return rotate_right(node)

def avl_right_left(node):
    '''avl_right_left(node) -> node
    
    Returns the root of the tree obtained by resolving a right_left
    case at node.
    '''
    node.right = rotate_right(node.right)
    return rotate_left(node)
    
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
    if not node:
        node = AvlNode(n)
        added = True
    elif n < node.data:
        node.left, added = avl_add(node.left, n)
        if added:
            update_height(node)
            if not avl_balanced(node):
                if n < node.left.data:
                    node = avl_left_left(node)
                else:
                    node = avl_left_right(node)
    elif n > node.data:
        node.right, added = avl_add(node.right, n)
        if added:
            update_height(node)
            if not avl_balanced(node):
                if n > node.right.data:
                    node = avl_right_right(node)
                else:
                    node = avl_right_left(node)
    else:
        added = False
    return (node, added)
        
def avl_remove(node, n):
    '''avl_remove(node, int) -> (node, bool)

    Returns the result of removing n from the subtree rooted at
    node. Assumes the subtree to be a valid AVL tree with no
    duplicates.

    The first returned value is the root of the AVL tree obtained as a
    result of the removal. The second value indicates whether removal
    succeeded. Removal fails if n is not present in the subtree.
    '''
    if not node:
        removed = False
    elif n < node.data:
        node.left, removed = avl_remove(node.left, n)
        if removed:
            update_height(node)
            if not avl_balanced(node):
                if n < node.left.data:
                    node = avl_left_left(node)
                else:
                    node = avl_left_right(node)
    elif n > node.data:
        node.right, removed = avl_remove(node.right, n)
        if removed:
            update_height(node)
            if not avl_balanced(node):
                if n > node.right.data:
                    node = avl_right_right(node)
                else:
                    node = avl_right_left(node)
    else:
        if node.num_children() == 2:
            succ = bst_find_min(node.right)
            node.data = succ
            node.right, _ = avl_remove(node.right, succ)
        elif node.left:
            node = node.left
        elif node.right:
            node = node.right
        else:
            node = None
        removed = True
    return (node, removed)

########## Timing. ##########

import timeit

def tree_find_time(tree, x):
    start_time = timeit.default_timer()
    if not tree.find(x):
        pass
    return (timeit.default_timer() - start_time)

def list_find_time(lst, x):
    start_time = timeit.default_timer()
    try:
        lst.index(x)
    except:
        pass
    return (timeit.default_timer() - start_time)

def get_trees(lst):
    trees = [Bst(), Treap(), AvlTree()]
    for x in lst:
        for t in trees:
            t.add(x)
    return trees

def compare_find(n=1000, repeat=3, number=1000):
    lst_times = []
    tree_times = [[], [], []]
    limit = 1<<30
    # Perform several repetitions. 
    for _ in range(repeat):
        # generate list and trees.
        lst = random.sample(range(limit), n)
        trees = get_trees(lst)
        lst_time = 0
        tree_time = [0]*len(trees)
        # accumulate total find time over a number of iterations.
        for _ in range(number):
            x = random.randint(0,limit)
            lst_time += list_find_time(lst, x)
            for i,t in enumerate(trees):
                tree_time[i] += tree_find_time(t, x)
        # Save times for this repetition.
        lst_times.append(lst_time)
        for i,times in enumerate(tree_times):
            times.append(tree_time[i])
    # Output the minimum time from each repetition, as per best practice.
    times = [n,min(lst_times)] + [min(times) for times in tree_times]
    times = [str(num) for num in times]
    print('\t'.join(times))
    

import matplotlib.pyplot as plt
def plot_times(fname='times.txt'):
    n = []
    times = [[], [], [], []]
    for line in open(fname):
        nums = line.split()
        n.append(int(nums[0]))
        for i,t in enumerate(nums[1:]):
            times[i].append(float(t))
    labels = ['List', 'BST', 'Treap', 'AVL']
    colors = ['-r', '-b', '-g', '-y']
    fig, (a0,a1) = plt.subplots(2,1)
    for i,t in enumerate(times):
        a0.plot(n, t, colors[i], label=labels[i])
    for i,t in enumerate(times[1:]):
        a1.plot(n, t, colors[i+1], label=labels[i+1])
    for ax in (a0,a1):
        ax.set(xlabel='n',ylabel='Time (s)')
        ax.legend(loc='best')
        ax.grid()
    a0.set_title("Time for 1000 find()'s in structures of size n")
    a1.set_title('Above figure without list')
    fig.subplots_adjust(hspace=.5)
    fig.savefig(fname[:-3]+'png')
    plt.show()
