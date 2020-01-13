import requests
from bs4 import BeautifulSoup 
from datetime import date, timedelta
import csv

#Initialisations
result = {}
months = {
        'Jan' : '01',
        'Feb' : '02',
        'Mar' : '03',
        'Apr' : '04',
        'May' : '05',
        'Jun' : '06',
        'Jul' : '07',
        'Aug' : '08',
        'Sep' : '09', 
        'Oct' : '10',
        'Nov' : '11',
        'Dec' : '12'
}


#Generating a range of dates from start of year to end of year for the result
start_date = date(2019, 1, 1)
end_date = date(2019, 12, 31)
delta = timedelta(days=1)
while start_date <= end_date:
    result[start_date.strftime("%Y-%m-%dT00:00:00+00:00")] = 0
    start_date += delta

#Converting wikipedia date to ISO format
def convert_date(launch_date):
    date = launch_date.split(" ")[0]
    if(len(date) == 1):
        date = "0"+date
    month = launch_date.split(" ")[1][:3]
    return "2019-"+str(months[month])+"-"+date+"T00:00:00+00:00"


URL = "https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches"
r = requests.get(URL)
bs = BeautifulSoup(r.content, 'html5lib')

#finding the table
table = bs.find("table", {"class": "wikitable collapsible"})

#all the rows in the table
rows = table.findAll(lambda tag: tag.name=='tr')

rowspan = 0
launch_date = ""
for row in rows[1:]:
    
    data = row.findAll(lambda tag: tag.name=='td')

    #launch vehichle line
    if(data[0].has_attr('rowspan')):
        rowspan = int(data[0]['rowspan'])-1
        span = data[0].find(lambda tag: tag.name=='span')
        launch_date = span.text
        continue

    #payloads
    if(rowspan > 0):
        if(data[-1].text.strip() in {"Successful", "Operational", "En Route"}):
            result[convert_date(launch_date)]+=1
    rowspan-=1


with open("output.csv", 'w') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(["date","value"])
    start_date = date(2019, 1, 1)
    end_date = date(2019, 12, 31)
    delta = timedelta(days=1)
    while start_date <= end_date:
        val = start_date.strftime("%Y-%m-%dT00:00:00+00:00")
        csvwriter.writerow([val,str(result[val])])
        start_date += delta

