from tkinter import *
from tkinter.filedialog import *
from functools import partial
import os
from shutil import copyfile
root = Tk()
root.title('TuTurDuDur\'s datapack generator')

upper_part = Label()
upper_part.grid(row=0,column=0)

# LabelFrame pack.png

pack_png = LabelFrame(upper_part, text= "pack.png", padx=20, pady=20)
pack_png.grid(column=0,row=0)

photo = ""
canvas = ""
image_path = StringVar()
def chose_image(frame):
    global photo, canvas, image_path
    image_path.set(askopenfilename(title="Chose an image",filetypes=[('png files','.png')]))
    photo = PhotoImage(file=image_path.get())
    canvas = Canvas(frame, width=photo.width(), height=photo.height(), bg="white")
    canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.grid(row=0,column=0)

image_frame = Frame(pack_png)
image_frame.grid(row=1, column=0)

button_image = Button(pack_png, text="Chose an image", command=partial(chose_image, image_frame))
button_image.grid(row=0,column=0)


# LabelFrame pack.mcmeta

pack_infos = LabelFrame(upper_part, text= "Pack infos", padx=20, pady=20)
pack_infos.grid(column=1,row=0)

# pack name

name_label = Label(pack_infos, text="Pack name:\t")
name_label.grid(row=0,column=0)

name_stringvar = StringVar()
name_stringvar.set("New Datapack")

name_entry = Entry(pack_infos, textvariable=name_stringvar, width = 50)
name_entry.grid(row=0,column=1)

# descprition

description_label = Label(pack_infos, text="Description:\t")
description_label.grid(row=1,column=0)

description_stringvar = StringVar()
description_stringvar.set("The best minecraft datapack ever created!")

description_entry = Entry(pack_infos, textvariable=description_stringvar, width = 50)
description_entry.grid(row=1,column=1)

# pack_format

format_label = Label(pack_infos, text="Pack Format :\t")
format_label.grid(row=2,column=0)

format_spinbox = Spinbox(pack_infos, from_=4, to=9,width=48)
format_spinbox.grid(row=2, column=1)

# LabelFrame data
data = LabelFrame(root, text = "data", padx=20, pady=20)
data.grid(row=1,column=0)

# namespace
namespace_label = Label(data, text="Namespace :\t")
namespace_label.grid(row=0,column=1)

namespace_stringvar = StringVar()
namespace_stringvar.set("tuturduduristhebest")

namespace_entry = Entry(data, textvariable=namespace_stringvar, width=50)
namespace_entry.grid(row=0,column=2)

# tick.mcfunction
createtick_checkvar = IntVar()
create_tick = Checkbutton(data, text = "Create a tick function ?", variable=createtick_checkvar)
create_tick.grid(row=1,column=0)

tickname_label = Label(data, text="Function name :\t")
tickname_label.grid(row=1,column=1)

tickname_stringvar = StringVar()
tickname_stringvar.set("tick")

tickname_entry = Entry(data, textvariable=tickname_stringvar, width=50)
tickname_entry.grid(row=1,column=2)

# load.mcfunction
createload_checkvar = IntVar()
create_load = Checkbutton(data, text = "Create a load function ?", variable=createload_checkvar)
create_load.grid(row=2,column=0)

loadname_label = Label(data, text="Function name :\t")
loadname_label.grid(row=2,column=1)

loadname_stringvar = StringVar()
loadname_stringvar.set("load")

loadname_entry = Entry(data, textvariable=loadname_stringvar, width=50)
loadname_entry.grid(row=2,column=2)

# Create button
def create(pack_name, image_path, namespace, descrpition, format, createtick, tickname, createload, loadname):
    NAME = pack_name.get()
    DESCRIPTION = descrpition.get()
    FORMAT = int(format.get())
    NAMESPACE= namespace.get()
    TICK = tickname.get()
    LOAD = loadname.get()
    CREATE_TICK = createtick.get()
    CREATE_LOAD = createload.get()
    IMAGE_PATH = image_path.get()
    def create_folder(name):
        try:
            os.mkdir(name)
        except FileExistsError:
            pass

    create_folder(NAME)

    # Creates pack.mcmeta:
    PACK_MCMETA=open(NAME+"/pack.mcmeta","w")
    PACK_MCMETA.write("""{
"pack": {
    "pack_format": %s,
    "description": \"%s\"
    }
}    """%(FORMAT,DESCRIPTION))
    PACK_MCMETA.close()


    if IMAGE_PATH != "" or True:
        copyfile(IMAGE_PATH, NAME+"/pack.png")
    # Creates data and functions folders:
    
    create_folder(NAME+"/data")
    if CREATE_LOAD or CREATE_TICK:
        create_folder(NAME+"/data/minecraft")
        create_folder(NAME+"/data/minecraft/tags")
        create_folder(NAME+"/data/minecraft/tags/functions")
        create_folder(NAME+"/data/"+NAMESPACE)
        create_folder(NAME+"/data/"+NAMESPACE+"/functions")
    if CREATE_TICK:
        with open(NAME+"/data/minecraft/tags/functions/tick.json","w") as tick:
            tick.write("""{
"values":[
    \"%s:%s\"
    ]
}"""%(NAMESPACE, TICK))
        with open(NAME+"/data/%s/functions/%s.mcfunction"%(NAMESPACE,TICK),"w"):
            pass


    if CREATE_LOAD:
        with open(NAME+"/data/minecraft/tags/functions/load.json","w") as load:
            load.write("""{
"values":[
    \"%s:%s\"
    ]
}"""%(NAMESPACE, LOAD))

        with open(NAME+"/data/%s/functions/%s.mcfunction"%(NAMESPACE,TICK),"w"):
            pass

final_button = Button(root,text="Create the datapack", command=partial(create,name_stringvar,image_path, namespace_entry, description_stringvar, format_spinbox, createtick_checkvar, tickname_entry, createload_checkvar, loadname_entry))
final_button.grid(row=2,column=0)

root.mainloop()
