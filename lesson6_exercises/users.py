#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

# deleted def get_user. not needed in this exercise

def process_map(filename):
    # go through the xml document and retrieve tag or attribute uid
    # add the uid to users array. set() insures that the array has unique values
    users = set()
    for _, element in ET.iterparse(filename):
        uid = element.get("uid")
        if uid:
            users.add(uid)

    return users


def test():

    users = process_map('users_example.osm')
    pprint.pprint(users)
    assert len(users) == 6



if __name__ == "__main__":
    test()