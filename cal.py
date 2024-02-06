from datetime import datetime, timedelta
from ics import Calendar
import arrow
from jinja2 import Environment, FileSystemLoader
import json
import requests

environment = Environment(loader=FileSystemLoader("."))
template = environment.get_template("template.html.j2")

today=arrow.now()

def process_calendar():

  cal_url=json.loads(open("config.json").read())['urls']
  
  c=Calendar()
  for url in cal_url:
    for event in Calendar(requests.get(url).text).events:
      c.events.add(event)

  out={}
  for i in range(0,2):
    out[i]=[]
    lastevent=""
    day = arrow.arrow.Arrow(today.year,today.month,today.day+i)
    for event in c.timeline.on(day):
      if lastevent!=event.name:
        if(event.duration==timedelta(days=1) and event.begin!=day):
          continue
        out[i].append(event)
      lastevent = event.name
  return out

def process_weather():
  weather_json=json.loads(requests.get("https://www.landi.ch/weather/api/lokalprognose/de/{}/G2661408".format(today.format('YYYY-MM-DD')),'r').text)
  return weather_json['ganzertag']

events=process_calendar()
weather=process_weather()
content = template.render(today=today.day,tomorrow=today.day+1,events=events,weather=weather)

with open("index.html", mode="w", encoding="utf-8") as message:
  message.write(content)


