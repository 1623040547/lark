from dataclasses import dataclass
import json
import sys


@dataclass
class TableLoad:
    app_id: str
    app_secret: str
    table_id: str
    table_name: str
    index_name: str
    data_name: str
    index_json: dict
    data_json: dict


# file/sheet/
class ConfigReader:
    project_dir = ''
    index_path = ''
    data_path = ''
    file_suffix = ''
    app_id = None
    app_secret = None
    loads = []
    is_increment = False
    config = None

    @classmethod
    def read_config(cls):
        config_path = './config.json'
        j = json.load(open(config_path))
        cls.app_id = j["app_id"]
        cls.app_secret = j["app_secret"]
        cls.index_path = j["index_path"]
        cls.data_path = j["data_path"]
        cls.file_suffix = j["file_suffix"]
        try:
            cls.is_increment = str(sys.argv[2]) == str(1)
            print("read_config:", cls.is_increment)
        except:
            pass
        for t in j["table"]:
            table_id = t["table_id"]
            table_name = t['name']
            sel_table_name = sys.argv[1]
            if sel_table_name != table_name:
                continue
            for k, v in t["loads"].items():
                index_file = cls.index_path + '/' + k + cls.file_suffix
                data_file = cls.data_path + '/' + v + cls.file_suffix
                cls.loads.append(
                    TableLoad(
                        app_id=cls.app_id,
                        app_secret=cls.app_secret,
                        table_id=table_id,
                        index_name=k,
                        data_name=v,
                        index_json=json.load(open(index_file, encoding='utf-8')),
                        data_json=json.load(open(data_file, encoding='utf-8')),
                        table_name=table_name
                    )
                )


def test_config_reader():
    ConfigReader.read_config()
    print(ConfigReader.app_id)
    print(ConfigReader.app_secret)
