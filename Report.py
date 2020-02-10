import re
import pprint
from Utils import Utils


pp = pprint.PrettyPrinter(indent=1)


class Task:

    def __init__(self, task: dict):
        self.id = task["id"]
        self.name = task["description"].split("--")[0].strip()
        self.description = task['description'].split("--")[1].strip() if len(
            task["description"].split("--")) == 2 else ""
        self.project = task["project"]["name"]
        self.time_interval = {
            "start": task["timeInterval"]["start"],
            "end": task["timeInterval"]["end"],
            "duration": self.parseDuration(task["timeInterval"]["duration"])
        }
        self.story_points = self.calcSP()

    def parseDuration(self, duration: str) -> int:
        num = list(map(int, re.findall(r'\d+', duration)))
        if len(num) == 1:
            return num[0]
        elif len(num) == 2:
            return num[0] * 60 + num[1]
        else:
            assert False

    def calcSP(self):
        return round(self.time_interval["duration"] / 60 / 4, 1)

    def serialize(self):
        serialized = {}
        for entry in vars(self):
            serialized[entry] = self.__dict__[entry]
        return serialized


class Report:
    def __init__(self, report: dict):
        self.tasks = []
        self.projects = set()
        self.story_points = 0
        for entry in report["timeEntries"]:
            task = Task(entry)
            self.tasks.append(task)
            self.projects.add(entry["project"]["name"])
            self.story_points += task.story_points

    def groupByTaskName(self) -> dict:
        grouped = {}
        for task in self.tasks:
            if task.name in grouped:
                grouped[task.name]["tasks"].append(task.serialize())
                grouped[task.name]["SP"] += round(task.story_points, 1)
            else:
                grouped[task.name] = {}
                grouped[task.name]["tasks"] = []
                grouped[task.name]["tasks"].append(task.serialize())
                grouped[task.name]["SP"] = round(task.story_points, 1)
        return grouped

    def groupByProject(self) -> dict:
        grouped = {}
        for task in self.tasks:
            if task.project in grouped:
                if task.name in grouped[task.project]["tasks"]:
                    grouped[task.project]["tasks"][task.name].append(task.serialize())
                else:
                    grouped[task.project]["tasks"][task.name] = []
                    grouped[task.project]["tasks"][task.name].append(task.serialize())
                grouped[task.project]["SP"] += round(task.story_points, 1)
            else:
                grouped[task.project] = {}
                grouped[task.project]["tasks"] = {}
                grouped[task.project]["tasks"][task.name] = []
                grouped[task.project]["tasks"][task.name].append(task.serialize())
                grouped[task.project]["SP"] = round(task.story_points, 1)
        return grouped

    def exportToJson(self, groupBy=None):
        if(groupBy == "project"):
            Utils.writeJsonFile(self.groupByProject(),  "export/SprintReport-06072020")
        elif(groupBy == "taskname"):
            Utils.writeJsonFile(self.groupByTaskName(), "export/SprintReport-06072020")

