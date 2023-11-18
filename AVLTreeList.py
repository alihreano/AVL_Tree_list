# username - jadmahajne, alihreano
# id1      - 318978152
# name1    - jad mahajne
# id2      - 315306191
# name2    - ali hreano


"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type value: str
    @param value: data of your node
    """

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right =None
        self.parent = None
        self.size = 1
        self.height = 0
        self.bf = 0


    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child
    """

    def getLeft(self):
        if (AVLNode.isRealNode(self.left)):
            return self.left
        return None

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child
    """

    def getRight(self):
        if(AVLNode.isRealNode(self.right)):
            return self.right
        return None

    """returns the parent 

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def getParent(self):
        return self.parent

    """return the value

    @rtype: str                                                                                                                                                                                                                                                                       
    @returns: the value of self, None if the node is virtual
    """

    def getValue(self):
        if(AVLNode.isRealNode(self)):
            return self.value
        return None

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def getHeight(self):
        if(AVLNode.isRealNode(self)):
            return self.height
        return -1

    """sets left child

    @type node: AVLNode
    @param node: a node
    """

    def setLeft(self, node):
        self.left=node
        return None

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def setRight(self, node):
        self.right=node
        return None

    """sets parent

    @type node: AVLNode
    @param node: a node
    """

    def setParent(self, node):
        self.parent=node
        return

    """sets value

    @type value: str
    @param value: data
    """

    def setValue(self, value):
        self.value=value
        return

    """sets the balance factor of the node

    @type h: int
    @param h: the height
    """

    def setHeight(self, h):
        self.height=h
        return None

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """


    def isRealNode(self):
        if self==None:
            return False
        if (self.height==-1):
            return False
        return True


"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.root = None
        self.len = 0
        self.first_node = None
        self.last_node = None

    # add your fields here

    """returns whether the list is empty

    @rtype: bool
    @returns: True if the list is empty, False otherwise
    """

    def empty(self):
        if self.root==None:
            return True
        return False

    """retrieves the value of the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: index in the list
    @rtype: str
    @returns: the the value of the i'th item in the list
    """
    def retrieve(self, i):
        node=self.retrieve_node(i)
        return node.value

    def retrieve_node(self, i):
        return self.Tree_Select(i + 1)

    def Tree_Select(T, k):
        def Tree_Select_rec(x, k):
            if (AVLNode.isRealNode(x.left)):
                r = x.left.size + 1
            else:
                r = 1
            if k == r:
                return x
            elif k < r:
                return Tree_Select_rec(x.left, k)
            else:
                return Tree_Select_rec(x.right, k - r)

        return Tree_Select_rec(T.root, k)

    """inserts val at position i in the list

    @type i: int
    @pre: 0 <= i <= self.length()
    @param i: The intended index in the list to which we insert val
    @type val: str
    @param val: the value we inserts
    @rtype: list
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, i, val):
        # insert a node with val in AVL treelist
        new_node = AVLNode(val)
        AVLTreeList.create_virtual_left(new_node)
        AVLTreeList.create_virtual_right(new_node)
        if self.empty():  # insert in an empty tree
            self.root = new_node
            self.len += 1
            self.last_node = self.first_node = new_node
            return 0
        if i == self.len:  # insert as the last item in the list
            # self.length>0 ==> i=self.length>=1
            self.last_node.right = new_node
            new_node.parent = self.last_node
            self.last_node = new_node
        else:
            if i == 0:  # update self.first_node
                self.first_node = new_node
            old_i = self.retrieve_node(i)
            if not(AVLNode.isRealNode(old_i.left)):
                old_i.left = new_node
                new_node.parent = old_i
            else:
                # i>0 because if i==0 then it has no left child ==> condition 1
                z = self.retrieve_node(i - 1)  # z is the predecessor of i
                z.right = new_node
                new_node.parent = z
        #at this point the new node is inserted in its regular location
        node_to_root = new_node.parent #starting the loop with the new_node's parent
        rotation_counter = 0
        while (node_to_root != None):  # go up to the root
            node_to_root.size += 1  # update the node's size
            node_to_root.bf = AVLTreeList.compute_BF(node_to_root)  # compute the balance factor for the node
            old_parent = node_to_root.parent  # save the old parent of the node before any rotation (to keep the path from the node to the root)
            has_left = (AVLNode.isRealNode(node_to_root.left))  # check if the node has left son
            has_right = (AVLNode.isRealNode(node_to_root.right))  # check if the node has right son
            if has_left:
                node_to_root.left.bf = AVLTreeList.compute_BF(node_to_root.left)
            if has_right:
                node_to_root.right.bf = AVLTreeList.compute_BF(node_to_root.right)
            if has_left and (node_to_root.bf == +2) and (node_to_root.left.bf == +1):  # check if we need to do right rotation
                AVLTreeList.Rotate_right(node_to_root)
                rotation_counter += 1
            elif has_right and (node_to_root.bf == -2) and (
                    node_to_root.right.bf == -1):  # check if we need to do left rotation
                AVLTreeList.Rotate_left(node_to_root)
                rotation_counter += 1
            elif has_right and (node_to_root.bf == -2) and (
                    node_to_root.right.bf == +1):  # check if we need to do right_left rotation
                AVLTreeList.Rotate_right(node_to_root.right)
                AVLTreeList.Rotate_left(node_to_root)
                rotation_counter += 2
            elif has_left and (node_to_root.bf == +2) and (
                    node_to_root.left.bf == -1):  # check if we need to do left_right rotation
                AVLTreeList.Rotate_left(node_to_root.left)
                AVLTreeList.Rotate_right(node_to_root)
                rotation_counter += 2
            else:  # if there is no rotations done, update the height
                prev_height=node_to_root.height
                AVLTreeList.update_height(node_to_root)
                if prev_height!=node_to_root.height and abs(node_to_root.bf)<2:
                    rotation_counter+=1
            if node_to_root.parent != None and node_to_root.parent.parent == None:  # check if there is a new root after rotation
                self.root = node_to_root.parent
            node_to_root = old_parent  # update the node to its parent
        self.len += 1

        return rotation_counter

    def compute_BF(node):
        # calculate the bf of the given node
        if (not(AVLNode.isRealNode(node.left))) and (AVLNode.isRealNode(node.right)):
            return (-1) - (node.right.height)
        elif (AVLNode.isRealNode(node.left)) and (not(AVLNode.isRealNode(node.right))):
            return (node.left.height) - (-1)
        elif (not(AVLNode.isRealNode(node.left))) and (not(AVLNode.isRealNode(node.right))):
            return 0
        else:
            return (node.left.height - node.right.height)

    def Rotate_right(node):
        # do a right rotation for the given node
        B = node
        if B.parent != None:
            is_left = (B.parent.left == B)
        A = node.left
        B.left = A.right
        if B.left != None:
            B.left.parent = B
        A.right = B
        A.parent = B.parent
        if A.parent != None:
            if (is_left):
                A.parent.left = A
            else:
                A.parent.right = A
        B.parent = A
        A.size = B.size
        AVLTreeList.update_height(B)
        AVLTreeList.update_size(B)
        AVLTreeList.update_height(A)

    def Rotate_left(node):
        # do a left rotation for the given node
        B = node
        if B.parent != None:
            is_left = (B.parent.left == B)
        A = node.right
        B.right = A.left
        if B.right != None:
            B.right.parent = B
        A.left = B
        A.parent = B.parent
        if A.parent != None:
            if (is_left):
                A.parent.left = A
            else:
                A.parent.right = A
        B.parent = A
        A.size = B.size
        AVLTreeList.update_height(B)
        AVLTreeList.update_size(B)
        AVLTreeList.update_height(A)

    def update_height(node):
        #updates the height of the given node
        if not(AVLNode.isRealNode(node.left))  and AVLNode.isRealNode(node.right):
            node.height = node.right.height + 1
        elif AVLNode.isRealNode(node.left) and not(AVLNode.isRealNode(node.right)):
            node.height = node.left.height + 1
        elif AVLNode.isRealNode(node.left) and AVLNode.isRealNode(node.right):
            node.height = max(node.left.height, node.right.height) + 1
        else:
            node.height = 0

    def update_size(node):
        #updates the size of the given node
        if not(AVLNode.isRealNode(node.left))  and AVLNode.isRealNode(node.right):
            node.size = node.right.size + 1
        elif AVLNode.isRealNode(node.left) and not (AVLNode.isRealNode(node.right)):
            node.size = node.left.size + 1
        elif AVLNode.isRealNode(node.left) and AVLNode.isRealNode(node.right):
            node.size = node.left.size + node.right.size + 1
        else:
            node.size = 1

    def create_virtual_right(node):
        #creates right virtual son for the given node
        node.right = AVLNode("None")
        node.right.height = -1
        node.right.size = 0
        node.right.parent=node
    def create_virtual_left(node):
        #creates left virtual son for the given node
        node.left = AVLNode("None")
        node.left.height = -1
        node.left.size = 0
        node.left.parent=node

    """deletes the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list to be deleted
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, i):
        node = AVLTreeList.retrieve_node(self, i)
        if self.len == 1:
            self.root = None
            self.len = 0
            self.last_node = self.first_node = None
            return 0
        if self.first_node == node: #if we are deleting the first node then update the self.first to be its successor
            self.first_node = AVLTreeList.retrieve_node(self, i + 1)
        if self.last_node == node: #if we are deleting the last node then update the self.last to be its predeccessor
            self.last_node = AVLTreeList.retrieve_node(self, i - 1)
        if not (AVLNode.isRealNode(node.right)) and not (AVLNode.isRealNode(node.left)):
            to_start = node.parent  # starting the node_to_root loop with the parent because a leaf
            AVLTreeList.delete_leaf(self, node)
        elif AVLNode.isRealNode(node.right) and AVLNode.isRealNode(node.left):
            successor = AVLTreeList.retrieve_node(self, i + 1)
            if successor == node.right:
                to_start = successor # starting the node_to_root loop with the successor if he has 2 children and the successor is his right son
            else:
                to_start = successor.parent # starting the node_to_root loop with the successor's parent if he has 2 children and the successor is not his right child
            AVLTreeList.delete_2child(self, node, i)
        else:
            to_start = node.parent #starting the node_to_root loop with the node's parent if the node has 1 child
            AVLTreeList.delete_1child(self, node)
        #at this point the node is deleted regularly from the tree
        node_to_root = to_start
        rotation_counter = 0
        while (node_to_root != None):  # go up to the root
            node_to_root.size -= 1  # update the node's size
            node_to_root.bf = AVLTreeList.compute_BF(node_to_root)  # compute the balance factor for the node
            old_parent = node_to_root.parent  # save the old parent of the node before any rotation (to keep the path from the node to the root)
            has_left = (AVLNode.isRealNode(node_to_root.left))  # check if the node has left son
            has_right = (AVLNode.isRealNode(node_to_root.right))  # check if the node has right son
            if has_left:
                node_to_root.left.bf = AVLTreeList.compute_BF(node_to_root.left)
            if has_right:
                node_to_root.right.bf = AVLTreeList.compute_BF(node_to_root.right)
            if has_left and (node_to_root.bf == +2) and (
                    node_to_root.left.bf == +1 or node_to_root.left.bf == 0):  # check if we need to do right rotation
                AVLTreeList.Rotate_right(node_to_root)
                rotation_counter += 1
            elif has_right and (node_to_root.bf == -2) and (
                    node_to_root.right.bf == -1 or node_to_root.right.bf == 0):  # check if we need to do left rotation
                AVLTreeList.Rotate_left(node_to_root)
                rotation_counter += 1
            elif has_right and (node_to_root.bf == -2) and (
                    node_to_root.right.bf == +1):  # check if we need to do right_left rotation
                AVLTreeList.Rotate_right(node_to_root.right)
                AVLTreeList.Rotate_left(node_to_root)
                rotation_counter += 2
            elif has_left and (node_to_root.bf == +2) and (
                    node_to_root.left.bf == -1):  # check if we need to do left_right rotation
                AVLTreeList.Rotate_left(node_to_root.left)
                AVLTreeList.Rotate_right(node_to_root)
                rotation_counter += 2
            else:  # if there is no rotations done, update the height
                prev_height = node_to_root.height
                AVLTreeList.update_height(node_to_root)
                if prev_height != node_to_root.height and abs(node_to_root.bf) < 2:
                    rotation_counter += 1
            if node_to_root.parent != None and node_to_root.parent.parent == None:  # check if there is a new root after rotation
                self.root = node_to_root.parent
            node_to_root = old_parent  # update the node to its parent
        self.len -= 1

        return rotation_counter

    def delete_leaf(T, node):
        #deletes the node as a leaf in the tree T
        if node == node.parent.right:
            AVLTreeList.create_virtual_right(node.parent)
            node.parent = None
        else:
            AVLTreeList.create_virtual_left(node.parent)
            node.parent = None

    def delete_1child(T, node):
        #deletes the node as a node that has 1 child in the tree T
        if node == T.root:
            if AVLNode.isRealNode(node.right):
                T.root = node.right
                node.right.parent = None
                AVLTreeList.create_virtual_right(node)
            else:
                T.root = node.left
                node.left.parent = None
                AVLTreeList.create_virtual_left(node)
        elif node == node.parent.right:
            if AVLNode.isRealNode(node.right):
                node.parent.right = node.right
                node.right.parent = node.parent
                node.parent = None
                AVLTreeList.create_virtual_right(node)
            else:
                node.parent.right = node.left
                node.left.parent = node.parent
                node.parent = None
                AVLTreeList.create_virtual_left(node)
        else:
            if AVLNode.isRealNode(node.right):
                node.parent.left = node.right
                node.right.parent = node.parent
                node.parent = None
                AVLTreeList.create_virtual_right(node)
            else:
                node.parent.left = node.left
                node.left.parent = node.parent
                node.parent = None
                AVLTreeList.create_virtual_left(node)

    def delete_2child(T, node, i):
        #deletes the node in index i as a node that has 2 children in the tree T
        y = AVLTreeList.retrieve_node(T, i + 1)
        if node == T.root:
            y_isleft = (y == y.parent.left)
            if y_isleft:
                y.parent.left = y.right
                y.right.parent = y.parent
                T.root = y
                y.left = node.left
                node.left.parent = y
                y.right = node.right
                node.right.parent = y
                y.parent = None
                y.size = node.size
                y.height = node.height
            else:
                T.root = y
                y.left = node.left
                node.left.parent = y
                y.parent = None
                y.size = node.size
                y.height = node.height
            return
        elif node == node.parent.right:
            node.parent.right = y
        elif node == node.parent.left:
            node.parent.left = y
        if y.parent == node:
            y.parent = node.parent
            y.left = node.left
            y.left.parent = y
        else:
            y.parent.left = y.right
            y.right.parent = y.parent
            y.parent = node.parent
            y.left = node.left
            node.left.parent = y
            y.right = node.right
            y.right.parent = y
        node.parent = None
        AVLTreeList.create_virtual_left(node)
        AVLTreeList.create_virtual_right(node)
        y.size = node.size
        y.height = node.height

    """returns the value of the first item in the list

    @rtype: str
    @returns: the value of the first item, None if the list is empty
    """

    def first(self):
        if self.empty():
            return None
        return self.first_node.value

    """returns the value of the last item in the list

    @rtype: str
    @returns: the value of the last item, None if the list is empty
    """

    def last(self):
        if self.empty():
            return None
        return self.last_node.value

    """returns an array representing list 

    @rtype: list
    @returns: a list of strings representing the data structure
    """

    def listToArray(self):
        if self.len==0:
            return []
        return AVLTreeList.ListToArray_rec(self.root)

    def ListToArray_rec(node):
        if not AVLNode.isRealNode(node):
            return []
        res = AVLTreeList.ListToArray_rec(node.left) + [node.value] + AVLTreeList.ListToArray_rec(node.right)
        return res

    """returns the size of the list 

    @rtype: int
    @returns: the size of the list
    """

    def length(self):
        return self.len

    """splits the list at the i'th index

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list according to whom we split
    @rtype: list
    @returns: a list [left, val, right], where left is an AVLTreeList representing the list until index i-1,
    right is an AVLTreeList representing the list from index i+1, and val is the value at the i'th index.
    """

    def split(self, i):
        if i == self.len - 1: #splitting the tree_list with its last element
            val = self.last_node.value
            AVLTreeList.delete(self, i)
            left = self
            right = AVLTreeList()
            return [left, val, right]
        if i == 0: #splitting the tree_list with its first elemnt
            val = self.first_node.value
            AVLTreeList.delete(self, i)
            left = AVLTreeList()
            right = self
            return [left, val, right]
        node_i = AVLTreeList.retrieve_node(self, i) # node_i is the node with the index i
        node_i_value=node_i.value
        if node_i == self.root: #splitting the tree_list with the elemnt that representing the root of the tree
            left = AVLTreeList() #left is the tree with elements that has index<i
            right = AVLTreeList() #right is the tree with elements that has index>i
            if AVLNode.isRealNode(self.root.left):
                left_length = self.root.left.size
                left_first = self.first_node
                left_last = AVLTreeList.retrieve_node(self, i - 1)
                AVLTreeList.update_fields(left, left_length, left_first, left_last, self.root.left)
            if AVLNode.isRealNode(self.root.right):
                right_length = self.root.right.size
                right_first = AVLTreeList.retrieve_node(self, i + 1)
                right_last = self.last_node
                AVLTreeList.update_fields(right, right_length, right_first, right_last, self.root.right)
            return [left, node_i.value, right]
        left = AVLTreeList() #left is the tree with elements that has index<i
        right = AVLTreeList() #right is the tree with elements that has index>i
        if AVLNode.isRealNode(node_i.left):
            left_node = node_i.left
            left_length = left_node.size
            left_first = AVLTreeList.find_first(left_node)
            left_last = left_node
            AVLTreeList.update_fields(left, left_length, left_first, left_last, left_node)
        if AVLNode.isRealNode(node_i.right):
            right_node = node_i.right
            right_length = right_node.size
            right_first = right_node
            right_last = AVLTreeList.find_last(right_node)
            AVLTreeList.update_fields(right, right_length, right_first, right_last, right_node)
        parent = node_i.parent
        while parent != None: #go up to the root
            T = AVLTreeList()
            is_right = (parent.right == node_i)
            if is_right: #if the upper arc/bond from parent is left (parent is a right son )
                AVLTreeList.create_virtual_right(parent)
                parent.right.parent = node_i.parent
                node_i.parent = None
                node_i = parent
                parent = node_i.parent
                T.root = node_i
                node_i.size = node_i.left.size + 1
                AVLNode.setHeight(node_i, AVLNode.getHeight(node_i.left) + 1)
                AVLTreeList.update_fields(T, T.root.size, AVLTreeList.find_first(T.root),
                                          AVLTreeList.find_last((T.root)), T.root)
                T.concat(left)
                left = T
            else:
                AVLTreeList.create_virtual_left(parent)
                node_i = parent
                parent = node_i.parent
                node_i.parent = None
                T.root = node_i.right
                T.root.parent = None
                AVLTreeList.create_virtual_right(node_i)
                node_i.left = right.root
                if (node_i.left == None):
                    AVLTreeList.create_virtual_left(node_i)
                    node_i.size = 1
                    node_i.height = 0
                right.root = node_i
                right.root.parent = None
                if (AVLNode.isRealNode(node_i.left)):
                    node_i.size = node_i.left.size + 1
                    AVLNode.setHeight(node_i, AVLNode.getHeight(node_i.left) + 1)
                AVLTreeList.update_fields(T, T.root.size, AVLTreeList.find_first(T.root),
                                          AVLTreeList.find_last((T.root)), T.root)
                AVLTreeList.update_fields(right, right.root.size, AVLTreeList.find_first(right.root),
                                          AVLTreeList.find_last((right.root)), right.root)
                right.concat(T)

        return [left, node_i_value, right]

    def find_first(node):
        #finds the first node from the given node
        current_node = node
        while (AVLNode.isRealNode(current_node.left)):
            current_node = current_node.left
        return current_node

    def find_last(node):
        #finds the last node from the given node
        current_node = node
        while (AVLNode.isRealNode(current_node.right)):
            current_node = current_node.right
        return current_node













    """concatenates lst to self

    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def concat(self, lst):
        T1=self
        T2=lst
        if T1.len==0 and T2.len==0: #if both of the tree_lists are empty
            return 0
        elif T1.len==0: #if self=T1 is empty
            AVLTreeList.update_fields(self, T2.len, T2.first_node, T2.last_node, T2.root)
            return T2.root.height
        elif T2.len==0: #if other=T2 is empty
            return T1.root.height
        T2.last_node=T2.retrieve_node(T2.length()-1)
        T2.first_node=T2.retrieve_node(0)
        T1.first_node=T1.retrieve_node(0)
        T1.last_node=T1.retrieve_node(T1.length()-1)
        last=T2.last_node
        first=T1.first_node
        length= T1.len + T2.len
        res=abs(T1.root.height-T2.root.height)
        if (T2.root.height>=T1.root.height):
            if T1.len==1: #if T1 has 1 element and T1.height<=T2.height
                T2.first_node.left=T1.root
                T1.root.parent=T2.first_node
                to_start=T2.first_node
                AVLTreeList.update_fields(self,length,first,last,T2.root)
            else:
                x = T1.retrieve_node(T1.length()-1)
                AVLTreeList.delete(T1, T1.length()-1 )
                first_h=T2.root
                while(first_h.height>T1.root.height):
                    if AVLNode.isRealNode(first_h.left):
                       first_h=first_h.left
                    else:
                        break
                if first_h==T2.root:
                    to_start=first_h
                    x.right=first_h
                    first_h.parent=x
                    x.left=T1.root
                    T1.root.parent=x
                    AVLTreeList.update_fields(self,length,first,last,x)
                else:
                    to_start=x
                    x.parent=first_h.parent
                    x.left=T1.root
                    T1.root.parent=x
                    x.right=first_h
                    first_h.parent=x
                    if x.parent!=None:
                        x.parent.left=x
                    AVLTreeList.update_fields(self,length,first,last,T2.root)
        else:
            x = T1.last_node
            AVLTreeList.delete(T1, T1.len - 1)
            first_h = T1.root
            while (first_h.height > T2.root.height):
                if AVLNode.isRealNode(first_h.right):
                    first_h = first_h.right
                else:
                    break
            if first_h == T1.root:
                to_start = first_h
                x.left = first_h
                first_h.parent = x
                x.right = T2.root
                T2.root.parent = x
                AVLTreeList.update_fields(self, length, first, last, x)
            else:
                to_start = x
                x.parent = first_h.parent
                x.right = T2.root
                T2.root.parent = x
                x.left = first_h
                first_h.parent = x
                if x.parent!=None:
                    x.parent.right = x
                AVLTreeList.update_fields(self, length, first, last, T1.root)
        node_to_root = to_start
        while (node_to_root != None):  # go up to the root
            AVLTreeList.update_size(node_to_root)
            node_to_root.bf = AVLTreeList.compute_BF(node_to_root)  # compute the balance factor for the node
            old_parent = node_to_root.parent  # save the old parent of the node before any rotation (to keep the path from the node to the root)
            has_left = (AVLNode.isRealNode(node_to_root.left))  # check if the node has left son
            has_right = (AVLNode.isRealNode(node_to_root.right))  # check if the node has right son
            if has_left:
                node_to_root.left.bf = AVLTreeList.compute_BF(node_to_root.left)
            if has_right:
                node_to_root.right.bf = AVLTreeList.compute_BF(node_to_root.right)
            if has_left and (node_to_root.bf == +2) and (
                    node_to_root.left.bf == +1 or node_to_root.left.bf == 0):  # check if we need to do right rotation
                AVLTreeList.Rotate_right(node_to_root)
            elif has_right and (node_to_root.bf == -2) and (
                    node_to_root.right.bf == -1 or node_to_root.right.bf == 0):  # check if we need to do left rotation
                AVLTreeList.Rotate_left(node_to_root)
            elif has_right and (node_to_root.bf == -2) and (
                    node_to_root.right.bf == +1):  # check if we need to do right_left rotation
                AVLTreeList.Rotate_right(node_to_root.right)
                AVLTreeList.Rotate_left(node_to_root)
            elif has_left and (node_to_root.bf == +2) and (
                    node_to_root.left.bf == -1):  # check if we need to do left_right rotation
                AVLTreeList.Rotate_left(node_to_root.left)
                AVLTreeList.Rotate_right(node_to_root)
            else:  # if there is no rotations done, update the height
                AVLTreeList.update_height(node_to_root)
            if node_to_root.parent != None and node_to_root.parent.parent == None:  # check if there is a new root after rotation
                self.root = node_to_root.parent
            node_to_root = old_parent  # update the node to its parent
        return res


    def update_fields(T,length,first,last,root):
        #updates the fields of the given tree T
        T.len=length
        T.first_node=first
        T.last_node=last
        T.root=root
        T.root.parent=None







    """searches for a value in the list

    @type val: str
    @param val: a value to be searched
    @rtype: int
    @returns: the first index that contains val, -1 if not found.
    """

    def search(self, val):
        res=AVLTreeList.listToArray(self)
        for i in range(res.length()):
            if(res[i]==val):
                return i
        return -1







    """returns the root of the tree representing the list

    @rtype: AVLNode
    @returns: the root, None if the list is empty
    """

    def getRoot(self):
        if self.empty():
            return None
        return self.root


