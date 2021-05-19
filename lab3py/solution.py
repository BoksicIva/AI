import sys
from id3 import ID3
from data import Dataframe
import copy


from numpy import log2 as log

# https://gist.github.com/rakendd/3e771b0de194d47b91595bd265945fc5#file-build_tree-py


# train = pd.read_csv (sys.argv[1])
# test = pd.read_csv (sys.argv[2])
model = ID3()
# a_entropy = {k:ent(train,k) for k in train.keys()[:-1]}
# print(a_entropy)


datafile = sys.argv[1]
dataset = Dataframe("")
dataset.read_data(dataset, datafile)


dataset_copy = Dataframe("")
dataset_copy.read_data(dataset_copy, datafile)
dataset.most_common_attribute=dataset.most_common(dataset)


root = model.fit(dataset,dataset_copy,dataset.attributes,dataset.target_attribute)
print("[BRANCHES]")
# model.traverse(root,"")
model.printAllRootToLeafPaths(root)

datafile_test = sys.argv[2]
dataset_test = Dataframe("")
dataset_test.read_data(dataset_test, datafile_test)

predictions=[]
for row in dataset_test.rows:
    predictions.append(model.predict(copy.copy(root),row,dataset.most_common_attribute))

print("[PREDICTIONS]: ", end="")
for predition in predictions:
    print(predition, end=" ")
print()
accuracy_score=model.accuracy_score(predictions,dataset_test.decisions)
print("[ACCURACY]: "+str(accuracy_score))

print("[CONFUSION_MATRIX]:")
confusion_matrix=model.confusion_matrix(predictions,dataset_test.decisions)





















# X_train = train.drop(train.columns[-1],axis=1)
# y_train = train[train.columns[-1]]
#
# X_test = test.drop(test.columns[-1],axis=1)
# y_test = test[test.columns[-1]]

#entropy_node=entropy_node(y_train)

# frequency = model.labels_frequency(train,y_train.name)
# return_column,keys,maxGain =model.max_gain(train,frequency,y_train)
# print(return_column)
# print(keys)
# print(maxGain)

# root = model.fit(train.copy(),train.copy(),train.columns.tolist(),y_train.name)
# model.traverse(root)
#print(frequency)


# root = model.fit(train,train,df.columns.tolist(),)

# return accuracy score
# y_pred = model.predict(X_test)
# model.accuracy_score(y_test, y_pred)


# print(train)
# print(test)