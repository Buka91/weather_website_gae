#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
from handlers.base import WeatherHandler

app = webapp2.WSGIApplication([
    webapp2.Route('/', WeatherHandler, name = "main")
], debug=True)