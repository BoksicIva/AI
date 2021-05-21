from node import Node
from math import log2 as log
import copy

vec = []


# https://www.geeksforgeeks.org/print-all-root-to-leaf-paths-of-an-n-ary-tree/


class ID3():

    def __init__(self):
        pass


    def max_frequency(self, frequency):
        return max(frequency, key=lambda k: frequency[k])

    def labels_frequency(self, dataframerows, index):
        frequency = {}

        for row in dataframerows:

            value = row.__getitem__(index)
            if value in frequency:
                frequency[value] += 1
            else:
                frequency[value] = 1

        sortedDict = dict(sorted(frequency.items(), key=lambda x: x[0].lower()))
        return sortedDict

    def labels_frequency_key(self, dataframerows, index, key, target_index):
        frequency = {}

        for row in dataframerows:
            if row.__getitem__(index) == key:
                value = row.__getitem__(target_index)
                if value in frequency:
                    frequency[value] += 1
                else:
                    frequency[value] = 1

        sortedDict = dict(sorted(frequency.items(), key=lambda x: x[0].lower()))
        return sortedDict

    def fit(self, D, D_parent, X, y):

        frequency = self.labels_frequency(D_parent.rows, D_parent.target_index)

        node = Node()
        node.children = []

        if not D.rows :
            node.leaf = True
            node.decision = self.max_frequency(frequency)
            return node

        frequency = self.labels_frequency(D.rows, D.target_index)

        if not X or  len(frequency.keys()) == 1:  # savrsena podjela da je sve "DA" ili sve "NE" ili ne postoji vise atributa po kojima se dijeli
            node.decision = self.max_frequency(frequency)
            node.leaf = True
            return node

        x,V_x, gain, index = self.max_gain(D, frequency, y)

        node.feature_name = x
        list_of_attributes=copy.copy(X)
        if x in list_of_attributes:
            list_of_attributes.remove(x)


        for v in V_x:
            node2 = Node()
            node2.feature_value = v
            node2.feature_name = x
            newrows = []

            for row in D.rows:

                if row[index] == v:
                    newrows.append(row)
            Dnew = copy.copy(D)

            Dnew.rows = newrows
            Dnew.attributes=list_of_attributes

            new_node = self.fit(Dnew, D, Dnew.attributes, y)

            node2.children.append(new_node)
            node.children.append(node2)

        return node

    def fit2(self, D, D_parent, X, y, depth,inner_depth):

        frequency = self.labels_frequency(D_parent.rows, D_parent.target_index)

        node = Node()
        node.children = []
        node.depth=inner_depth

        if not D.rows or node.depth == depth:
            node.leaf = True
            node.decision = self.max_frequency(frequency)
            return node

        frequency = self.labels_frequency(D.rows, D.target_index)

        if not X or len(frequency.keys()) == 1:  # savrsena podjela da je sve "DA" ili sve "NE"
            node.decision = next(iter(frequency.keys()))
            node.leaf = True
            return node

        x, V_x ,gain, index = self.max_gain(D, frequency, y)
        node.feature_name = x
        list_of_attributes = copy.copy(X)
        if x in list_of_attributes:
            list_of_attributes.remove(x)


        for v in V_x:
            node2 = Node()
            node2.feature_value = v
            node2.feature_name = x
            node2.depth = node.depth+1
            newrows = []
            for row in D.rows:

                if row[index] == v:
                    newrows.append(row)
            Dnew = copy.copy(D)
            Dnew.rows = newrows
            Dnew.attributes = list_of_attributes
            if node.depth +1== int(depth):
                node.children.append(node2)
                node3 = Node()
                node3.leaf = True

                frequency3 = self.labels_frequency(Dnew.rows, Dnew.target_index)
                node3.decision = self.max_frequency(frequency3)
                node2.children.append(node3)
                continue

            new_node = self.fit2(Dnew, D, Dnew.attributes, y, depth,inner_depth+1)
            new_node.depth = node.depth + 2
            node2.children.append(new_node)
            node.children.append(node2)

        return node

    def predict(self, node, row, keys,dataset):
        while not node.leaf:
            if not node.feature_value:
                found = False
                for child in node.children:
                    if not found and child.feature_value == row[keys[child.feature_name]]:
                        node = child
                        found = True

                        newrows = []
                        for train_row in dataset.rows:

                            if child.feature_value == train_row[keys[child.feature_name]]:
                                newrows.append(train_row)

                        dataset.rows = newrows
                if not found:
                    frequency = {}
                    for train_row in dataset.rows:
                        value = train_row[dataset.target_index]
                        if value in frequency:
                            frequency[value] += 1
                        else:
                            frequency[value] = 1
                    sortedDict = dict(sorted(frequency.items(), key=lambda x: x[0].lower()))

                    return max(sortedDict, key=lambda k: sortedDict[k])

            else:
                node = node.children[0]

        return node.decision




    def printPath(self, vec):
        for ele in vec:
            print(ele, end=" ")

        print()

    def printAllRootToLeafPaths(self, root):

        global vec

        if (not root):
            return

        if root.feature_value:
            vec.append(str(vec.__len__() + 1) + ":" + root.feature_name + "=" + root.feature_value)


        if (len(root.children) == 0):
            vec.append(root.decision)
            self.printPath(vec)
            vec.pop()
            return

        for i in range(len(root.children)):
            self.printAllRootToLeafPaths(root.children[i])


        if vec and root.feature_value:
           vec.pop()

    def accuracy_score(self, predictions, decision):
        num_data = len(decision)
        num_correct = 0

        for index in range(0, len(decision)):
            if predictions[index] == decision[index]:
                num_correct += 1

        return round(num_correct / num_data, 5)

    def entropy(self, frequency):
        entropy = 0
        sum = 0
        for key in frequency:
            sum += frequency[key]

        for key in frequency:
            x = frequency[key] / sum
            entropy -= x * log(x)

        return entropy

    def confusion_matrix(self, predictions, decision):
        mylist = list(set(predictions + decision))
        mylist = sorted(mylist)

        index = 0
        dictionary = {}
        for value in mylist:
            dictionary[value] = index
            index += 1

        n = len(mylist)

        matrix = [[0 for x in range(n)] for y in range(n)]

        for index in range(0, len(predictions)):
            for key in dictionary:
                if predictions[index] == key:
                    index1 = dictionary[key]
                if decision[index] == key:
                    index2 = dictionary[key]
            matrix[index2][index1] += 1

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
        return_index = 0
        gain_attributes={}

        for attribute in data.attributes:
            index = data.keys[attribute]
            values = {}
            for row in data.rows:
                key = row[index]
                if key not in values:
                    values[key] = 1
                else:
                    values[key] += 1
            gain = entropy

            for key in values:
                frequency_of_labels = self.labels_frequency_key(data.rows, index, key, data.target_index)
                new_entorpy = self.entropy(frequency_of_labels)
                gain -= values[key] * new_entorpy / len(data.rows)

            gain_attributes[attribute]=gain
            if gain > maxGain or len(data.attributes)==1 or (gain == maxGain and return_col!= "" and return_col > attribute) or (gain==0 and return_col== ""):
                maxGain = gain
                return_col = attribute
                keys = sorted(values.keys())
                return_index = index

        gain_attributes=dict(sorted(gain_attributes.items(), key=lambda item: format(item[1],'.4f'),reverse=True))
        for key in gain_attributes:
            print("IG("+key+")="+str(format(gain_attributes[key],'.4f')),end=" ")
        print()

        return return_col,list(keys), maxGain, return_index
