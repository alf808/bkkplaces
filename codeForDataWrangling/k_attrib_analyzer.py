#!/usr/bin/env python
"""
    Retrieve the k attributes in tag "tag" and count occurences per k
"""
import xml.etree.cElementTree as ET
import codecs
import json


def get_key_counts(file_in,pretty=False):
    """Count all k values and number of variations of each."""
    file_out = "{0}.json".format(file_in)
    key_names = {}
    # just look at "k" attributes in tag "tag"
    for _, elem in ET.iterparse(file_in):
        if elem.tag == "tag":
            k_val = elem.get("k")
            # keep count of the key names
            if k_val in key_names:
                key_names[k_val] += 1
            else:
                key_names[k_val] = 1

    data = []
    with codecs.open(file_out, "w") as fo:
        for key in key_names:
            count = key_names[key]
            el = {
                "key_name": key,
                "count": count
            }
            data.append(el)
            if pretty:
                fo.write(json.dumps(el, indent=2)+"\n")
            else:
                fo.write(json.dumps(el) + "\n")

    return data


if __name__ == '__main__':
    OSM_FILE = 'bangkok_thailand.osm'
    get_key_counts(OSM_FILE,False)
