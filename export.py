import requests
import pprint
import json
import datetime
from datetime import date
import re

pp = pprint.PrettyPrinter(indent=4)

api = {
    "endpoint": "https://api.clockify.me/api/workspaces/5c6d212ab079873a550108c0/reports/summary",
    "key": "XjvZ28qiwG3DXF+/",
}

def calcPrevSprintTimeStamp() -> dict:
    output_format = "%Y-%m-%dT%H:%M:%S.000Z"

    today = date.today()
    week = datetime.date(int(today.year), int(today.month), int(today.day)).isocalendar()[1] - 2
    if week % 2 == 1:
        week -= 1

    start_date = datetime.datetime.strptime(str(today.year) + "-W" + str(week) + "-1", "%G-W%V-%u")
    end_date = datetime.datetime.strptime(str(today.year) + "-W" + str(week + 1) + "-7 23:59:59", "%G-W%V-%u %H:%M:%S")

    return {
        "startDate": start_date.strftime(output_format),
        "endDate": end_date.strftime(output_format)
    }

def openJsonFile(name : str) -> dict:
    with open(name, "r") as file:
        return json.load(file)


def getReportSummary() -> dict:
    sprint_timestamp = calcPrevSprintTimeStamp()
    summary_rq = openJsonFile("json/summary_request.json")
    summary_rq["startDate"] = sprint_timestamp["startDate"]
    summary_rq["endDate"] = sprint_timestamp["endDate"]

    response = requests.post(api["endpoint"],
                             headers={"X-Api-Key": api["key"], 'Content-type': 'application/json'},
                             json=summary_rq)
    return json.loads(response.text)


def parseTaskDuration( duration : str ) -> int:
    num = list(map(int, re.findall(r'\d+', duration)))
    if len(num) == 1:
        return num[0]
    elif len(num) == 2:
        return num[0] * 60 + num[1]
    else:
        assert False


def calcSP( duration : int) -> float:
    return round(duration / 60 / 4, 1)


def main():
    report = getReportSummary()
    sp = 0
    for entry in report["timeEntries"]:
        #pp.pprint(entry)
        duration = parseTaskDuration(entry["timeInterval"]["duration"])
        print(entry["project"]["name"] + " : " + entry["description"])
        print("Duration: ", duration)
        sp += calcSP(duration)
        print("SP: ", calcSP(duration))
    print("story points: ", round(sp, 1))


if __name__ == "__main__":
    main()
