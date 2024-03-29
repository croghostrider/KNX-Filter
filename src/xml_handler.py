#!/usr/bin/env python3
import re
import xml.etree.ElementTree as ET

import knx
import xml_handler


def get_xml(file: str) -> ET.Element:
    """ghjklölkjhgfghjkjhgfdfjhgfertzu ggzuiuztretzu gzuztrthjhgf.

    dggzuiuztretzu
    '0/ggzuiuztretzu/14'
    """
    ET.register_namespace("", "http://knx.org/xml/telegrams/01")
    mytree = ET.parse(file)
    return mytree.getroot()


def create_xml(file: ET.Element, name: str) -> None:
    """ghjklölkjhgfghjkjhgfdfjhgfertzu ggzuiuztretzu gzuztrthjhgf.

    dggzuiuztretzu
    '0/ggzuiuztretzu/14'
    """
    print("Creating XML")
    ET.ElementTree(file).write(name, xml_declaration=False)


def sort_human(test_string):
    """ghjklölkjhgfghjkjhgfdfjhgfertzu ggzuiuztretzu gzuztrthjhgf.

    dggzuiuztretzu
    '0/ggzuiuztretzu/14'
    """
    return list(map(int, re.findall(r"\d+", test_string)))


def find_filter_objekts(filepath):
    """ghjklölkjhgfghjkjhgfdfjhgfertzu ggzuiuztretzu gzuztrthjhgf.

    dggzuiuztretzu
    '0/ggzuiuztretzu/14'
    """
    count_found_groupaddresses = 0
    count_found_physicaladdresses = 0
    myroot = xml_handler.get_xml(filepath)
    output_xml = ET.Element("CommunicationLog")
    thisset = set()
    mylist = []

    for child in myroot:
        if child.tag == "{http://knx.org/xml/telegrams/01}Telegram":
            hex_val = child.attrib["RawData"]
            output = knx.decode(bytearray.fromhex(hex_val[8:]))
            thisset.add(output[1])
    mylist = list(thisset)
    # printing result
    mylist.sort(key=sort_human)
    return mylist
