[![Build Status](https://app.travis-ci.com/ElenaSafonova/PTLab1.svg?branch=main)](https://app.travis-ci.com/ElenaSafonova/PTLab1)
# PTLab1
Лабораторная работа № 1 по дисциплине "Технологии программирования"
# Цели работы
1. Познакомиться c распределенной системой контроля версий кода Git и ее функциями;
2. Познакомиться с понятиями «непрерывная интеграция» (CI) и «непрерывное развертывание»
(CD), определить их место в современной разработке программного обеспечения;
3. Получить навыки разработки ООП-программ и написания модульных тестов к ним на
современных языках программирования;
4. Получить навыки работы с системой Git для хранения и управления версиями ПО;
5. Получить навыки управления автоматизированным тестированием программного обеспечения,
расположенного в системе Git, с помощью инструмента Travis CI.
6. Выполнить индивидуальное задание (вариант 9): Определить и вывести на экран студента, имеющего 90 баллов по всем дисциплинам. Если таких студентов несколько, нужно вывести любого из них. Если таких студентов нет, необходимо вывести сообщение об их отсутствии. Формат - YAML.
# Ход работы
### Создадим файл формата yaml, класс YAMLDataReader как наследник класса DataReader, тест этого класса и исправим файл main для работы с новым класом. Для этого откроем ветку yaml проекта.
#### Представленный в файле src/YAMLDataReader.py класс реализует чтение данных из  файлов формата .yaml
```python
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

```
#### Тестирование класса YAMLDataReader осуществляется с помощью класса, реализованного в файле test/test_YAMLDataReader.py:
```python
import pytest
from typing import Tuple
from Types import DataType
from YAMLDataReader import YAMLDataReader


class TestYAMLDataReader:

    @pytest.fixture()
    def file_and_data_content(self) -> Tuple[str, DataType]:
        text = "---\n" +\
            "- Иванов Константин Дмитриевич:\n" + \
            "    математика: 80\n" + \
            "    химия: 90\n" + \
            "- Петров Петр Семенович:\n" + \
            "    русский язык: 87\n" + \
            "    литература: 78\n"

        data = {
            "Иванов Константин Дмитриевич": [
                ("математика", 80), ("химия", 90)
            ],
            "Петров Петр Семенович": [
                ("русский язык", 87), ("литература", 78)
            ]
        }
        return text, data

    @pytest.fixture()
    def filepath_and_data(self,
                          file_and_data_content: Tuple[str, DataType],
                          tmpdir) -> Tuple[str, DataType]:
        p = tmpdir.mkdir("datadir").join("my_data.yaml")
        p.write(file_and_data_content[0])
        return str(p), file_and_data_content[1]

    def test_read(self, filepath_and_data:
                  Tuple[str, DataType]) -> None:
        file_content = YAMLDataReader().read(filepath_and_data[0])
        assert file_content == filepath_and_data[1]

```
#### main.py:
```python
from YAMLDataReader import YAMLDataReader
from CalcRating import CalcRating
import argparse
import sys


def get_path_from_arguments(args) -> str:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument("-p", dest="path", type=str, required=True,
                        help="Path to datafile")
    args = parser.parse_args(args)
    return args.path


def main():
    path = get_path_from_arguments(sys.argv[1:])
    reader = YAMLDataReader()
    students = reader.read(path)
    print("Students: ", students)
    rating = CalcRating(students).calc()
    print("Ratings: ", rating)


if __name__ == "__main__":
    main()
```
#### Работа кода ветки yaml
![pull_yaml](/reports/report.png)
#### Проверка кода прошла успешно
![test_yaml](/reports/test_yaml.png)
#### Pull request ветки yaml
![pull_yaml](/reports/pull_yaml.png)

### Создадим новую ветку проекта code90 для выполнения задания по варианту 9 (код,тесты, исправление main.py)
#### Расчета задания по варианту 9 осуществляется с помощью кода, представленного в файле src/CheckAll90Ratings.py
```python
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

```

#### Файл test/test_CheckAll90Ratings.py содержит класс для выполнения модульного тестирования методов класса CheckAll90Ratings:
```python
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


```
#### main.py:
```python
from YAMLDataReader import YAMLDataReader
from CheckAll90Ratings import CheckAll90Ratings
import argparse
import sys


def get_path_from_arguments(args) -> str:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument("-p", dest="path", type=str, required=True,
                        help="Path to datafile")
    args = parser.parse_args(args)
    return args.path


def main():
    path = get_path_from_arguments(sys.argv[1:])
    reader = YAMLDataReader()
    students = reader.read(path)
    print("Students: ", students)
    rating = CheckAll90Ratings(students).calc()
    print("Ratings All 90: ", rating)


if __name__ == "__main__":
    main()
```
#### Работа кода ветки code90
![pull_yaml](/reports/report2.png)
#### Проверка кода прошла успешно
![test_code90](/reports/test_code90.png)
#### Pull request ветки code90
![pull_code90](/reports/pull_code90.png)

### Network graph:
![merge](/reports/merge_code90.png)
### Структура файлов проекта:
![Директория](/reports/dir.png)
### UML-диаграмма:
![UML](/reports/UML.png)
### Пакеты:
- pytest - тестирование
- mypy - корректность работы с типами
- pycodestyle - соответствие кода стандарту РЕР-8
- pyyaml - модуль для работы с yaml
- types-PyYAML - корректность работы с типами (аналог mypy)
# Выводы
1. Закреплено представление о распределенной системе контроля версий кода Git и ее функциях;
2. Закреплены понятия «непрерывная интеграция» (CI) и «непрерывное развертывание»
(CD), определено их место в современной разработке программного обеспечения;
3. Получены навыки разработки ООП-программ и написания модульных тестов к ним на
современных языках программирования;
4. Получены навыки работы с системой Git для хранения и управления версиями ПО;
5. Получены навыки управления автоматизированным тестированием программного обеспечения, расположенного в системе Git, с помощью инструмента Travis CI.
