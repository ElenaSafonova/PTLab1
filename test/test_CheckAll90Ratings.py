from typing import Dict, Tuple
from Types import DataType
from CheckAll90Ratings import CheckAll90Ratings
import pytest

RatingsType = Dict[str, float]


class TestCheckAll90Ratings():

    @pytest.fixture()
    def input_data(self) -> Tuple[DataType, RatingsType]:
        data: DataType = {
            "Абрамов Петр Сергеевич":
            [
                ("математика", 90),
                ("русский язык", 90),
                ("программирование", 90)
            ],
            "Петров Игорь Владимирович":
            [
                ("математика", 61),
                ("русский язык", 80),
                ("программирование", 78),
                ("литература", 97)
            ],
            "Иванов Иван Иванович":
            [
                ("математика", 90),
                ("русский язык", 90),
                ("программирование", 90),
                ("литература", 90)
            ]

        }

        rating_scores: RatingsType = {
            "Абрамов Петр Сергеевич": 90,
            "Иванов Иван Иванович": 90
        }
        return data, rating_scores

    def test_init_calc_rating(self, input_data:
                              Tuple[DataType,
                                    RatingsType]) -> None:
        calc_rating = CheckAll90Ratings(input_data[0])
        assert input_data[0] == calc_rating.data

    def test_calc(self, input_data:
                  Tuple[DataType, RatingsType]) -> None:
        rating = CheckAll90Ratings(input_data[0]).calc()

        # первое, что проверяем - все ли посчитанные с 90 баллами есть в списке
        for student in rating.keys():
            rating_score = rating[student]

            assert pytest.approx(rating_score,
                                 abs=0.001) == input_data[1][student]

        # делаем перекрестную проверку - у всех, кто в списке, 90 баллов
        for student in input_data[1]:
            rating_score = input_data[1][student]

            assert pytest.approx(rating_score,
                                 abs=0.001) == rating[student]
