import re


class Task:
    def __init__(self, task : dict):
        self.id = task["id"]
        self.name = task['description'].split("--")[0]
        self.description = task['description'].split("--")[1]
        self.project = task["project"]["name"]
        self.time_intervals = {
            "start": task["timeInterval"]["start"],
            "end": task["timeInterval"]["end"],
            "duration": self.parseDuration(task["timeInterval"]["duration"])
        }


    def parseDuration(self, duration: str) -> int:
        num = list(map(int, re.findall(r'\d+', duration)))
        if len(num) == 1:
            return num[0]
        elif len(num) == 2:
            return num[0] * 60 + num[1]
        else:
            assert False


class Report:
    def __init__(self, report: dict):
        self.tasks = []
        self.projects = set()
        for entry in report["timeEntries"]:
            self.tasks.append(Task(entry))
            self.projects.add(entry["project"]["name"])






