#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
count the key types in of each of four categories in a dictionary:
  "alphanum", for tags that contain only lowercase letters and are valid,
  "alphanum_colon", for otherwise valid tags with a colon in their names,
  "problemchars", for tags with problematic characters, and
  "other", for other tags that do not fall into the other three categories.
See the 'process_map' and 'test' functions for examples of the expected format.
"""


alphanum = re.compile(r'^([a-zA-Z0-9]|_)*$')
alphanum_colon = re.compile(r'^([a-zA-Z0-9]|_)*(:([a-zA-Z0-9]|_)*)*$')
problemchars = re.compile(r'[=\-\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    # Look at tag element "<tag>". Find the k attributes that potentially can be
    # keys for BSON dictionary. Keep count of the k values with non-colon valid characters
    # and k values with problem characters, namely those defined in problemchars variable.
    if element.tag == "tag":
        k = element.get("k")

        if re.search(alphanum, k):
            keys["alphanum"] += 1
        elif re.search(alphanum_colon, k):
            keys["alphanum_colon"] += 1
        elif re.search(problemchars, k):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1

    return keys



def process_map(filename):
    keys = {"alphanum": 0, "alphanum_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertion below will be incorrect then.
    # Note as well that the test function here is only used in the Test Run;
    # when you submit, your code will be checked against a different dataset.
    keys = process_map('bangkok_thailand.osm')
    pprint.pprint(keys)
    #assert keys == {'lower': 5, 'lower_colon': 0, 'other': 1, 'problemchars': 1}


if __name__ == "__main__":
    test()