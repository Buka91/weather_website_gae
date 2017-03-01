#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handlers import base

app = base.webapp2.WSGIApplication([
    base.webapp2.Route('/', base.WeatherHandler)
], debug=True)