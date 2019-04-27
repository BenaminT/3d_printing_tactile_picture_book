
from tkinter import * 
from tkinter import filedialog, messagebox, simpledialog
import os
import pickle
from PIL import ImageTk, Image
import src.layout_page_stl as gen_page


# ---------------------------------
#    GLOBAL VARS 
# ---------------------------------

current_image_selection = ''
curent_image_file_data = '' 
images = []
canvas_locations = {}
canvas_asset = 1
page_name = ""


# -----------------------------------------------------------------
#                               MAIN
# -----------------------------------------------------------------

root = Tk()
root.title("Create Page")
root.geometry('1465x700')
root.configure(background='grey')

frame = Frame(root)
frame.grid(row = 0, column =0, sticky='n')
frame.configure(background='grey')

# ---------------------------------------------------
#           MAKE MENU
# ---------------------------------------------------

def run_page_gen():
   gen_page.make_page(canvas_locations,page_name)


def set_page_size(): 
  print('size')

def set_page_name(): 
  global page_name
  page_name = simpledialog.askstring("Page Name ", "Enter name")


menubar = Menu(root)
root.config(menu=menubar)

fileMenu = Menu(menubar)
fileMenu.add_command(label='Gen Page', command=run_page_gen)
#fileMenu.add_command(label='Set Page Size', command=set_page_size)
fileMenu.add_command(label='Set Page Name', command=set_page_name)

menubar.add_cascade(label = 'File', menu=fileMenu)


# ---------------------------------------------------
#           MAKE ASSET TEXT
# ---------------------------------------------------
lbl = Label(frame, text="  Assets: ",font=( '14'))
lbl.grid(column=0, row=1)
lbl.configure(background='grey')




# ---------------------------------------------------
#                MAKE SCROLL BAR 
# ---------------------------------------------------
def get_dirs():
    path = os.getcwd() +'/assets'
    dirs = [name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name))]
    return dirs


def load_image(dir):
    global current_image_selection, curent_image_file_data
    path = os.getcwd() + '/assets/' + dir + '/' + dir + '.png'
    curent_image_file_data = os.getcwd() + '/assets/' + dir + '/' + dir + '.p'
    current_image_selection = path
    image = Image.open(path)
    image = image.resize((220,200),Image.ANTIALIAS)
    img = ImageTk.PhotoImage( image )
    panel = Label(frame, image = img)
    return panel,img


def display_info(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    name = w.get(index)
    panel,img = load_image(name)
    panel.image = img
    panel.grid(column=0, row=20)


#creating the scrollbar and list
scrollbar= Scrollbar(frame)
scrollbar.grid(row=1,column=3, rowspan=5, sticky=N+S)
mylist=Listbox(frame, height=18, width=35, yscrollcommand=scrollbar.set, font=('14') )
mylist.grid(row=1,column=2,rowspan=5,sticky=E+W)
scrollbar.config(command=mylist.yview)
mylist.bind('<<ListboxSelect>>',display_info)


#setting the list items:
dirs = get_dirs()
for dir in dirs:
   mylist.insert(END,  str(dir) )

#layout for the list and scrollbar
mylist.grid(column=0, row=1,sticky='nw')




# ---------------------------------------------------
#                MAKE BREAK LINE 
# ---------------------------------------------------
lbl2 = Label(frame, text=" ")
lbl2.grid(column=0, row=18)
lbl2.configure(background='grey')




# ---------------------------------------------------
#              MAKE ASSET INFO TEXT 
# ---------------------------------------------------
lbl3 = Label(frame, text="Asset Info: ", font=( '14') ) 
lbl3.grid(column=0, row=19)
lbl3.configure(background='grey')

#make the blank placeholder image
path = os.getcwd() + '/src/blank.png'
image = Image.open(path)
image = image.resize((220,200),Image.ANTIALIAS)
img = ImageTk.PhotoImage( image )
panel = Label(frame, image = img) 
panel.image = img
panel.grid(column=0, row=20)




# ---------------------------------------------------
#                MAKE BREAK LINE 
# ---------------------------------------------------
lbl2 = Label(frame, text=" ")
lbl2.grid(column=0, row=21)
lbl2.configure(background='grey')




# ---------------------------------------------------
#              INSERT ASSET BUTTON 
# ---------------------------------------------------
def insert_asset():

   global canvas_asset
   image = Image.open(current_image_selection)

   if (pickle.load(open(curent_image_file_data,"rb"))['size'] == 'small'):
      image = image.resize((220,230),Image.ANTIALIAS)  #resize the image

   elif (pickle.load(open(curent_image_file_data,"rb"))['size'] == 'large'):
      image = image.resize((550,480),Image.ANTIALIAS)  #resize the image

   img = ImageTk.PhotoImage( image )
   images.append(img)
   
   canvas1.create_image(940,140,image=img)  # place the image 

   canvas_locations[canvas_asset] = {'X' : 0, 'Y': 0, 'Path' : current_image_selection}
   canvas_asset = canvas_asset + 1


btn = Button(frame, text="Insert Asset", command=insert_asset)
btn.grid(column=0, row=22)



# ---------------------------------------------------
#                MAKE BREAK LINE 
# ---------------------------------------------------
lbl2 = Label(frame, text=" ")
lbl2.grid(column=0, row=23)
lbl2.configure(background='grey')



# ---------------------------------------------------
#                MAKE BREAK LINE 
# ---------------------------------------------------
lbl2 = Label(frame, text=" ")
lbl2.grid(column=4, row=0)
lbl2.configure(background='grey')



# ---------------------------------------------------
#                 CANVAS CREATION   
# ---------------------------------------------------

canvas1 = Canvas(root,width = 1100, height = 680, background = 'white')   #1100 = 210   and   680 = 148

drag_data = {"x": 0, "y": 0, "item": None}

def on_token_press( event):
    '''Begining drag of an object'''
    # record the item and its location
    drag_data["item"] = canvas1.find_closest(event.x, event.y)[0]
    drag_data["x"] = event.x
    drag_data["y"] = event.y
    
   
def on_token_release(event):
    '''End drag of an object'''
    canvas_locations[drag_data["item"]]['X'] = drag_data["x"]
    canvas_locations[drag_data["item"]]['Y'] = drag_data["y"]
    print(drag_data["x"],drag_data["y"])
    # reset the drag information
    drag_data["item"] = None
    drag_data["x"] = 0
    drag_data["y"] = 0


def on_token_motion(event):
    '''Handle dragging of an object'''
    # compute how much the mouse has moved
    delta_x = event.x - drag_data["x"]
    delta_y = event.y - drag_data["y"]
    # move the object the appropriate amount
    canvas1.move(drag_data["item"], delta_x, delta_y)
    # record the new position
    drag_data["x"] = event.x
    drag_data["y"] = event.y

canvas1.bind("<ButtonPress-1>", on_token_press)
canvas1.bind("<ButtonRelease-1>", on_token_release)
canvas1.bind("<B1-Motion>", on_token_motion)


canvas1.grid(column=1, row=0)


root.mainloop()