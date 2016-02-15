#!/usr/bin/env python

"""Retrieve the top level tags of an OSM file
"""


import xml.etree.cElementTree as ET
import codecs
import json

def get_top_level_tags(file_in,pretty=False):
    # Write the results in a file.Return dict containing name and count of top level tags.
    file_out = "{0}.json".format(file_in)
    data = []
    tags = {}
    with codecs.open(file_out, "w") as fo:
        # retrieve and count top level tags, create a dictionary for each tag, and place in array
        for _, elem in ET.iterparse(file_in):
            if elem.tag in tags:
                tags[elem.tag] += 1
            else:
                tags[elem.tag] = 1

        if tags:
            data.append(tags)
            if pretty:
                fo.write(json.dumps(tags, indent=2)+"\n")
            else:
                fo.write(json.dumps(tags) + "\n")
    return data


if __name__ == '__main__':
    OSM_FILE = 'bangkok_thailand.osm'
    print get_top_level_tag_summary(OSM_FILE,True)
