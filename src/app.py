#!/usr/bin/env python3
import xml.etree.ElementTree as ET

import gui
import knx
import xml_handler

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


def filter_teregramms(search_filter: "list[str]", filter_mode: int) -> None:
    """ghjklölkjhgfghjkjhgfdfjhgfertzu ggzuiuztretzu gzuztrthjhgf.

    dggzuiuztretzu
    '0/ggzuiuztretzu/14'
    """
    count_found_telegramms = 0
    count_removed_telegramms = 0
    myroot = xml_handler.get_xml(r"tests\sampel-1.xml")
    output_xml = ET.Element("CommunicationLog")

    for child in myroot:
        if child.tag == "{http://knx.org/xml/telegrams/01}Telegram":
            hex_val = child.attrib["RawData"]
            output = knx.decode(bytearray.fromhex(hex_val[8:]))
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
    xml_handler.create_xml(output_xml, "filter_teregramms2.xml")


def filter_groupaddress_change(search_filter: "list[str]", filter_mode: int) -> None:
    """ghjklölkjhgfghjkjhgfdfjhgfertzu ggzuiuztretzu gzuztrthjhgf.

    dggzuiuztretzu
    '0/ggzuiuztretzu/14'
    """
    myroot = xml_handler.get_xml("filter_teregramms2.xml")
    output_xml = ET.Element("CommunicationLog")
    group_values: "dict[str, bytearray]" = {}
    group_values_old: "dict[str, bytearray]" = {}

    for child in myroot:
        if child.tag == "{http://knx.org/xml/telegrams/01}Telegram":
            hex_val = child.attrib["RawData"]
            output = knx.decode(bytearray.fromhex(hex_val[8:]))
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

    xml_handler.create_xml(output_xml, "filter_on_change_teregramms.xml")


# helper function to perform sort


def user_input() -> "tuple[int, int]":
    """ghjklölkjhgfghjkjhgfdfjhgfertzu ggzuiuztretzu gzuztrthjhgf.

    dggzuiuztretzu
    '0/ggzuiuztretzu/14'
    """
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


def treeview_sort_column(tv, col, reverse):
    """ghjklölkjhgfghjkjhgfdfjhgfertzu ggzuiuztretzu gzuztrthjhgf.

    dggzuiuztretzu
    '0/ggzuiuztretzu/14'
    """
    l = [(tv.set(k, col), k) for k in tv.get_children("")]
    l.sort(key=lambda t: int(t[0]), reverse=reverse)
    for index, (val, k) in enumerate(l):
        tv.move(k, "", index)


def init() -> None:
    """ghjklölkjhgfghjkjhgfdfjhgfertzu ggzuiuztretzu gzuztrthjhgf.

    dggzuiuztretzu
    '0/ggzuiuztretzu/14'
    """
    gui.init()
    # # set_filter, set_mode = user_input()
    # start = time.time()
    # # if set_mode == MODE_TELEGRAMM:
    # #     filter_teregramms(group_addresses, set_filter)
    # # if set_mode == MODE_CHANGE:
    # #     filter_groupaddress_change(group_addresses, set_filter)

    # find_filter_objekts()

    # end = time.time()
    # total_time = end - start
    # print("needed time: ", total_time)


init()
