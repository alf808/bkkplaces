#!/usr/bin/env python
""" Prepare OSM file and convert in some JSON format that mongoDB will consume  """
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json

# added all alpha numeric characters
alphanum = re.compile(r'^([a-zA-Z0-9]|_)*$')
alphanum_colon = re.compile(r'^([a-zA-Z0-9]|_)*:([a-zA-Z0-9]|_)*$')
# added hyphen as a problem char
problemchars = re.compile(r'[=\-\+/&<>;\'"\?%#$@\,\. \t\r\n]')
addresschars = re.compile(r'addr:(\w+)')
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
OSM_FILE = 'bangkok_thailand.osm'

def shape_element(element):
    # create document 
    node = {}
    #address = {}
    if element.tag == "node" or element.tag == "way" :
        # start creating a json document
        node = {'created':{}, 'tagtype':element.tag}
        for item in element.attrib:
            try:
                key_name = element.attrib[item]
            except KeyError:
                continue
            if item == 'lat' or item == 'lon':
                continue
            if item in CREATED:
                node['created'][item] = key_name
            else:
                node[item] = key_name
        try:
            node['pos']=[float(element.attrib['lat']),float(element.attrib['lon'])]
        except KeyError:
            pass
        
        if 'bkkaddress' not in node.keys():
            node['bkkaddress'] = {}
        # Iterate through the content of the tag 'tag'
        for item in element.iter('tag'):
            # handle attribute k 
            k = item.attrib['k']
            v = item.attrib['v']
            if problemchars.match(k):
                continue

            if alphanum_colon.match(k):
                k_list = k.split(":")
                # handle attribute k with name containing "addr:"
                # otherwise attribute k without
                if k.startswith('addr:'):
                    node['bkkaddress'][k_list[1]] = v

                else:
                    # if it does not begin with addr then create underscored key
                    ks = k_list[0] + "_" + k_list[1]
                    node[ks] = v
 
            if alphanum.match(k):
                node[k] = v

        if not node['bkkaddress']:
            node.pop('bkkaddress',None)

        # for "way" tag place all "nd" in an array node_refs
        if element.tag == "way":
            node['node_refs'] = []
            for nd in element.iter('nd'):
                node['node_refs'].append(nd.attrib['ref'])

        return node
    else:
        return None


def process_map(file_in, pretty = False):
    """
    Process the osm file and output file to some JSON format
    """
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():

    data = process_map(OSM_FILE)
    pprint.pprint(data[500])


if __name__ == "__main__":
    test()