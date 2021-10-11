from typing import Dict
from Types import DataType

RatingType = Dict[str, float]


class CheckAll90Ratings():

    def __init__(self, data: DataType) -> None:
        self.data: DataType = data
        self.rating: RatingType = {}

    def calc(self) -> RatingType:
        for key in self.data:
            # self.rating[key] = 0.0
            ratingCount = 0
            for subject in self.data[key]:
                if subject[1] == 90:
                    # print(key + " : "+ str(subject[1]))
                    ratingCount = ratingCount + 1

            if ratingCount == len(self.data[key]):
                self.rating[key] = 90

        return self.rating
