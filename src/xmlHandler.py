#!/usr/bin/env python3
import xml.etree.ElementTree as ET

def get_xml(file: str) -> ET.Element:
    ET.register_namespace("", "http://knx.org/xml/telegrams/01")
    mytree = ET.parse(file)
    return mytree.getroot()


def create_xml(file: ET.Element, name: str) -> None:
    print("Creating XML")
    ET.ElementTree(file).write(name, xml_declaration=False)