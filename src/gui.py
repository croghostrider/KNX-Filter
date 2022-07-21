#!/usr/bin/env python3
import re
import tkinter as tk
from tkinter import filedialog as fd, ttk

from ttkwidgets import CheckboxTreeview

import xml_handler

global root
global tree


def init():
    """ghjklölkjhgfghjkjhgfdfjhgfertzu ggzuiuztretzu gzuztrthjhgf.

    dggzuiuztretzu
    '0/ggzuiuztretzu/14'
    """

    root = tk.Tk()
    root.title("KNX-Filter")
    # x = root.winfo_screenwidth() // 2
    # y = int(root.winfo_screenheight() * 0.1)
    # root.geometry("500x600+" + str(x) + "+" + str(y))
    tree = CheckboxTreeview(root, height=15)
    tree.grid(row=0, column=0, sticky="n")
    tree.heading("#0", text="Group Addresses", anchor="w")
    scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    tree2 = CheckboxTreeview(root, height=15)
    tree2.grid(row=0, column=2, sticky="n")
    tree2.heading("#0", text="Physical Addresses", anchor="w")
    scrollbar2 = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree2.yview)
    tree2.configure(yscroll=scrollbar2.set)
    scrollbar2.grid(row=0, column=3, sticky="ns")
    my_btn = tk.Button(root, text="Open File", command=open)
    my_btn.grid(row=1, column=2, sticky="e")
    root.mainloop()


def open():
    """ghjklölkjhgfghjkjhgfdfjhgfertzu ggzuiuztretzu gzuztrthjhgf.

    dggzuiuztretzu
    '0/ggzuiuztretzu/14'
    """
    global data_filter
    root.filename = fd.askopenfilename(title="Select A File")
    data_filter = xml_handler.find_filter_objekts(root.filename)
    if len(root.filename) > 35:
        root.filename = root.filename[-35:]
    my_label = tk.Label(root, text=root.filename)
    my_label.grid(row=1, column=0)


def num_sort(test_string, pos):
    """ghjklölkjhgfghjkjhgfdfjhgfertzu ggzuiuztretzu gzuztrthjhgf.

    dggzuiuztretzu
    '0/ggzuiuztretzu/14'
    """
    return list(map(int, re.findall(r"\d+", test_string)))[pos]


def check_item(parent, iid, value):
    """ghjklölkjhgfghjkjhgfdfjhgfertzu ggzuiuztretzu gzuztrthjhgf.

    dggzuiuztretzu
    '0/ggzuiuztretzu/14'
    """
    if tree.exists(iid) == True:
        return True
    tree.insert(parent, "end", iid, text=value)
    return False


def create_gui(addresses, phys):
    """ghjklölkjhgfghjkjhgfdfjhgfertzu ggzuiuztretzu gzuztrthjhgf.

    dggzuiuztretzu
    '0/ggzuiuztretzu/14'
    """
    for address in addresses:
        main_num = str(num_sort(address, 0))
        check_item("", main_num, main_num)
        middel_num = main_num + "/" + str(num_sort(address, 1))
        check_item(main_num, middel_num, middel_num)
        tree.insert(middel_num, "end", text=address)

    print(tree.get_children(""))
