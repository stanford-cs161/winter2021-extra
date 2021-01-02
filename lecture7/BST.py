# This is a Node class for our BST.  
# Nodes have a key and an optional value and color, and pointers to left and right children, as well as to their parent.
# A node is also a BST, that it is the root of.
class Node:
    def __init__(self,k,v=None,color="red"):
        self.key = k
        self.value = v
        self.leftChild = None
        self.rightChild = None
        self.parent = None
        self.color = color
    
    def __str__(self):
        return str(self.key)
        
    # Node helper functions
    def setChild(self, n, whichChild):
        if whichChild == "left":
            self.leftChild = n
        elif whichChild == "right":
            self.rightChild = n
            
    def setParent(self,n):
        self.parent = n
        
    def isLeaf(self):
        if self.leftChild == None and self.rightChild == None:
            return True
        return False

    def numChildren(self):
        if self.isLeaf():
            return 0
        if self.rightChild == None or self.leftChild == None:
            return 1
        return 2
        
    # Now the BST things that we'll need.
    def search(self,k):
        if k == self.key:
            return self # found it!
        if k < self.key:
            if self.leftChild != None:
                return self.leftChild.search(k)
            return self
        if k > self.key:
            if self.rightChild != None:
                return self.rightChild.search(k)
            return self
    
    def insert(self,n):
        r = self.search(n.key)
        if r.key == n.key:
            print("Need distinct keys.")
            return None
        if r.key < n.key:
            r.setChild(n, "right")
            n.setParent(r)
        if r.key > n.key:
            r.setChild(n, "left")
            n.setParent(r)
            
    # deletes a node underneath self with key value k, if it exists.
    # returns (new root, deleted node)  
    # deleted node is None if it was not found.
    # new root is equal to self unless we delete the root.
    def delete(self,k):
        r = self.search(k)
        if r.parent == None:
            whichChild = None
        elif r.key < r.parent.key:
            whichChild="left"
        else:
            whichChild="right"
            
        if r.key != k:
            # then r wasn't found.
            return self, None
        elif r.isLeaf():
            if whichChild != None:
                r.parent.setChild(None, whichChild)
                return self, r
            else:
                return None, self # we deleted the root and there's nothing left.
        elif r.leftChild != None and r.rightChild == None:
            replacement = r.leftChild
            if whichChild != None:
                r.parent.setChild(r.leftChild, whichChild)
            r.leftChild.setParent( r.parent )
            if whichChild != None:
                return self, r
            else:
                return replacement, r
        elif r.rightChild != None and r.leftChild == None:
            replacement = r.rightChild
            if whichChild != None:
                r.parent.setChild(r.rightChild, whichChild)
            replacement.setParent( r.parent )
            if whichChild != None:
                return self, r
            else:
                return replacement, r
        else: # then r has two children
            successor = r.rightChild.search(k)
            r.rightChild.delete( successor.key ) 
            # this will be one of the other two cases, so we'll never recurse too deep
            if whichChild != None:
                r.parent.setChild(successor, whichChild )
            successor.parent.setParent( r.parent )
            successor.setChild( r.leftChild, "left" )
            successor.setChild( r.rightChild, "right" )
            if whichChild != None:
                return self,r
            return successor, r
        
            
def prettyPrint(r,maxLevel=5):
    Q = [r]
    lvl = 0
    count = 0
    spacing = 32
    while lvl < maxLevel:
        n = Q.pop(0)
        if n == None:
            print(" "*spacing, end="")
            print( "-", end="")
            count += 1
            Q.append(None)
            Q.append(None)
        else:
            print(" "*spacing, end="")
            print(n.key, end="" )
            count += 1
            L = n.leftChild
            R = n.rightChild
            Q.append(L)
            Q.append(R)
        if count >= 2**lvl:
            print("\n\n")
            spacing = int(spacing/1.65)  
            lvl += 1
            count = 0
 
        
        
        

        
    
        
        
            
        
