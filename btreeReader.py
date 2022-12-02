# Sample Btree stored in txt file
# [(8, 16)]
# [[(2, 4), (5, 10)], [(11, 22), (14, 28)]]
# [(2, 4), (5, 10)]
# [[(0, 0), (1, 2)], [(3, 6), (4, 8)], [(6, 12), (7, 14)]]
# [(11, 22), (14, 28)]
# [[(9, 18), (10, 20)], [(12, 24), (13, 26)], [(15, 30), (16, 32), (17, 34), (18, 36), (19, 38)]]

# The below code is used to parse the file storing the btree information without creating another BTree Data Structure

import ast          #used for converting a string into their corresponding data types          
import linecache    #used for reading files with offsetting index

resultList= []

# for each document id mentioned in csv format taken as input
# the data will be converted into tuple or integer
inp= ast.literal_eval(input('Please enter the documents to be searched!!').replace(' ',''))
print(inp)

# if the input data is in integer format, convert it into list else take it as tuple
docids= inp if isinstance(inp, tuple) else [inp]

# function to search a document in the btree file
def findDoc(docid, parent, children, line=2):
    if docid in parent or docid in children:
        print(docid)
    else:
        # initial index to be traversed as i
        i=0
        # for each keys in the parent node
        for key in parent:
            # if the document id is found, print it and end the function
            print(key[0], docid)
            if docid == key[0]:
                resultList.append(docid)
                print(docid)
                return
            # if the id is lesser than the key traversing from left
            # check if the node has children or not
            # if children exist, reasssign the children node at index i from list of list as the new parent
            # linecache can retrieve a particular line from the file
            # the children node of the new parent node exist at an offset of '(i*2)+2'
            # search for the document in that parnet child pair
            # if the childrent does not exist, print that the document is not found and exit the function
            if docid<key[0]:
                print('child node to be reffered: ',children[i])
                if len(children)>0:
                    parent= children[i]
                    children= linecache.getline('./data/btree.txt', line+((i*2)+2))
                    children= [] if children=='' else ast.literal_eval(children.replace('\n',''))
                    findDoc(docid, parent, children, line+((i*2)+2)) 
                    break
                else:
                    print(docid,'not found')
                    continue
            i+=1
        # if the end of the keys in a node is reached i.e. i== total number of keys in the parent node
        # take the last child node as the new parent node
        if (isinstance(children,list) or isinstance(children,tuple)) and i==len(parent):
            parent= children[i] if len(children)>0 else []
            if len(parent)==0:
                print(docid,'not found')
            else:
                children= linecache.getline('./data/btree.txt', line+((i*2)+2))
                children= [] if children=='' else ast.literal_eval(children.replace('\n',''))
                findDoc(docid, parent, children, line+((i*2)+2))
    

# print(docids)
for docid in docids:
    # treeSamp= btree.BTree(3)
    inputFile= open('./data/'+'btree'+'.txt','r')
    parent= ast.literal_eval(inputFile.readline().replace('\n',''))
    children= ast.literal_eval(inputFile.readline().replace('\n',''))
    findDoc(docid,parent,children)
    print(resultList)