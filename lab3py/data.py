class Dataframe():
    def __init__(self):
        self.rows = []
        self.attributes = []
        self.target_attribute = []
        self.target_index = 0
        self.keys = {}
        self.decisions = []

    def read_data(self, dataset, datafile):
        f = open(datafile)
        original_file = f.read()
        rowsplit_data = original_file.splitlines()
        dataset.rows = [rows.split(',') for rows in rowsplit_data]

        # list attributes
        dataset.attributes = dataset.rows.pop(0)

        for row in dataset.rows:
            dataset.decisions.append(row.__getitem__(len(row) - 1))

        dataset.target_index = len(dataset.attributes) - 1
        dataset.target_attribute = dataset.attributes.pop(dataset.target_index)

        for i in range(0, len(dataset.attributes)):
            dataset.keys[dataset.attributes.__getitem__(i)] = i

        dataset.keys = dict(sorted(dataset.keys.items(), key=lambda x: x[0].lower()))
