import requests
import json
import datetime
import os
from datetime import date
from Utils import Utils
from Report import Report
import sys

def calcPrevSprintTimeStamp() -> dict:
    output_format = "%Y-%m-%dT%H:%M:%S.000Z"

    today = date.today()
    week = datetime.date(int(today.year), int(today.month), int(today.day)).isocalendar()[1] - 2
    if week % 2 == 1:
        week -= 1

    start_date = datetime.datetime.strptime(str(today.year) + "-W" + str(week) + "-1", "%G-W%V-%u")
    end_date = datetime.datetime.strptime(str(today.year) + "-W" + str(week + 1) + "-7 23:59:59", "%G-W%V-%u %H:%M:%S")

    return {
        "weeks": str(week) + "-" + str(week + 1),
        "startDate": start_date.strftime(output_format),
        "endDate": end_date.strftime(output_format)
    }


def getReportSummary(timestamp: dict) -> dict:
    api_endpoint = "https://api.clockify.me/api/workspaces/5c6d212ab079873a550108c0/reports/summary"
    user_key = Utils.readJsonFile("json/user_key.json")

    summary_rq = Utils.readJsonFile("json/summary_request.json")
    summary_rq["startDate"] = timestamp["startDate"]
    summary_rq["endDate"] = timestamp["endDate"]

    response = requests.post(api_endpoint,
                             headers={"X-Api-Key": user_key["key"], 'Content-type': 'application/json'},
                             json=summary_rq)
    return json.loads(response.text)


def main():
    if(len(sys.argv) != 2):
        print("You need to pass excatly one paramater.\nUsage: python3 export.py 'project'/'taskname'")
        return
    else:
        if not os.path.isdir("export"):
            os.mkdir("export")

        sprint_timemstamp = calcPrevSprintTimeStamp()
        Report(getReportSummary(sprint_timemstamp), sprint_timemstamp).exportToJson(sys.argv[1])


if __name__ == "__main__":
    main()
