#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import jinja2
import webapp2
import json
from google.appengine.api import urlfetch


city_list = list()
not_append = [u"Mestna", u"Občina"]


def read_data():
    if len(city_list) == 0:
        with open('cityList.json') as data_file:
            for line in data_file:
                data_line = json.loads(line)
                if data_line['country'] == 'SI' and data_line['name'][:6] not in not_append:
                    city_list.append(data_line['name'])


template_dir = os.path.join(os.path.dirname(__file__), "templates")
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
        params = {"cities": city_list}
        return self.render_template("weather.html", params = params)

    def post(self):
        read_data()
        city = self.request.get("selected_city")
        if city != "" and city != "Izberi kraj":
            url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + ",SI&units=metric&appid=ed30e7091295cdef6e5431257291d403"
            results = urlfetch.fetch(url)
            data = json.loads(results.content)
            params = {"data": data, "cities": city_list}
            return self.render_template("weather.html", params = params)
        else:
            params = {"cities": city_list}
            return self.render_template("weather.html", params = params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', WeatherHandler)
], debug=True)