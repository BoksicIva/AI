import sys
from id3 import ID3
from data import Dataframe
import copy

model = ID3()

datafile = sys.argv[1]
dataset = Dataframe("")
dataset.read_data(dataset, datafile)


dataset_copy = Dataframe("")
dataset_copy.read_data(dataset_copy, datafile)



if len(sys.argv) ==3:
    root = model.fit(dataset,dataset_copy,dataset.attributes,dataset.target_attribute)
    print("[BRANCHES]:")
else:

    root = model.fit2(dataset,dataset_copy,dataset.attributes,dataset.target_attribute,sys.argv[3],0)
    print("[BRANCHES]:")



model.printAllRootToLeafPaths(root)

datafile_test = sys.argv[2]
dataset_test = Dataframe("")
dataset_test.read_data(dataset_test, datafile_test)

predictions=[]
for row in dataset_test.rows:
    predictions.append(model.predict(copy.copy(root),row,dataset_test.keys,copy.copy(dataset)))

print("[PREDICTIONS]: ", end="")
for predition in predictions:
    print(predition, end=" ")
print()
accuracy_score=model.accuracy_score(predictions,dataset_test.decisions)
print("[ACCURACY]: "+str(format(accuracy_score, '.5f')))

print("[CONFUSION_MATRIX]:")
confusion_matrix=model.confusion_matrix(predictions,dataset_test.decisions)













