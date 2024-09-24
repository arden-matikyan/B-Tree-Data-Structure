from __future__ import annotations
import json
import math
from typing import List

# Node Class.
# You may make minor modifications.
class Node():
    def  __init__(self,
                  keys     : List[int]  = None,
                  children : List[Node] = None,
                  parent   : Node = None):
        self.keys     = keys
        self.children = children
        self.parent   = parent

# DO NOT MODIFY THIS CLASS DEFINITION.
class Btree():
    def  __init__(self,
                  m    : int  = None,
                  root : Node = None):
        self.m    = m
        self.root = None


    # DO NOT MODIFY THIS CLASS METHOD.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            return {
                "k": node.keys,
                "c": [(_to_dict(child) if child is not None else None) for child in node.children]
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)

    # Insert.
    def insert(self, key: int):

       
        # null root, insert first 
        if self.root is None: 
            self.root = Node([key], [None, None], None)
            return 
    
        self.insertAt(self.root, key)    

        return 

    def insertAt(self, root: Node, key: int): 
            current = root

            #print("inserting ", key,  " into ", root.keys)

            # check if current root has any children, if it doesn't then we can just insert into the node 
            if all(x is None for x in current.children): 
                ##print("no children")

                # we must insert the key in order to the current node 
                # append to list if needed 
                if current.keys[len(current.keys)-1] < key:
                    current.keys.append(key)
                else: # insert at front or mid-list 
                    for i in range(len(current.keys)):
                        if key < current.keys[i]:
                            current.keys.insert(i, key)
                            break

                current.children.append(None)

                # since we just added a key we need to check if the current node is overful (root/leaf overfull value is m keys)

                if len(current.keys) == self.m: 
                   ##print("overfull node!")
                    
                    # order of operations: left rot, right rot, split 

                    # No parent node (root) so we split 
                    if current.parent is None: 
                        #print("first Splitting ")
                        self.split(current)
                        return
                    else: 
                        
                        loc = current.parent.children.index(root)
                        
                        # if there is a left sibling we can check for a left rotation 
                        if loc != 0: 
                            # if left sibling is NOT full, we can do a left rotation 
                            if len(current.parent.children[loc-1].keys)+1 != self.m: 
                                #print("LEFT rot")
                                self.leftRotation(current)
                                return
                            # if there is a right sibling we can check for a right rotation 
                        if loc != len(current.parent.keys): 
                            #print("checking: ", current.parent.children[loc+1].keys)
                            if len(current.parent.children[loc+1].keys)+1 != self.m: 
                                #print("RIGHT ROT")
                                self.rightRotation(current)
                                return
                        
                        #print("last splitting")
                        self.split(current)
                
            else: # Current node has children, we must find which child to insert into 
                
                ##print("go to cild")
                # parent node is the current, will be autmatically updated if inserted at a lower level 
                parent = current 
                insertPosition = -1 

                # Search across keys of current node to determine child to go to 
                for i in range(len(current.keys)): 
                    # key to be inserted belongs at child i 
                    ##print(key)
                    if key < current.keys[i]: 
                        insertPosition = i 
                        break
                
                # inserts at the end 
                if insertPosition == -1: 
                    insertPosition = len(current.keys)

                # probably not needed but update parent     
                current.children[insertPosition].parent = current     

                self.insertAt(current.children[insertPosition], key)
            

    def split(self, root: Node): 
        

        # Split keys and children depending on even or odd 
        if self.m % 2 == 0: 
            median = self.m//2 - 1 
        else: 
            median = len(root.keys)//2
            
        medianKey = root.keys[median]
        leftKeys = root.keys[0:median]
        rightKeys = root.keys[median+1:len(root.keys)]

        leftChildren = root.children[0:median+1]
        rightChildren = root.children[median+1:len(root.children)]


        # at top of the tree, there needs to be a new root node 
        if root.parent is None: 
            
           #print("split again: ", root.keys)
            self.root = Node([medianKey],[],None)
            newParent = self.root

            leftChild = Node(leftKeys, leftChildren, newParent)
            rightChild = Node(rightKeys, rightChildren, newParent)
            

            if leftChildren[0] is not None: 
                for x in leftChild.children: 
                    x.parent = leftChild
            if rightChildren[0] is not None: 
                for x in rightChild.children: 
                    x.parent = rightChild   

            newParent.children.append(leftChild)
            newParent.children.append(rightChild)
            
            return 
        else: # median key needs to bubble up to parent.  

            #print("splitting ", root.keys)

            newParent = root.parent
            leftChild = Node(leftKeys, leftChildren, newParent)
            rightChild = Node(rightKeys, rightChildren, newParent)

            
            loc = newParent.children.index(root)


            del newParent.children[loc]
            newParent.children.insert(loc,leftChild) 
            newParent.children.insert(loc+1,rightChild)  
            
            ##print(newParent.keys)

            self.insertUp(newParent, medianKey)

            

            return 

        
            
    def rightRotation(self, current: Node): 
        
        # key to rotate up to the parent is the largest(last) of the keys 
        keyToGoUp = current.keys[-1]
   
        # we need to find the key in the parent that is rotated down, this will be the first key in the parent that is bigger than the key coming up 

        keyToGoDown = None 
        pKeys = current.parent.keys
        for i in range(len(pKeys)): 
            if pKeys[i] > keyToGoUp: 

                childToGoRight = current.children[-1]
                del current.children[-1]

                keyToGoDown = pKeys[i]
                pKeys[i] = keyToGoUp
                # we can insert the parent key coming down into the first key of the current nodes right sibling 
                current.parent.children[i+1].keys.insert(0,keyToGoDown)
                current.parent.children[i+1].children.insert(0,childToGoRight)
                break

        # rightmost case 
        if keyToGoDown is None:
            childToGoRight = current.children[-1]
            del current.children[-1]

            keyToGoDown = pKeys[-1]
            pKeys[-1] = keyToGoUp
            # we can insert the parent key coming down into the first key of the current nodes right sibling 
            current.parent.children[-1].keys.insert(0,keyToGoDown)
            current.parent.children[i].children.insert(0,childToGoRight)

       
        del current.keys[-1]

       ##print("Rotated Right")
       ##print(current.keys)
       ##print(current.parent.keys)



    def leftRotation(self, current: Node): 
            
        # key to rotate up to the parent is the smallest(first) of the keys 
        keyToGoUp = current.keys[0]
        ##print("keyToGoUp: ", keyToGoUp)

        # we need to find the key in the parent that is rotated down, this will be the rightmost key that is less than the key to go up
        keyToGoDown = None 
        pKeys = current.parent.keys
        for i in range(len(pKeys)-1, -1, -1): 
            if keyToGoUp > pKeys[i]:
                
                childToGoLeft = current.children[0]
                del current.children[0]

                keyToGoDown = pKeys[i]
                #print("replacing ", keyToGoDown, " with ", keyToGoUp)
                pKeys[i] = keyToGoUp
                
                current.parent.children[i].keys.append(keyToGoDown)
                current.parent.children[i].children.append(childToGoLeft)
                break
                

        del current.keys[0]


       ##print("Rotated Left")
       ##print(current.keys)
       ##print(current.parent.keys)



    def insertUp(self, root: Node, key: int):

        #print("inserting ", key,  " into ", root.keys)
        current = root 

        if current.keys[len(current.keys)-1] < key:
            current.keys.append(key)
        else: # insert at front or mid-list 
            for i in range(len(current.keys)):
                if key < current.keys[i]:
                    current.keys.insert(i, key)
                    break

        if len(current.keys) == self.m: 
           ##print("overfull node!")
            
            # order of operations: left rot, right rot, split 

            # No parent node (root) so we split 
            if current.parent is None: 
                #print("first Splitting")
                self.split(current)
                return
            else: 
                loc = current.parent.children.index(root)

                # if there is a left sibling we can check for a left rotation 
                if loc != 0: 
                    # if left sibling is NOT full, we can do a left rotation 
                    if len(current.parent.children[loc-1].keys)+1 != self.m: 
                        #print("LEFT rot")
                        self.leftRotation(current)
                        return
                    # if there is a right sibling we can check for a right rotation 
                if loc != len(current.parent.keys): 
                    #print("Checkingb: ", current.parent.children[loc+1].keys)
                    if len(current.parent.children[loc+1].keys)+1 != self.m: 
                        #print("RIGHT ROT")
                        self.rightRotation(current)
                        return 
                
                #print("last Splitting")
                self.split(current)




    # Delete.
    def delete(self, key: int):
        # Fill in the details.
        
       #print("del ", key)

       #print("root: ", self.root.children[0].children[1].parent.keys)







        # =================================================================================

        def inOrderSuccessor(root: Node, key: int) -> Node: 
            
            # right subtree 
            rst = root.children[root.keys.index(key)+1] 
            
            # root is the right subtree, go left as possible 
            while not all(x is None for x in rst.children):
                rst = rst.children[0]

            return rst

        # =================================================================================

        def checkUnderful(self, current: Node): 
            
            #print("CHECK underful: ", current.keys)

            underful = math.ceil(self.m/2)-2
            
            # if we are removing from the root, no resturcturing is needed
            if current.parent is not None: 
                
               ##print("not root")

                if len(current.keys) == underful: 
                    
                    #for i in range(len(current.parent.children)):
                       ##print(current.parent.children[i].keys)
                    loc = current.parent.children.index(current)
                    
                    ##print((current.parent.keys))
                    ##print(loc)

                    # 1. Use a right rotation if possible and effective.
                    # if current has a left sibling that can rotate right 
                    if loc != 0: 
                        # if the left sibling has a key it can give 
                        if len(current.parent.children[loc-1].keys)-1 > underful: 
                           #print("Doing a right rotate on the left sibling")
                            self.rightRotation(current.parent.children[loc-1])
                            return 

                    

                    # 2. Use a left rotation if possible and effective.
                    # if current has a right sibling that can left rotate 
                    if loc != len(current.parent.keys):
                        # if the right sibling has akey to give 
                        if len(current.parent.children[loc+1].keys)-1 > underful: 
                           #print("Doing a left rotate on the right sibling")
                            self.leftRotation(current.parent.children[loc+1])
                            return 


                    # Special Merge Case, if parent is single root ? 
                 
                    # 3. Merge with left sibling if possible and effective.
                    # check if left sibling exists 
                    if loc != 0: 
                        
                       #print("Merging with left sibling")
                        
                        # special case of single parent 

                        remParent = False 
                        if current.parent.parent is None:
                           #print("parent is root: ", current.parent.keys)
                            if len(current.parent.keys) == 1: 
                                
                                remParent = True 

                        # get left sibling and its children
                        
                        leftSiblingKeys = [] + current.parent.children[loc-1].keys
                        leftSiblingChildren = current.parent.children[loc-1].children

                        # get parent key value and remove it from the list 
                        parentToDrop = current.parent.keys[loc-1]
                        del current.parent.keys[loc-1]
                        del current.parent.children[loc-1]
                       
                        leftSiblingKeys.append(parentToDrop)
                        
                        leftSiblingKeys = leftSiblingKeys + current.keys 
                        current.keys = leftSiblingKeys 

                        newChildren = leftSiblingChildren + current.children
                        current.children = newChildren 

                        if remParent == True: 
                            #print("new root")
                            #print(current.keys)
                            current.parent = None
                            self.root.keys = current.keys
                            self.root.children = current.children

                        if current.parent is not None: 
                           ##print("check parent")
                            checkUnderful(self, current.parent)

                        return 
                        


                    # 4. Merge with right sibling if possible and effective
                    # check if right sibling exists 
                    if loc != len(current.parent.children):
                    
                        remParent = False 
                        if current.parent.parent is None:
                           #print("parent is roots")
                            if len(current.parent.keys) == 1: 
                                remParent = True 

                       #print("Merging with right")

                        # get right sibling and its children
                        rightSiblingKeys = [] + current.parent.children[loc+1].keys
                        rightSiblingChildren = current.parent.children[loc+1].children

                        # get parent key value and remove it from the list 
                        parentToDrop = current.parent.keys[loc]
                        del current.parent.keys[loc]
                        del current.parent.children[loc+1]


                        current.keys.append(parentToDrop)
                       
                        current.keys = current.keys + rightSiblingKeys
                        
                        current.children = current.children + rightSiblingChildren 

                        if remParent == True: 
                           #print("new root")
                           #print(current.keys)
                            current.parent = None
                            self.root.keys = current.keys
                            self.root.children = current.children

                        if current.parent is not None: 
                           ##print("checking with parent")
                            checkUnderful(self, current.parent)

                        return     

        # =================================================================================

        current = self.root 

       ##print("current: ", current.keys, "right child ", current.children[1].keys, " right child child: ", current.children[1].children[1].keys)
       ##print(":: ", current.children[1].children[1].parent.keys)


        # search the tree until we find the node of the key to delete 
        while key not in current.keys:

            # key isn't in current node, we must go down  
            if key > current.keys[-1]:
                current = current.children[-1]
            else: 
                for i in range(len(current.keys)):
                    if key < current.keys[i]:
                        current = current.children[i]
                        break 
            
            
        

        # current node contains the key to delete 
        
        # if current key is not in a leaf node 
        if not all(x is None for x in current.children): 
           ##print("not a leaf")
            node = inOrderSuccessor(current, key)
            replacementKey = node.keys[0]
            current.keys[current.keys.index(key)] = replacementKey

            current = node 
            key = replacementKey


        self.deleteFromLeaf(current, key)

   
        # now the leaf node is removed, we need to check if the node is underful 
        
        checkUnderful(self, current)

        return 
            


    def deleteFromLeaf(self, current: Node, key: int): 
        
       #print("deleting from node: ", current.keys, " key: ", key)

        # remove key from list 
        current.keys.remove(key)
        # Because we are deleting from a leaf, we know all the children are None, so we can just delete the last child in the list 
        current.children.pop()
        
        return 






















    # Search
    def search(self,key) -> str:
        
        path = [] 

        def searchNode(current: Node, ket: int):
            
            if key in current.keys: 
                return 
            else: 

                if key > current.keys[-1]: 
                    path.append(len(current.keys))
                    searchNode(current.children[len(current.keys)], key)
                else:    
                    for i in range(len(current.keys)):
                        if key < current.keys[i]:
                            path.append(i)
                            break
                    searchNode(current.children[i], key)
        
        searchNode(self.root, key)

        return json.dumps(path)