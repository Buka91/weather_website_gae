#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import ndb

class Town(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.StringProperty()
    temperature = ndb.FloatProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def add_to_database(cls, name, description, temp):
        town = Town(name = name, description = description, temperature = temp)
        town.put()