import requests
from bs4 import BeautifulSoup
import re
def resultsList():
    url = "https://vnrvjietexams.net/eduprime3exam/results/"
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    table = soup.select_one("#exmlst table")
    rows = table.find_all("tr")
    results = []

    for row in rows[1:]:
        columns = row.find_all("td")
        examIdElement = columns[0].find("a")
        examId = examIdElement.get("data-id") if examIdElement else "No data found"
        results.append({
            "name": columns[0].get_text().strip() if columns[0].get_text().strip() else "No data found",
            "examId": examId,
            "resultsReleasedOn": columns[1].get_text().strip() if columns[1].get_text().strip() else "No data found",
            "lastDateOfRCRV": columns[2].get_text().strip() if columns[2].get_text().strip() else "No data found"
        })

    if not rows:
        results.append({"error": "No data found"})

    return results

def getResultsById(htno, examId):
    url = "https://vnrvjietexams.net/eduprime3exam/Results/Results?htno=" + htno + "&examid=" + examId
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    # print(soup)

    

    table = soup.select_one("div").find_all("table")[3]
    

    print(table)


    # rows = table.find_all("tr")
    # print(rows)
    # results = []

    # for row in rows[1:]:
    #     columns = row.find_all("td")
    #     results.append({
    #         "subjectCode": columns[0].get_text().strip() if columns[0].get_text().strip() else "No data found",
    #         "subjectName": columns[1].get_text().strip() if columns[1].get_text().strip() else "No data found",
    #         "internalMarks": columns[2].get_text().strip() if columns[2].get_text().strip() else "No data found",
    #         "externalMarks": columns[3].get_text().strip() if columns[3].get_text().strip() else "No data found",
    #         "totalMarks": columns[4].get_text().strip() if columns[4].get_text().strip() else "No data found",
    #         "result": columns[5].get_text().strip() if columns[5].get_text().strip() else "No data found"
    #     })

    # if not rows:
    #     results.append({"error": "No data found"})

    

    # return results

htno = "22071A6787"
examId = "6185&_=1714748484132"
results = getResultsById(htno, examId)
# print(results)
    
