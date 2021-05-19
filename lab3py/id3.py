from node import Node
from numpy import log2 as log
import copy
vec = []

# https://github.com/danielpang/decision-trees/blob/master/learn.py
# https://github.com/stratzilla/id3-decision-tree/blob/master/id3_tree.py

# https://github.com/tofti/python-id3-trees/blob/master/id3.py

#https://www.geeksforgeeks.org/print-all-root-to-leaf-paths-of-an-n-ary-tree/



class ID3():

    def __init__(self):
        pass

    def argmax(self, D_parent, frequency):
        entropy = self.entropy(frequency)

    ## TOOOOOOODOOOOOOOOOOOO
    ## provjeri jel vraca prvu abecednu vrijednost
    def max_frequency(self, frequency):
        return max(frequency, key=lambda k: frequency[k])

    def make_split(df, t):
        """
        Splits a dataframe on attribute.

        Parameter:
        df -- the dataframe to split
        t -- target attribute to split upon

        Return:
        new_df -- split dataframe
        """
        new_df = {}
        for df_key in df.groupby(t).groups.keys():
            new_df[df_key] = df.groupby(t).get_group(df_key)
        return new_df

    def labels_frequency(self, dataframerows, index):
        frequency = {}

        for row in dataframerows:

            value = row.__getitem__(index)
            if value in frequency:
                frequency[value] += 1
            else:
                frequency[value] = 1

        #sort = sorted(frequency.keys(), key=lambda x: x.lower())
        sortedDict = dict(sorted(frequency.items(), key=lambda x: x[0].lower()))
        return sortedDict

    def labels_frequency_key(self, dataframerows, index,key,target_index):
        frequency = {}

        for row in dataframerows:
            if row.__getitem__(index)==key:
                value = row.__getitem__(target_index)
                if value in frequency:
                    frequency[value] += 1
                else:
                    frequency[value] = 1

        sortedDict = dict(sorted(frequency.items(), key=lambda x: x[0].lower()))
        return frequency

    def fit(self, D, D_parent, X, y):

        frequency = self.labels_frequency(D_parent.rows, D_parent.target_index)


        node = Node()
        node.children=[]

        if not D.rows:
            node.leaf = True
            node.decision = self.max_frequency(frequency)
            return node

        frequency = self.labels_frequency(D.rows, D.target_index)


        if not X or len(frequency.keys()) == 1:  # savrsena podjela da je sve "DA" ili sve "NE"
            node.decision = next(iter(frequency.keys()))
            node.leaf = True
            return node


        x, V_x, gain,index = self.max_gain(D, frequency,y)
        node.feature_name = x
        X.remove(x)
        subtrees = {}
        for v in V_x:
            # new_node=Node()
            # new_node.feature_name=x
            # new_node.feature_value=v
            node2=Node()
            node2.feature_value=v
            node2.feature_name = x
            newrows = []
            for row in D.rows:

                if row[index] == v:
                    newrows.append(row)
            Dnew=copy.copy(D)

            Dnew.rows=newrows
            new_node = self.fit(Dnew, D,X, y)
            node2.children.append(new_node)
            node.children.append(node2)

        return node

    def predict(self, node, row,most_common_atributes):
        while not node.leaf:
            if not node.feature_value:
                found= False
                for child in  node.children:
                    if not found and child.feature_value in row:
                        node=child
                        found = True
                if not found:
                    most_common=most_common_atributes[node.feature_name]
                    for child in node.children:
                        if  child.feature_value == most_common:
                            node = child
            else:
                node=node.children[0]
        return node.decision





    def traverse(self, root,path=""):

        if(root.feature_value):
            path+=root.feature_name+"="+root.feature_value
            print(path,end=" ")
        if root.decision:
            print(root.decision)
        n = len(root.childern)
        if n > 0:
            for i in range(0, n):
                self.traverse(root.childern[i])
        else:
            path=""

    def traverse2(self, root):

        print(root.feature_name + "=" + root.feature_value, end=" ")
        if root.decision:
            print(root.decision)
        n = len(root.childern)
        if n > 0:
            for i in range(0, n):
                self.traverse(root.childern[i])

    def printPath(self,vec):

        # Print elements in the vector
        for ele in vec:
            print(ele, end=" ")

        print()

    def printAllRootToLeafPaths(self,root):

        global vec

        # If root is null
        if (not root):
            return

        # Insert current node's
        # data into the vector
        if root.feature_value:
            vec.append(str(vec.__len__()+1)+":"+root.feature_name+"="+root.feature_value)

        # If current node is a leaf node
        if (len(root.children) == 0):
            # Print the path
            vec.append(root.decision)
            self.printPath(vec)
            # Pop the leaf node
            # and return
            vec.pop()
            return

        # Recur for all children of
        # the current node
        for i in range(len(root.children)):
            # Recursive Function Call
            self.printAllRootToLeafPaths(root.children[i])
        if vec:
            vec.pop()


    def accuracy_score(self, predictions, decision):
        num_data = len(decision)
        num_correct = 0

        for index in range(0,len(decision)) :
            if predictions[index] == decision[index]:
                num_correct += 1

        return round(num_correct / num_data, 5)

    def entropy(self, frequency):
        entropy=0
        sum=0
        for key in frequency:
            sum+=frequency[key]

        for key in frequency:
            x=frequency[key]/sum
            entropy -= x * log(x)
        # x = frequency["yes"] / (frequency["no"] + frequency["yes"])
        # y = frequency["no"] / (frequency["no"] + frequency["yes"])
        #
        # entropy = -1 * (x * log(x) + y * log(y))
        return entropy

    def confusion_matrix(self,predictions,decision):
        mylist = list(set(predictions+decision))
        mylist=sorted(mylist)
        print(mylist)

        index=0
        dictionary={}
        for value in mylist:
            dictionary[value]=index
            index+=1

        print(dictionary)

        n= len(mylist)

        matrix = [[0 for x in range(n)] for y in range(n)]

        for index in range(0,len(predictions)):
            for key in dictionary:
                if predictions[index] ==key:
                    index1=dictionary[key]
                if decision[index]==key:
                    index2=dictionary[key]
            matrix[index2][index1]+=1

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                print(matrix[i][j], end=' ')
            print()


    def max_gain(self, data, frequency, y):
        global return_column
        entropy = self.entropy(frequency)
        maxGain = 0
        return_col = ""
        keys = []
        return_index=0

        for attribute in data.keys:
            index=data.keys[attribute]
            values = {}
            for row in data.rows:
                # key = data[i][column]
                key = row[index]
                if key not in values:
                    values[key] = 1
                else:
                    values[key] += 1
            gain = entropy

            # for key in values:
            #     yes = 0
            #     no = 0
            #     for row in data.rows:
            #         # print(data[data.columns[-1]])
            #         # print(data[data.columns.get_loc(data[-1].name)])
            #         if row[index] == key:
            #             if row[-1] == "yes":
            #                 yes += 1
            #             else:
            #                 no += 1
            #     x = yes / (yes + no)
            #     y = no / (yes + no)
            #     if x != 0 and y != 0:
            #         gain += (values[key] * (x * log(x) + y * log(y))) / len(data.rows)

            for key in values:
                frequency_of_labels=self.labels_frequency_key(data.rows,index,key,data.target_index)
                new_entorpy=self.entropy(frequency_of_labels)
                gain-=values[key]*new_entorpy/len(data.rows)


            if gain > maxGain:
                maxGain = gain
                return_col = attribute
                keys = values.keys()
                return_index = index

        return return_col, list(keys), maxGain, return_index
