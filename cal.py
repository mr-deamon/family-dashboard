from datetime import datetime, timedelta
from ics import Calendar
import arrow
from jinja2 import Environment, FileSystemLoader
import json
import requests

environment = Environment(loader=FileSystemLoader("."))
template = environment.get_template("template.html.j2")

YOUR_TIMEZONE = 'Europe/Berlin'  # Example timezone
today=arrow.now(YOUR_TIMEZONE)

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
    day = arrow.now(YOUR_TIMEZONE).replace(hour=0, minute=0, second=0, microsecond=0).shift(days=+i)
    for event in c.timeline.on(day):
      if lastevent!=event.name:
        if(event.duration==timedelta(days=1) and event.begin!=day):
          continue
        event_begin_local = event.begin.to(YOUR_TIMEZONE)
        event.end = event.end.to(YOUR_TIMEZONE) if event.end else None  # Convert event.end similarly, if used
        
        # You might need to adjust this part depending on how you use the event times
        # For example, you could replace the event.begin with the localized version
        event.begin = event_begin_local
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


