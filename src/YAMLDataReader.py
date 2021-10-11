from Types import DataType
from DataReader import DataReader
# import pyyaml module
import yaml
from yaml.loader import SafeLoader


class YAMLDataReader(DataReader):

    def __init__(self) -> None:
        self.key: str = ""
        self.students: DataType = {}

    def read(self, path: str) -> DataType:

        # Open the file and load the file
        with open(path) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            # print(data)
        for student in data:
            for name, subjects in student.items():
                self.key = name
                self.students[self.key] = []
                for subject, rating in subjects.items():
                    self.students[name].append((subject, int(rating)))
                    # print (name + " : " + str(subject) + " " + str(rating))

        return self.students
