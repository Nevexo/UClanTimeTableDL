from bs4 import BeautifulSoup
from ics import Calendar, Event
import requests
from requests.auth import HTTPDigestAuth
from datetime import datetime
from dateutil import tz

date_format = '%Y-%m-%d %H:%M:%S' 

c = Calendar()
with open("UCLan Weekly Timetable.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
week = soup.find_all("tr")
lessons = []
for day in week[1:6]:
    date = (day.find("th").text.split()[1]).split("/")
    #print(date)
    for row in day.find_all("td", {"class": "StuTTEvent"}):
        lesson = {}
        text = row.text.split()
        strongs = row.findAll('strong')
        spans = row.findAll('span')
        due_dt = [datetime.strptime(date[2] + "-" + date[1] + "-" + date[0] + " " + strongs[0].text[0:5] + ":00"
            ,date_format).replace(tzinfo=tz.gettz('England/London'))
            , datetime.strptime(date[2] + "-" + date[1] + "-" + date[0] + " " + strongs[0].text[8:] + ":00"
            ,date_format).replace(tzinfo=tz.gettz('England/London'))]
        due_dt = [due_dt[0].astimezone(tz.tzutc()),due_dt[1].astimezone(tz.tzutc())]
        lesson['time'] = [due_dt[0].strftime(date_format),due_dt[1].strftime(date_format)]
        name = " ".join((spans[0].text).split())
        lesson['name'] = name[9:]
        lesson['moduleNumber'] = name[0:6] 
        lesson['location'] = strongs[1].text
        lesson['group'] = " ".join((spans[1].text).split())
        for index, word in enumerate(text): 
            if "," in word:
                lesson['who'] = (word + text[index+1])
                break
        e = Event()
        e.name = lesson.get("name")
        e.begin = lesson.get("time")[0]
        e.end = lesson.get("time")[1]
        e.description = lesson.get("group")
        e.location = lesson.get("location")
        c.events.add(e)
        lessons.append(lesson)
print (lessons)
with open('my.ics', 'w') as f:
    f.write(str(c))
