import json

class Utils:

    @staticmethod
    def readJsonFile(name: str) -> dict:
        with open(name, "r") as file:
            return json.load(file)


    @staticmethod
    def writeJsonFile(json_data: dict, path: str) -> None:
        with open(path, 'w+') as file:
            json.dump(json_data, file, indent=4)
