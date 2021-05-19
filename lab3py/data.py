class Dataframe():
    def __init__(self, classifier):
        self.rows = []
        self.attributes = []
        self.target_attribute=[]
        self.target_index=0
        self.keys={}
        self.decisions=[]
        self.most_common_attribute={}


    def read_data(self, dataset, datafile):
        print
        "Reading data..."
        f = open(datafile)
        original_file = f.read()
        rowsplit_data = original_file.splitlines()
        dataset.rows = [rows.split(',') for rows in rowsplit_data]

        # list attributes
        dataset.attributes = dataset.rows.pop(0)

        #decistions for each row
        for row in dataset.rows:
            dataset.decisions.append(row.__getitem__(len(row)-1))

        dataset.target_index=len(dataset.attributes) - 1
        dataset.target_attribute= dataset.attributes.pop(dataset.target_index)

        for i in range(0,len(dataset.attributes)):
            dataset.keys[dataset.attributes.__getitem__(i)]=i

        # create array that indicates whether each attribute is a numerical value or not

    def most_common(self,dataset):
        most_common_atributes={}
        for attribute in dataset.keys:
            index=dataset.keys[attribute]
            values={}
            for row in dataset.rows:
                # key = data[i][column]
                key = row[index]
                if key not in values:
                    values[key] = 1
                else:
                    values[key] += 1
            max=0
            maxkey=""
            for key in values:
                if values[key] > max or (values[key] == max and key < maxkey):
                    max=values[key]
                    maxkey=key

            most_common_atributes[attribute]=maxkey

        return most_common_atributes
