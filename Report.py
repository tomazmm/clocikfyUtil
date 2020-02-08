import re
import pprint

pp = pprint.PrettyPrinter(indent=4)

class Task:


    def __init__(self, task: dict):
        self.id = task["id"]
        self.name = task["description"].split("--")[0].strip()
        self.description = task['description'].split("--")[1].strip() if len(task["description"].split("--")) == 2 else ""
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

        self.sorted = self.groupByTaskName()
        pp.pprint(self.sorted)


    def groupByTaskName(self) -> sorted:
        sorted = {}
        for task in self.tasks:
            if task.name in sorted:
                sorted[task.name]["tasks"].append(task.serialize())
                sorted[task.name]["SP"] += task.story_points
            else:
                sorted[task.name] = {}
                sorted[task.name]["tasks"] = []
                sorted[task.name]["SP"] = task.story_points
                sorted[task.name]["tasks"].append(task.serialize())
        return sorted


    def serialize(self):
        for entry in (vars(self)):
            if(entry == "tasks"):
                print("Tasks: ")
                for task in self.__dict__[entry]:
                    print(vars(task))
            else:
                print(str(entry), " : ", self.__dict__[entry])

