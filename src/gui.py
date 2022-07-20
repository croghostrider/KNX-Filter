#!/usr/bin/env python3
import re
import tkinter as tk
from ttkwidgets import CheckboxTreeview

root = tk.Tk()

tree = CheckboxTreeview(root)

def num_sort(test_string, pos):
    return list(map(int, re.findall(r"\d+", test_string)))[pos]
    
def check_item(parent, iid, value):
    if tree.exists(iid) == True:
        print("item exist", iid)
        return True
    else:
        tree.insert(parent, "end", iid, text=value)
        return False

def create_gui(addresses):
    columns = ("number",)
    tree.heading("#0", text="groupaddresses", anchor="w")
    for address in addresses:
        main_num = str(num_sort(address, 0))
        check_item("", main_num, main_num)
        middel_num = main_num + "/" + str(num_sort(address, 1))
        check_item(main_num, middel_num, middel_num)
        tree.insert(middel_num, "end", text=address)

    print(tree.get_children(""))
    tree.pack()
    root.title("KNX-Filter")
    x = root.winfo_screenwidth() // 2
    y = int(root.winfo_screenheight() * 0.1)
    root.geometry("500x600+" + str(x) + "+" + str(y))

    root.mainloop()