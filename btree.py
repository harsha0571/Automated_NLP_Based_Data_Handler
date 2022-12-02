# BTree is a self balancing tree, that can have multiple keys stored in a single node.
# Upon insertion of a new key, the arrangement of keys and nodes are automatically handled.
# For an order 'n', there can be a maximum of '2*n' keys in a node.
# Once a node contains 2n keys, it performs self balancing by creating a new node as its parent.
# The parent node will take the median of the previous node.
# The left and right of the median will become the left and right child node.
# A node can have at most (2*n)-1 children.
# All intermediate node i.e except the last node have exactly n-1 keys

# Node
class Node:
    def __init__(self,leaf=False):
        self.leaf= leaf
        self.keys= []
        self.child= []

# Btree
class BTree:
    def __init__(self, t):
        self.root = Node(True)
        self.t= t

    # Node Insertion
    def insert(self, k):
        root= self.root
        # if the no. of keys in the node is equal to n-1 children
        # create a new node
        if len(root.keys) == (2*self.t)-1:
            temp = Node()
            # make the new node, the parent node
            self.root = temp
            # add the previous root of tree as the left child
            temp.child.insert(0, root)
            # split the left child
            self.split_child(temp,0)
            # add the required key in the non empty node
            self.insert_non_full(temp, k)
        else:
            self.insert_non_full(root, k)
    
    # Insert key into non full node
    def insert_non_full(self, x, k):
        # find the index of the last key in the given node x
        i = len(x.keys) - 1
        # check if the given node does not have any children
        if x.leaf:
            # add an empty (index,key) pair in the keys list
            x.keys.append((None, None))
            # while a key exist and the key to be inserted
            # is lesser than the previous keys
            while i>= 0 and k[0] < x.keys[i][0]:
                # move from last node to its left till new key
                # is found to be greater than the key on its left
                # or is on the leftmost end
                # this is doen to maintain the keys in increasing order
                x.keys[i+1]= x.keys[i]
                i-=1
            x.keys[i+1]= k
        # if the node has children nodes
        else:
            # find the index where the new key satisfy the 
            # increasing order
            while i>=0 and k[0] < x.keys[i][0]:
                i-=1
            i+=1
            # checking if the leftmost child of the i th index
            # has a full key list
            if len(x.child[i].keys) == (2*self.t) - 1:
                # split the node child a index i
                self.split_child(x,i)
                if k[0] > x.keys[i][0]:
                    i+=1
            # insert the key in the child node
            self.insert_non_full(x.child[i],k)

    # split the keys in the i th child node into left and right
    def split_child(self, x, i):
        t = self.t
        y = x.child[i]
        z = Node(y.leaf)
        x.child.insert(i+1,z)
        # inserting the median key of the child node to the
        # parent node's keys
        x.keys.insert(i, y.keys[t-1])
        # slicing keys in right and left node respectively
        # number of keys= number of children-1
        z.keys= y.keys[t:(2*t)-1]
        y.keys= y.keys[0:t-1]
        # slicing children 
        if not y.leaf:
            z.child= y.child[t:2*t]
            y.child= y.child[0:t]
    
    # to search a key in the btree
    # k:- key to be searched
    # x:- the node to searched
    def search_key(self, k, x=None):
        # if the node does exist:
        if x is not None:
            # initializing index for traversal
            i= 0
            # while index is valid and key is greater than the keys
            # mentioned int the node
            # increase the index to traverse the right
            while i<len(x.keys) and k>x.keys[i][0]:
                i+= 1
            # if the index is still valid and the key is found
            if i< len(x.keys) and k==x.keys[i][0]:
                return (x,i)
            # if the key is not found in this node
            # and the node is a leaf node, the key does not exist
            elif x.leaf:
                return None
            # the key is not found in this node but it has a child node.
            # Either i>len(keys) i.e it is pointing to the rightmost child
            # node that has keys > keys in the parent node.
            # Or the key is found from which the argument key is lesser in
            # value. We move to the left child node of that key for searching.
            # child node that contains key greater thean the paren
            else:
                return self.search_key(k, x.child[i])
        else:
            return self.search_key(k, self.root)

    # x:- node, l:- level
    # prints tree elements with labels like level and number of keys in each node
    def print_tree(self, x, l=0):
        print("Level ", l, " ", len(x.keys), end=":")
        for i in x.keys:
            print(i, end=" ")
        print()
        l+=1
        if len(x.child) > 0:
            for i in x.child:
                self.print_tree(i,l)

    # prints tree in pair of parent and children node as lists
    # will be used for storing the btree in the files
    def print(self,x):
        # print(x.leaf)
        if len(x.keys)>0:
            print(x.keys)
        if len(x.child)>0:
            li= [fe.keys for fe in x.child]
            print(li)
    
    # uses the above print method and redirect the content to a file 
    # will write a parent (x) and children nodes in a file at a time
    def saveInFile(self,x):
        f= open('./data/btree.txt','w')
        from contextlib import redirect_stdout
        with redirect_stdout(f):
            self.localStore(x)

    # stores all the nodes in a file as parent and children node pairs
    def localStore(self, x):
        self.print(x)
        if not x.leaf and len(x.child)>0:
            # print('\n')
            set= x.child
            for children in set:
                if not children.leaf:
                    self.localStore(children)