#!/usr/bin/env python3
import time
from typing import Any, NamedTuple
import xml.etree.ElementTree as ET
import re


from ttkwidgets import CheckboxTreeview
import tkinter as tk

root = tk.Tk()

tree = CheckboxTreeview(root)


group_addresses = [
    "31/1/100",
    "31/1/101",
    "31/1/102",
    "31/1/103",
    "31/1/104",
    "31/1/110",
    "31/1/111",
    "31/1/112",
    "31/1/113",
    "31/1/114",
]


EIB_OPEN_GROUPCON = 0x26
EIB_GROUP_PACKET = 0x27
KNXWRITE = 0x001
KNXREAD = 0x80
FILTER_PHYSICAL = 0
FILTER_GROUP = 1
MODE_TELEGRAMM = 1
MODE_CHANGE = 2


class Telegram(NamedTuple):
    src: str
    dst: str
    value: Any


def decode_individual_address(individual_address: int) -> str:
    """Decode an individual address into human readable string representation.

    decode_individual_address(4606)
    '1.1.254'

    See also: http://www.openremote.org/display/knowledge/KNX+Individual+Address
    """
    return f"{(individual_address >> 12) & 0x1f}.{(individual_address >> 8) & 0x07}.{(individual_address) & 0xff}"


def decode_group_address(group_address: int) -> str:
    """Decodes a group address into human readable string representation.

    decode_group_address(270)
    '0/1/14'
    """
    return f"{(group_address >> 11) & 0x1f}/{(group_address >> 8) & 0x07}/{(group_address) & 0xff}"


def decode(buf: bytearray) -> Telegram:
    """Decodes a binary telegram in the format:

        2 byte: src
        2 byte: dst
        X byte: data

    Returns a Telegram namedtuple.

    If the data had only 1 bytes the value is either 0 or 1
    In case there was more than 1 byte the value will contain the raw data as
    bytestring.

    decode(bytearray([0x11, 0xFE, 0x00, 0x07, 0x00, 0x83]))
    Telegram(src='1.1.254', dst='0/0/7', value=3)

    decode(bytearray([0x11, 0x08, 0x00, 0x14, 0x00, 0x81]))
    Telegram(src='1.1.8', dst='0/0/20', value=1)

    """
    src = decode_individual_address(buf[0] << 8 | buf[1])
    dst = decode_group_address(buf[2] << 8 | buf[3])

    data = buf[6:]

    value = (data[0] & 0x3F).to_bytes(1, "big") if len(data) == 1 else data[1:]
    return Telegram(src, dst, value)


def get_xml(file: str) -> ET.Element:
    ET.register_namespace("", "http://knx.org/xml/telegrams/01")
    mytree = ET.parse(file)
    return mytree.getroot()


def create_xml(file: ET.Element, name: str) -> None:
    print("Creating XML")
    ET.ElementTree(file).write(name, xml_declaration=False)


def filter_teregramms(search_filter: "list[str]", filter_mode: int) -> None:
    count_found_telegramms = 0
    count_removed_telegramms = 0
    myroot = get_xml("1.xml")
    output_xml = ET.Element("CommunicationLog")

    for child in myroot:
        if child.tag == "{http://knx.org/xml/telegrams/01}Telegram":
            hex_val = child.attrib["RawData"]
            output = decode(bytearray.fromhex(hex_val[8:]))
            if output[filter_mode] in search_filter:
                output_xml.append(child)
                count_found_telegramms = count_found_telegramms + 1
            else:
                count_removed_telegramms = count_removed_telegramms + 1
        else:
            output_xml.append(child)

    print("total telegramms:", count_removed_telegramms + count_found_telegramms)
    print("found: ", count_found_telegramms)
    print("removed: ", count_removed_telegramms)
    create_xml(output_xml, "filter_teregramms2.xml")


def filter_groupaddress_change(search_filter: "list[str]", filter_mode: int) -> None:
    myroot = get_xml("filter_teregramms2.xml")
    output_xml = ET.Element("CommunicationLog")
    group_values: "dict[str, bytearray]" = {}
    group_values_old: "dict[str, bytearray]" = {}

    for child in myroot:
        if child.tag == "{http://knx.org/xml/telegrams/01}Telegram":
            hex_val = child.attrib["RawData"]
            output = decode(bytearray.fromhex(hex_val[8:]))
            if output[filter_mode] in search_filter:
                group_values[output[1]] = output[2]
                if output[1] in group_values_old:
                    if group_values[output[1]] != group_values_old[output[1]]:
                        output_xml.append(child)
                else:
                    output_xml.append(child)
                group_values_old[output[1]] = output[2]
            else:
                output_xml.append(child)
        else:
            output_xml.append(child)

    create_xml(output_xml, "filter_on_change_teregramms.xml")

# helper function to perform sort
def num_sort(test_string, pos):
    return list(map(int, re.findall(r'\d+', test_string)))[pos]

def sort_human(test_string):
    return list(map(int, re.findall(r'\d+', test_string)))


def find_filter_objekts():
    count_found_groupaddresses = 0
    count_found_physicaladdresses = 0
    myroot = get_xml("1.xml")
    output_xml = ET.Element("CommunicationLog")
    thisset = set()
    mylist = []

    for child in myroot:
        if child.tag == "{http://knx.org/xml/telegrams/01}Telegram":
            hex_val = child.attrib["RawData"]
            output = decode(bytearray.fromhex(hex_val[8:]))
            thisset.add(output[1])
    mylist = list(thisset)
    # printing result
    mylist.sort(key=sort_human)
    create_gui(mylist)


def user_input() -> "tuple[int, int]":
    print("What do you want filter?")
    print("Please choose:")
    print("1) Group address")
    print("2) Physical address")
    i = input("Enter number:")
    print("")
    if int(i) == 1:
        set_filter = FILTER_GROUP
    elif int(i) == 2:
        set_filter = FILTER_PHYSICAL
    else:
        print("Invalid number")
        exit()
    print("Please choose mode:")
    print("1) Filter telegramms")
    print("2) Filter last change")
    i = input("Enter number:")
    print("")
    if int(i) == 1:
        set_mode = MODE_TELEGRAMM
    elif int(i) == 2:
        set_mode = MODE_CHANGE
    else:
        print("Invalid number")
        exit()
    return set_filter, set_mode

def check_item(parent, iid, value):
    if tree.exists(iid)==True:
        print("item exist", iid)
        return True
    else:
        tree.insert(parent, "end", iid, text=value)
        return False

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(key=lambda t: int(t[0]), reverse=reverse)
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)


def create_gui(addresses):
    columns = ('number',)
    tree.heading('#0', text='groupaddresses', anchor='w')
    for address in addresses:
        main_num = str(num_sort(address, 0)) 
        check_item("", main_num, main_num)
        middel_num = main_num + "/" + str(num_sort(address, 1)) 
        check_item(main_num, middel_num, middel_num)
        tree.insert(middel_num, "end", text=address )

    print(tree.get_children(''))
    # treeview_sort_column(tree, "#0", False)


    tree.pack()
    root.mainloop()

def init() -> None:
    # set_filter, set_mode = user_input()
    start = time.time()
    # if set_mode == MODE_TELEGRAMM:
    #     filter_teregramms(group_addresses, set_filter)
    # if set_mode == MODE_CHANGE:
    #     filter_groupaddress_change(group_addresses, set_filter)

    find_filter_objekts()
    end = time.time()
    total_time = end - start
    print("needed time: ", total_time)


init()
