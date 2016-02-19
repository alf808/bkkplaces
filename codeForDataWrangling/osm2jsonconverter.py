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
postcode_th = re.compile(r'^(\d{5}).*$')
phone_rid66 = re.compile(r'^\D*66\D*(.*)$')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
OSM_FILE = 'bangkok_thailand.osm'

def cleanpostcode(code):
    m = postcode_th.match(code)
    # postcode will be passed here and compared to postcode_th
    # grab only the first 5 digits
    if m:
        cleaned = m.group(1)
    # if not 5 digit match, then return the most common postal code in Bangkok
    else:
        cleaned = "10200"
    return cleaned

def cleanphones(phone):
    # those with multiple phone numbers will be split and place in an array
    ph = phone.split(";")
    ph_array = []
    for item in ph:
        # if number contains 66, take it out and return the remaining numbers
        m = phone_rid66.match(item)
        if m:
            item = m.group(1)
        if item:
            ph_array.append(item)
    return ph_array

def shape_element(element):
    # create document 
    node = {}
    #address = {}
    if element.tag == "node" or element.tag == "way" :
        # start creating a json document
        node = {'created':{}, 'tagtype':element.tag}
        # nitem for node name, aname for attrib value
        for nitem in element.attrib:
            try:
                aname = element.attrib[nitem]
            except KeyError:
                continue
            if nitem == 'lat' or nitem == 'lon':
                continue
            if nitem in CREATED:
                node['created'][nitem] = aname
            else:
                node[nitem] = aname
        try:
            node['pos']=[float(element.attrib['lat']),float(element.attrib['lon'])]
        except KeyError:
            pass
        
        # Iterate through the content of the tag 'tag'
        for item in element.iter('tag'):
            # handle attribute k 
            k = item.attrib['k']
            v = item.attrib['v']
            if problemchars.match(k):
                continue

            if alphanum_colon.match(k):
                k_list = k.split(":")
                k1 = k_list[0]
                k2 = k_list[1]
                # handle attribute k with name containing "addr:"
                # otherwise attribute k without
                if k1 == 'addr':
                    if 'bkkaddress' not in node.keys():
                        node['bkkaddress'] = {}
                    # fix postcode to 5-digit characters
                    if k2 == 'postcode':
                        node['bkkaddress'][k2] = cleanpostcode(v)
                    else:
                        node['bkkaddress'][k2] = v

                else:
                    # if it does not begin with addr then create underscored key
                    ks = k1 + "_" + k2
                    node[ks] = v
 
            if alphanum.match(k):
                if k == 'phone':
                    if 'phone' not in node.keys():
                        node['phone'] = {}
                    node['phone']['countrycode'] = 66
                    node['phone']['numbers'] = cleanphones(v)

                else:
                    node[k] = v

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