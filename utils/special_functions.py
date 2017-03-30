#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def is_local():
    if os.environ.get('SERVER_NAME', '').startswith('localhost'):
        return True
    elif 'development' in os.environ.get('SERVER_SOFTWARE', '').lower():
        return True
    else:
        return False


def replace_utf8(string):
    if u"č" in string:
        string = string.replace(u"č", u"c")
    if u"Č" in string:
        string = string.replace(u"Č", u"C")
    if u"š" in string:
        string = string.replace(u"š", u"s")
    if u"Š" in string:
        string = string.replae(u"Š", u"S")
    if u"ž" in string:
        string = string.replace(u"ž", u"z")
    if u"Ž" in string:
        string = string.replace(u"Ž", u"Z")
    return string