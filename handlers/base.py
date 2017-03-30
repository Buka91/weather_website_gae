#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import jinja2
import webapp2
import time
import datetime
import json
from utils.special_functions import is_local
from utils.read_file import read_data, city_list
from google.appengine.api import urlfetch
from utils.special_functions import replace_utf8
from utils.secrets import SECRET
from models.town import Town


template_dir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}

        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class WeatherHandler(BaseHandler):
    def get(self):
        read_data()
        name = self.request.get("name")
        description = self.request.get("description")
        temp = self.request.get("temp")
        if temp:
            temp = float(temp)
        params = {"cities": city_list, "name": name, "description": description, "temp": temp}
        return self.render_template("weather.html", params = params)

    def post(self):
        city = self.request.get("selected_city")
        if city != "" and city != "Izberi kraj":
            city = replace_utf8(city)
            town = Town.query(Town.name == city).fetch()
            if town:
                if town[0].updated > datetime.datetime.now() - datetime.timedelta(hours = 1):
                    if is_local():
                        time.sleep(0.1)
                    return self.redirect("/?name=" + town[0].name + "&description=" + town[0].description + "&temp=" + str(town[0].temperature))
                else:
                    while True:
                        try:
                            url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + ",SI&units=metric&appid=" + SECRET
                            break
                        except:
                            continue
                    results = urlfetch.fetch(url)
                    data = json.loads(results.content)
                    description = data[u"weather"][0][u"description"]
                    temp = data[u"main"][u"temp"]
                    town[0].description = description
                    town[0].temperature = temp
                    town[0].put()
                    if is_local():
                        time.sleep(0.1)
                    return self.redirect("/?name=" + town[0].name + "&description=" + description + "&temp=" + str(temp))
            while True:
                try:
                    url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + ",SI&units=metric&appid=" + SECRET
                    break
                except:
                    continue
            results = urlfetch.fetch(url)
            data = json.loads(results.content)
            name = replace_utf8(data[u"name"])
            description = data[u"weather"][0][u"description"]
            temp = data[u"main"][u"temp"]
            Town.add_to_database(name = name, description = description, temp = float(temp))
            if is_local():
                time.sleep(0.1)
            return self.redirect("/?name=" + name + "&description=" + description + "&temp=" + str(temp))
        if is_local():
            time.sleep(0.1)
        return self.redirect_to("main")