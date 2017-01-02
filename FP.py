import collections
import itertools
import os
import operator

'''Ulrik Soderstrom
CSC 440
10/24/16
FP-Growth Algorithm'''

min_sup = input("Please enter an integer value support count: ")

path = input("Enter path to a folder with data ")
os.chdir(path)

filename = input("Enter a filename of data set in folder ")

Data_File = open(path + "/" + filename, "r")

Item_Set = []
PreSorted = []
frequency = []

#Append data from file to list 
for line in Data_File:
        line_list = [x.strip(",") for x in line.lower().split()]
        Item_Set.append(line_list)
print("1. Appending data from file")

#Append data from tuples into list form tuples -- O(n)

for i in range(0, len(Item_Set)):
    for j in range(0, len(Item_Set[i])):
        #print(Item_Set[i])
        PreSorted.append(Item_Set[i][j])

#Sort item types based on count -- O(n) and remove items below minimum support 
counts = collections.Counter(PreSorted)

Removable = []
Items_worth_checking = []

for item in counts:
    if counts[item] < min_sup:
        Removable.append(item)
    if counts[item] > min_sup:
        Items_worth_checking.append(item)

new_list = sorted(PreSorted, key=counts.get, reverse=True)

for item in new_list:
    if item not in frequency:
        frequency.append(item)

Sorted = [[] for i in range(len(Item_Set))]


print("2. Sorting tuples based on Priority")

#Sort tuples based on items frequency 
[sorted(x,key=frequency.index) for x in Item_Set]



'''for j in range(0, 15):
        for i in range(0, len(Item_Set)):
                Sorted[i].append(Item_Set[i][j]) '''

for i in range(0, len(Item_Set)):
    for j in range(0, len(Item_Set[i])):
        Sorted[i].append(Item_Set[i][j]) 

print("3. Generating FP-Growth Tree")

#Tree
class Node:
    def __init__(self, name, parent):
        self.name = name
        self.count = 1
        self.parent = parent
        self.children = []

    def add_child(self, name, parent):  
        new_node = Node(name, parent)
        parent.children.append(new_node)
        return 

    def add_FPchild(self, name, parent):  
        index = len(parent.children)
        parent.add_child(name, parent)
        return 

    def add_FPTuple(self, itemset, parent):
        for item in itemset: 
            for child in parent.children:
                if item == child.name:
                    child.count += 1
                    itemset.remove(item)
                    return self.add_FPTuple(itemset, child)
            self.add_FPchild(item, parent)
            itemset.remove(item)
            return self.add_FPTuple(itemset, parent.children[len(parent.children)-1])

    def display_tree(self, parent):
        print("\n")
        print(parent.name) 
        print(" has a count of ")
        print(parent.count)
        print(" is parent of ")
        print(len(parent.children))
        print(" children named ")
        for child in parent.children:
            print(child.name)
            print("with a count of ")
            print(child.count)
        for i in xrange(0,len(parent.children)):
            FPTree.display_tree(parent.children[i])
        
    def find_count_parent_by_name(self, name, parent, branch, branches):
        if parent.name != "root":
            branch.append(parent.name)
            branch.append(parent.count)
        if len(parent.children) == 0:
                branch.pop()
                branch.pop()
        for child in parent.children:
            if child.name == name:
                branch.append(child.name)
                branch.append(child.count)
                branches.append(branch[:])
                branch.pop()
                branch.pop()
        for i in xrange(0, len(parent.children)):
            if i == (len(parent.children)-1) and parent.name != "root":
                branch.pop()
                branch.pop()
            self.find_count_parent_by_name(name, parent.children[i], branch, branches)
        return branches

#Generate FPTree
FPTree = Node("root", None)

for itemset in Sorted:
    FPTree.add_FPTuple(itemset, FPTree)

print("4. Tree Generated")

Condition_itemsets = []
branch = []

#Generate rules from FP-Tree 
print("5. Taversing tree for conditional itemsets")

Condition_itemsets = []
branch = []

Frequent_Itemsets = {}

for sets in Items_worth_checking: 
    Condition_itemsets = []
    Condition_itemsets = FPTree.find_count_parent_by_name(sets, FPTree, branch, Condition_itemsets)

    for i in xrange (0, len(Condition_itemsets)):
        if len(Condition_itemsets[i]) > 2:
            freq = min(Condition_itemsets[i])
            Condition_no_freq = [x for x in Condition_itemsets[i] if not isinstance(x, int)]
            for L in range(2, len(Condition_no_freq)+1):
                for subset in itertools.combinations(Condition_no_freq, L):
                    if sets in subset:
                        if subset in Frequent_Itemsets:
                            Frequent_Itemsets[subset] = (freq+Frequent_Itemsets[subset])
                        else: Frequent_Itemsets[subset] = freq

counter = collections.Counter()
for d in Frequent_Itemsets:
    counter.update(d)

Frequent_Itemsets = {k: v for k, v in Frequent_Itemsets.iteritems() if v > min_sup}
Sorted_Frequent_Itemsets = sorted(Frequent_Itemsets.items(), key=operator.itemgetter(1))

print("6. Completed! Frequent Itemsets:")
print(Sorted_Frequent_Itemsets)
