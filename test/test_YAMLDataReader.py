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
