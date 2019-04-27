from tkinter import * 
from tkinter import filedialog, messagebox
import os
import src.trace_and_create_data as tool_1


window = Tk()
window.title("Create Asset")
window.geometry('480x235')


# -----------------------------------------------------------------------------
# Make the blank row
lbl = Label(window, text="")
lbl.grid(column=0, row=0)

# first row 
asset_path = StringVar()
asset_path.set("")

def get_file_path():
    window.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("png files","*.png")))
    asset_path.set(window.filename)

lbl3 = Label(window, text="Path to asset image: ")
lbl3.grid(column=0, row=1)

txt = Entry(window,width=35, textvariable=asset_path)
txt.grid(column=2, row=1)

btn = Button(window, text="Select file", command=get_file_path)
btn.grid(column=4, row=1)


# -----------------------------------------------------------------------------

# Make the blank row
lbl2 = Label(window, text="")
lbl2.grid(column=0, row=2)

# row for asset name
asset_name = StringVar()
asset_name.set("")

lbl4 = Label(window, text="Asset name: ")
lbl4.grid(column=0, row=3)

txt = Entry(window,width=35, textvariable=asset_name)
txt.grid(column=2, row=3)


# -----------------------------------------------------------------------------

# Make the blank row
lbl6 = Label(window, text="")
lbl6.grid(column=0, row=4)

height = IntVar() 
lbl7 = Label(window, text="Asset Height (in mm): ")
lbl7.grid(column=0, row=5)

txt1 = Entry(window,width=35, textvariable=height)
txt1.grid(column=2, row=5)

# -----------------------------------------------------------------------------

# Make the blank row
lbl5 = Label(window, text="")
lbl5.grid(column=0, row=6)

small = IntVar() 
cb1 = Checkbutton(window,variable=small, onvalue=1,offvalue=0,text="Small")
cb1.grid(column=1, row=7)

large = IntVar()
cb2 = Checkbutton(window,variable=large, onvalue=1,offvalue=0,text="Large")
cb2.grid(column=2, row=7)

# Make the blank row
lbl = Label(window, text="")
lbl.grid(column=0, row=8)

# -----------------------------------------------------------------------------

# create button
def create_asset():

    if (asset_path.get() == ""):
        messagebox.showwarning('Warning', 'No path gievn to the asset image')

    elif (asset_name.get() == ""): 
        messagebox.showwarning('Warning', 'No name given for the asset')

    elif (int(height.get())<1):
        messagebox.showwarning('Warning', 'Height needs to be set')
    
    elif (small.get() == 1 or large.get() == 1 ):

        if (small.get() == 1):
            result = tool_1.run(str(asset_path.get()), str(asset_name.get()), True, int(height.get()))
        else: 
            result = tool_1.run(str(asset_path.get()), str(asset_name.get()), False, int(height.get()))
    
        if (result[0]):
            
            messagebox.showinfo('Success', 'Assett ' + asset_name.get() + ' Created successfully')
            window.destroy()
        else: 
            messagebox.showinfo('Failure', 'Assett not created due to: ' + result[1])
    
    else:
        messagebox.showwarning('Warning', 'Please seclect either large or small size')
            

btn = Button(window, text="create asset", command=create_asset)
btn.grid(column=0, row=9)
window.mainloop()