#Vajda Tibor

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import pymongo

# your url
connectionURL=""

client = pymongo.MongoClient(connectionURL)

db = client["database"]

table = db["table"]

window = Tk()
window.title('MongoDB')
window.geometry("350x600")
window.resizable(width=False, height=False)


def add():
    name = nameText.get()
    address = addressText.get()
    gender = radioGender.get()
    relationship = cb.get()
    if name=="" or address=="":
       messagebox.showwarning("Empty", "Name or Address is empty!")
    else:
      row = {"name": name, "address": address,
            "gender": gender, "relationship": relationship}
      table.insert_one(row)
      list_all()


def list_all():
    tv.delete(*tv.get_children())
    for x in table.find():
        tv.insert(parent='', index=0, values=(
            x["name"], x["address"], x["gender"], x["relationship"]))


def select():
    selected = tv.focus()
    if selected:
      global temp
      temp = tv.item(selected, 'values')
      nameText.delete(0, END)
      addressText.delete(0, END)
      nameText.insert(0, temp[0])
      addressText.insert(0, temp[1])
      radioGender.set(temp[2])
      cb.set(temp[3])
      list_all()
    else:
       messagebox.showwarning("Select", "Select a row!")


def update():
    query = {"name": temp[0], "address": temp[1],
             "gender": temp[2], "relationship": temp[3]}
    name = nameText.get()
    address = addressText.get()
    gender = radioGender.get()
    relationship = cb.get()
    if name=="" or address=="":
       messagebox.showwarning("Empty", "Name or Address is empty!")
    else:
      row = {"$set": {"name": name, "address": address,
                     "gender": gender, "relationship": relationship}}
      table.update_one(query, row)
      list_all()


def delete():
    query = {"name": temp[0], "address": temp[1],
             "gender": temp[2], "relationship": temp[3]}
    table.delete_one(query)
    list_all()


# name
lbl = Label(window, text="Name:")
lbl.place(x=20, y=20)
nameText = Entry(window, text="")
nameText.place(x=80, y=20)

# address
lbl = Label(window, text="Address:")
lbl.place(x=20, y=60)
addressText = Entry(window, text="")
addressText.place(x=80, y=60)

# gender
lbl = Label(window, text="Gender:")
lbl.place(x=20, y=100)
radioGender = StringVar()
radioGender.set("male")
r1 = Radiobutton(window, text="male", variable=radioGender, value="male")
r2 = Radiobutton(window, text="female", variable=radioGender, value="female")
r3 = Radiobutton(window, text="other", variable=radioGender, value="other")
r1.place(x=80, y=100)
r2.place(x=140, y=100)
r3.place(x=200, y=100)

# relationship
lbl = Label(window, text="Relationship status:")
lbl.place(x=20, y=140)
data = ("Single", "In a relationship", "Married", "Complicated")
cb = Combobox(window, values=data, state="readonly")
cb.set(data[0])
cb.place(x=140, y=140)

# add btn
btn = Button(window, text="Add new", command=lambda: add())
btn.place(x=20, y=180)

# refresh btn
btn = Button(window, text="Refresh", command=lambda: list_all())
btn.place(x=260, y=180)

# select btn
btn = Button(window, text="Select", command=lambda: select())
btn.place(x=260, y=550)

# update btn
btn = Button(window, text="Update", command=lambda: update())
btn.place(x=20, y=550)

# Delete btn
btn = Button(window, text="Delete", command=lambda: delete())
btn.place(x=100, y=550)

# TableView
tv = Treeview(
    columns=(1, 2, 3, 4),
    show='headings',
    height=15,
)
tv['columns'] = ('Name', 'Address', 'Gender', 'Relationship')
tv.column('Name', anchor=CENTER, width=80)
tv.column('Address', anchor=CENTER, width=80)
tv.column('Gender', anchor=CENTER, width=80)
tv.column('Relationship', anchor=CENTER, width=80)

tv.heading('Name', text='Name', anchor=CENTER)
tv.heading('Address', text='Address', anchor=CENTER)
tv.heading('Gender', text='Gender', anchor=CENTER)
tv.heading('Relationship', text='Relationship', anchor=CENTER)
list_all()
tv.place(x=15, y=220)

window.mainloop()
