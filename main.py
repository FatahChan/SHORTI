from tkinter import *
import os
import subprocess as sp
import py_compile
# main window size
HEIGHT = 500
WIDTH = 1000



# fonts
HEl12B = ['Helvetica', '12', 'bold']
HEl10B = ['Helvetica', '10', 'bold']

# colors
Indigo_Dye = "#134074"
Prussian_Blue = "#13315C"
Oxford_Blue = "#0B2545"
Cadet_Grey = "#8DA9C4"
Mint_Cream = "#EEF4ED"
Mint_Green = "#B2FFA9"
Red_Orange_Color_Wheel = "#FF4A1C"
Maximum_Blue_Purple ="#B8B8F3"
# main window
root = Tk()

root.title("SHORTI")
canvas = Canvas(root, height=HEIGHT, width=WIDTH, bg=Prussian_Blue)
canvas.pack()

last_load_response = ""

# main frame
frame = Frame(root, bg=Prussian_Blue, bd=5)
frame.place(relx=0.5, rely=0.01, relwidth=.95, relheight=0.98, anchor='n')

# initiating frames
list_box_frame = Frame(frame, bg=Indigo_Dye, bd=5)
response_frame = Frame(frame, bg=Indigo_Dye, bd=5)
reload_frame = Frame(frame, bg=Indigo_Dye, bd=5)
# placing frames in main frame
list_box_frame.place(relx=0.005, rely=0.01, relwidth=.4, relheight=0.98)
response_frame.place(relx=0.420, rely=0.01, relwidth=.575, relheight=0.81)
reload_frame.place(relx=0.420, rely=0.84, relwidth=.575, relheight=0.15)


def AddtoAHK(response_name):
    with open("script.ahk", 'a') as f:
        f.write("\n\n")
        f.write(":or:" + response_name + ".::\n")
        f.write("FileRead, Clipboard, %A_ScriptDir%\\responses\\" + response_name + ".txt\n")
        f.write("Send, ^v\n")
        f.write("return")


def RemovefromAHK(response_name):
    f = open("script.ahk", 'r')
    lines = f.readlines()
    f.close()
    for i in range(len(lines)):
        if (":or:" + response_name + ".::\n") == lines[i]:
            del lines[i:i+4]
            break
    f = open("script.ahk", "w+")
    for line in lines:
        f.write(line)
    f.close()

#func reload AHK script and exit the program
def exit():
    sp.Popen("run.bat")
    root.destroy()


# func loads currently selected response in the listbox
def load_response():
    global last_load_response
    last_load_response = listbox.get(ANCHOR)
    if last_load_response != "":
        response_text.delete("1.0", END)
        with open("responses\\" + last_load_response + ".txt") as f:
            text_on_file = f.readlines()
            for i in text_on_file:
                response_text.insert(END, i)
            print(last_load_response, "Loaded")
        label_loaded.configure(text=last_load_response + " Loaded")


# save the text widget text to responsename.txt
def save_response():
    if last_load_response != "":
        # kill AHK
        os.system("TASKKILL /F /IM AutoHotkeyU64.exe")
        with open("responses\\" + last_load_response + ".txt", 'w+', encoding="utf-8") as f:
            f.write(response_text.get("1.0", END))
        print(last_load_response + " Saved")
        label_loaded.configure(text=last_load_response + " Saved")
        sp.Popen("run.bat")


def delete_listbox():
    print(listbox.get(ANCHOR), "Deleted")
    os.remove('responses\\' + str(listbox.get(ANCHOR)) + ".txt")
    RemovefromAHK(listbox.get(ANCHOR))
    listbox.delete(ANCHOR)


def create_response_save(newResponse):
    if " " not in newResponse and newResponse != "":
        f = open("responses\\" + newResponse + ".txt", "w+")
        if not (newResponse in listbox.get(0, "end")):
            listbox.insert(END, newResponse)
            print(newResponse, "Added")
            AddtoAHK(newResponse)
            popup.destroy()
        else:
            print(newResponse, "Already exist")
            create_label_warning.configure(text=newResponse + " Already exist")
        f.close()
    else:
        print("Invalid Response Name")
        create_label_warning.configure(text="Invalid Response Name")




def create_response():
    global popup
    popup = Toplevel()
    popup_canvas = Canvas(popup, height=100, width=700, bg=Prussian_Blue)
    popup_canvas.pack()
    popup_frame = Frame(popup, bg=Prussian_Blue, bd=10)
    popup_frame.place(relx=0.5, rely=0.01, relwidth=1, relheight=1, anchor='n')
    create_label = Label(popup_frame,
                         text="Please use two words to make shorti (eg. hichat) to activate type (hichat.) then space",
                         font=HEl12B,
                         bg=Indigo_Dye,
                         fg="#63ADF2")
    create_entry = Entry(popup_frame, font=HEl12B)
    create_label.place(relx=0.005, relwidth=.99, relheight=0.25)
    global create_label_warning
    create_label_warning = Label(popup_frame, text="", font=HEl12B, bg=Mint_Green, fg=Oxford_Blue)
    create_label_warning.place(relx=0.005, rely=0.75, relwidth=.8, relheight=0.3)
    create_entry.place(relx=0.005, rely=0.35, relwidth=.99, relheight=0.3)
    create_save_button = Button(popup_frame,
                                text="Save",
                                font=HEl12B,
                                command=lambda: create_response_save(create_entry.get()))
    create_save_button.place(relx=0.815, rely=0.75, relwidth=.18, relheight=0.3)
    popup.mainloop()


listbox = Listbox(list_box_frame, bd=5, font=HEl12B, selectmode='SINGLE', bg=Cadet_Grey, fg=Oxford_Blue)
for i in (os.listdir('responses\\')):
    i = i.replace(".txt", '')
    listbox.insert(END, i)

load_button = Button(list_box_frame, text="Load", font=HEl12B, command=load_response, bd=5, activebackground=Red_Orange_Color_Wheel, fg=Oxford_Blue)
create_button = Button(list_box_frame, text="Create New Response", font=HEl12B, command=create_response, bd=5, activebackground=Red_Orange_Color_Wheel, fg=Oxford_Blue)
delete_button = Button(list_box_frame, text="Delete", font=HEl12B, command=delete_listbox, bd=5, activebackground=Red_Orange_Color_Wheel, fg=Oxford_Blue)

response_text = Text(response_frame, font=HEl10B, bg=Cadet_Grey, fg=Oxford_Blue)
response_save_button = Button(response_frame, text="Save", font=HEl12B, command=save_response, bd=5, activebackground=Red_Orange_Color_Wheel, fg=Oxford_Blue)
label_loaded = Label(response_frame, text="No response loaded", font=HEl12B, bg=Mint_Green)

reload_button = Button(reload_frame, text="RELOAD & EXIT", font=HEl12B, command=exit, bd=5, activebackground=Red_Orange_Color_Wheel, fg=Oxford_Blue)

response_text.place(relx=0.005, rely=0.005, relwidth=.99, relheight=0.75)
listbox.place(relx=0.005, rely=0.005, relwidth=.99, relheight=0.80)
label_loaded.place(relx=0.05, rely=0.78, relwidth=.9, relheight=0.1)
create_button.place(relx=0.05, rely=0.82, relwidth=.90, relheight=0.05)
load_button.place(relx=0.05, rely=0.88, relwidth=.90, relheight=0.05)
delete_button.place(relx=0.05, rely=0.94, relwidth=.90, relheight=0.05)
response_save_button.place(relx=0.05, rely=0.9, relwidth=.90, relheight=0.1)
reload_button.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

# main window loop
root.mainloop()