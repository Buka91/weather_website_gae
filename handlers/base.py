#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import jinja2
import webapp2
import secrets
import readFile
from google.appengine.api import urlfetch


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
        readFile.read_data()
        params = {"cities": readFile.city_list}
        return self.render_template("weather.html", params = params)

    def post(self):
        readFile.read_data()
        city = self.request.get("selected_city")
        if city != "" and city != "Izberi kraj":
            url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + ",SI&units=metric&appid=" + secrets.secret()
            results = urlfetch.fetch(url)
            data = readFile.json.loads(results.content)
            params = {"data": data, "cities": readFile.city_list}
            return self.render_template("weather.html", params = params)
        else:
            params = {"cities": readFile.city_list}
            return self.render_template("weather.html", params = params)