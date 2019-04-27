
import pickle
from src.write_facet import write_facet 

X = 0
Y = 1  
Z = 2
page_length_mm = 200  # bed size - 210x120 mm
page_height_mm = 120
page_depth_cm = 0.5 
page_offset = 0 
page_gui_canvas_x = 1100
page_gui_canvas_y = 680 

class asset(object):

    def __init__(self,x,y,mesh,file_name): 
        self.x_offset = (x/page_gui_canvas_x)*page_length_mm    #change scale to the printer bed size
        self.y_offset = (y/page_gui_canvas_y)*page_height_mm
        self.mesh = pickle.load(open(mesh,"rb"))
        self.half_x = self.mesh['x_half']
        self.half_y = self.mesh['y_half']
        self.file_name = file_name
        self.offset_points() 
        self.write_points()

    def offset_points(self):
        for facet in self.mesh['points']:
            for vertex in facet.keys():
                facet[vertex][X] = page_length_mm -(facet[vertex][X] + self.x_offset) + self.half_x + 2   # page_length_mm
                facet[vertex][Y] = (facet[vertex][Y] + self.y_offset) - self.half_y - 5    # height of the base page
                facet[vertex][Z] = facet[vertex][Z] + page_depth_cm

    def write_points(self):
        for triangle in self.mesh['points']:
            write_facet(self.file_name, 
                        str(triangle['vertex1'][0]), str(triangle['vertex1'][1]), str(triangle['vertex1'][2]), 
                        str(triangle['vertex2'][0]), str(triangle['vertex2'][1]), str(triangle['vertex2'][2]), 
                        str(triangle['vertex3'][0]), str(triangle['vertex3'][1]), str(triangle['vertex3'][2]) ) 





def make_page(placemnt,name):

    file_name = ".\pages/" + name + ".stl" 

    f = open(file_name,"w")
    f.write('solid ' +  name +'\n')
    f.close()
    
    # write the points for the page the assets sit on
    write_facet(file_name,0,0,0,0,page_height_mm,0,page_length_mm,0,0)
    write_facet(file_name,0,page_height_mm,0,page_length_mm,page_height_mm,0,page_length_mm,0,0)

    write_facet(file_name,0,0,page_depth_cm,0,page_height_mm,page_depth_cm,page_length_mm,0,page_depth_cm)
    write_facet(file_name,0,page_height_mm,page_depth_cm,page_length_mm,page_height_mm,page_depth_cm,page_length_mm,0,page_depth_cm)

    write_facet(file_name,0,0,0,0,0,page_depth_cm, page_length_mm,0,0)
    write_facet(file_name,0,0,page_depth_cm, page_length_mm,0,page_depth_cm, page_length_mm,0,0)
    
    write_facet(file_name,0,page_height_mm,0, 0,page_height_mm,page_depth_cm, page_length_mm,page_height_mm,0)
    write_facet(file_name,0,page_height_mm,page_depth_cm,page_length_mm,page_height_mm,page_depth_cm, page_length_mm,page_height_mm,0)

    write_facet(file_name,page_length_mm,0,0, page_length_mm,0,page_depth_cm, page_length_mm,page_height_mm,0)
    write_facet(file_name,page_length_mm,0,page_depth_cm, page_length_mm,page_height_mm,page_depth_cm, page_length_mm,page_height_mm,0)

    for key in placemnt.keys():
        ass = asset(placemnt[key]['X'], placemnt[key]['Y'], placemnt[key]['Path'][:-4]+'.p', file_name)

    f = open(file_name,"a")
    f.write('endsolid ' + name)
    f.close()