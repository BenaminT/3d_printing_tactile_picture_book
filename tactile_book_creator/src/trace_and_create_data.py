'''
Name: trace_and_create_data 

Desc: This the script called by the create asset application. It will load an image to be copied. The user will outline the image
       and then add anything they want embossed as well. 

Output: 

Author: Benjamin Thomas 
Project: Final year project - 3d printing childrens picture books 
'''

# -------------------------------------------------------------------------
#                               IMPORTS
# -------------------------------------------------------------------------
import cv2
import numpy as np
import matplotlib.pyplot as plt
import triangle
import pickle
import os 
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
#                                GLOBAL DEFS
# -------------------------------------------------------------------------
X = 0                      # used for indexing arrays 
Y = 1 
Z = 2 
points = []                # stores all the points clicked for the main outline
embossed = []              # stores arrays of all points used fro embossing lines 
new_emboss = []            # stores the poitns for embossed linse 
embossing_flag = False     # used as a flag to know when the user is embossing 
embossing_width = 0.3      # width in cm of an embossed line
embossing_height = 0.75    # heihgt in cm of an embossed line
embossing_dir = ''         # direction of the embossing line Y - vertical, X - horizontal
object_data = {}           # data to be returned at the end for the object
object_data['points'] = [] # init the data list

image_disaply_size = 500   # diaply size of the image to be traced

Small = True
scale = 80                 # up scale the size of the object by 80/50 
# -------------------------------------------------------------------------



def trace_image(image_path):

    global  points, embossed, new_emboss, embossing_flag

    def click_co(event, x ,y, flags, param):
        if (event == cv2.EVENT_LBUTTONDOWN):
            #print(x,y)
            if not embossing_flag:
                points.append([(x/image_disaply_size)*scale,((y/image_disaply_size)*scale)])
            else:
                new_emboss.append([(x/image_disaply_size)*scale,((y/image_disaply_size)*scale),embossing_dir]) 

    img = cv2.imread(image_path)
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_co)
    npImg = np.array(img)
    indices = np.argwhere(npImg == 0 )
    resized = cv2.resize(img,(image_disaply_size,image_disaply_size))

    while True:
        cv2.imshow("image",resized)   #resized
        key = cv2.waitKey(1) & 0xFF
 
        # if the 'c' key is pressed, break from the loop
        if key == ord("c"):
            if len(new_emboss) != 0:
                 embossed.append(new_emboss)
            cv2.destroyAllWindows()
            break
        
        # if n is pressed start a new line for embossing
        if key == ord("y"):
            if not embossing_flag:
                embossing_flag = True 
            else:
                embossed.append(new_emboss)
                new_emboss = []
            embossing_dir = 'Y'
        
        if key == ord("x"):
            if not embossing_flag:
                embossing_flag = True
            else:
                embossed.append(new_emboss)
                new_emboss = []
            embossing_dir = 'X' 
    return points





#calculate the segsments for constrinated triangulation
def simple_segs(points):
    segs = []
    for each in range(len(points)):
        if each == len(points) - 1:
            segs.append([each,0])
        else:
            segs.append([each,each+1])
    return segs





# create the points for hte top face
def create_top_points(points,height):
    top_layer_points = []
    for point in points:
        top_layer_points.append( [ point[X] , point[Y], height ] )
    return top_layer_points





#bring the object down to that it is sittong on the x and y axis
def noramlise_points(points):
    x = [] 
    y = [] 
    
    for point in points: 
        x.append(point[X])
        y.append(point[Y])

    x_min = min(x)
    y_min = min(y)

    for point in points:
        point[X] = point[X] - x_min
        point[Y] = point[Y] - y_min
    for item in embossed:
        for point in item: 
            point[X] = point[X] - x_min
            point[Y] = point[Y] - y_min
            



#write a facet to a file
def write_facet(v1_x,v1_y,v1_h, v2_x,v2_y,v2_h, v3_x,v3_y,v3_h):
    point = {}
    point['vertex1'] = [v1_x,v1_y,v1_h] 
    point['vertex2'] = [v2_x,v2_y,v2_h] 
    point['vertex3'] = [v3_x,v3_y,v3_h] 
    object_data['points'].append(point)




#Make the sides of the main object. Give it the point of the botom face and the height  
def make_3d( points, height, emboss):

    if not emboss:
        top_layer_points = create_top_points(points,height)
        for point in range(len(points)):
            if point == (len(points) - 1):
                write_facet( points[point][X],           points[point][Y],    0.0 ,
                               top_layer_points[point][X], top_layer_points[point][Y], top_layer_points[point][Z],
                               points[0][X],               points[0][Y],               0.0  )

                write_facet( top_layer_points[point][X], top_layer_points[point][Y], top_layer_points[point][Z],
                               top_layer_points[0][X],     top_layer_points[0][Y],     top_layer_points[0][Z],
                               points[0][X],               points[0][Y],               0.0   )

            else:
                write_facet( points[point][X],           points[point][Y],            0.0,
                               top_layer_points[point][X], top_layer_points[point][Y],  top_layer_points[point][Z],
                               points[point+1][X],         points[point+1][Y],          0.0  )

                write_facet( top_layer_points[point][X],   top_layer_points[point][Y],    top_layer_points[point][Z],
                               top_layer_points[point+1][X], top_layer_points[point+1][Y],  top_layer_points[point+1][Z],
                               points[point+1][X],           points[point+1][Y],            0.0  )
    else: 
        top_layer_points = create_top_points(points,height+embossing_height)
        for point in range(len(points)):
            if point == (len(points) - 1):
                write_facet( points[point][0],           points[point][1],           points[point][2],
                               top_layer_points[point][0], top_layer_points[point][1], top_layer_points[point][2],
                               points[0][0],               points[0][1],               points[point][2]  )

                write_facet( top_layer_points[point][0], top_layer_points[point][1], top_layer_points[point][2],
                               top_layer_points[0][0],     top_layer_points[0][1],     top_layer_points[0][2],
                               points[0][0],               points[0][1],               points[point][2]   )
            else:
                write_facet( points[point][0],           points[point][1],            points[point][2],
                               top_layer_points[point][0], top_layer_points[point][1],  top_layer_points[point][2],
                               points[point+1][0],         points[point+1][1],          points[point][2]  )

                write_facet( top_layer_points[point][0],   top_layer_points[point][1],    top_layer_points[point][2],
                               top_layer_points[point+1][0], top_layer_points[point+1][1],  top_layer_points[point+1][2],
                               points[point+1][0],         points[point+1][1],            points[point][2]  )



#write the two planes, one at the bottom and one height above
def write_planes(v1,v2,v3,height):
   
    write_facet(v1[0],v1[1],0.0,
                  v2[0],v2[1],0.0,
                  v3[0],v3[1],0.0)

    write_facet(v2[0],v2[1],height,
                  v1[0],v1[1],height,
                  v3[0],v3[1],height)




# write the vertexs for the top and bottom planes in the stl
def generate_object(image_path,height):
    
    points = trace_image(image_path)
    segs = simple_segs(points)
    tri = triangle.triangulate({'vertices': points, 'segments' :segs }, 'pf' )
    
    # Create a view of the two sides
    #p_array = dict(vertices=np.array(points))
    #triangle.compare(plt, p_array, tri)
    #plt.show()
    
    for triangle_obj in tri['triangles']:
        write_planes(points[triangle_obj[0]], points[triangle_obj[1]], points[triangle_obj[2]], height)
    make_3d(points,height,False)

  

# calcualte the emobssin points given a line. 
# Add and reomve the wdith set from teh point to create a 3d line to be printed 
def calc_embossing():
    all_embossed = [] 
    for data in embossed:
        points_min = []
        points_add = []
        for point in data:
            if point[2] == 'Y':
                points_add.append( [ point[X]+embossing_width, point[Y] ] ) 
                points_min.append( [ point[X]-embossing_width, point[Y] ] )
            elif point[2] == 'X':
                points_add.append( [ point[X], point[Y]+embossing_width ] ) 
                points_min.append( [ point[X], point[Y]-embossing_width ] )
        points_min = list(reversed(points_min))
        emboss_points = points_add + points_min
        all_embossed.append(emboss_points)
    return all_embossed



# Go though all of the embossed lines drawn by the user and create them to be pritned.
def generate_embossing(height):
 
    embs = calc_embossing()
    keys = ['vertex1','vertex2','vertex3'] 
    
    for emb in embs:
        segs = simple_segs(emb)
        tri = triangle.triangulate({'vertices': np.array(emb),'segments' :segs }, 'pf' )
        
        for trian in tri['triangles']:
            point = {}
            ref = 0
            for vertex in trian:
                point[keys[ref]] = [emb[vertex][X], emb[vertex][Y], height]    
                ref = ref + 1
            object_data['points'].append(point)

        for trian in tri['triangles']:
            point = {}
            ref = 0
            for vertex in trian:
                point[keys[ref]] = [emb[vertex][X], emb[vertex][Y], height+embossing_height]    
                ref = ref + 1
            object_data['points'].append(point)
            
        for vertex in emb:
            vertex.append(height)
        make_3d(emb,height,True)  



#create the icon image to be used by tool 2
def create_icon_drawing(points,asset_name,asset_path):

    # draw the main outline of the shape 
    x = [] 
    y = [] 
    
    for each in points:
        x.append(each[X])
        y.append(each[Y])
 
    x_min = min(x)
    y_min = min(y)
    x_max = max(x)
    y_max = max(y)

    x.append(points[0][X])
    y.append(points[0][Y])
    plt.plot(x,y,'k-')

    # draw all of the embossed lines
    for line in embossed:
        x = [] 
        y = [] 
        for point in line:
            x.append(point[X])
            y.append(point[Y])

        plt.plot(x,y,'k-')

    object_data['x_half'] = (x_max - x_min)/2
    object_data['y_half'] = (y_max-y_min)/2

    middle = plt.Circle(((x_max - x_min)/2,(y_max-y_min)/2),1,color='r')
    
    plt.gcf().gca().add_artist(middle)

    plt.axis('off')
    plt.gca().invert_yaxis()
    name = asset_name + '.png'
    plt.savefig(asset_path + '/' + name, bbox_inches = 'tight')




def dump_data(asset_name,asset_path):
    name = asset_name + '.p'
    pickle.dump(object_data, open(asset_path + '/' + name,'wb'))



def create_asset_dir(asset_name):  
    path = os.getcwd() +'/assets'
    dirs = [name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name))]

    if asset_name in dirs:
        return [False, 'Asset with that name already exists in /assets']
    else:
        path = os.getcwd() +'/assets/' + str(asset_name)
        os.makedirs(path)
        return [True,path]




def create_asset_stl(path_to_save, object_data):
    f = open(path_to_save+'/stl.stl',"w")
    f.write('solid drawing\n')
    for triangle in object_data['points']:
        f.write("facet normal 0.0 0.0 0.0\n")
        f.write("outer loop\n")
        f.write("vertex " + str(triangle['vertex1'][0]) + " " + str(triangle['vertex1'][1]) + " " + str(triangle['vertex1'][2]) +"\n")
        f.write("vertex " + str(triangle['vertex2'][0]) + " " + str(triangle['vertex2'][1]) + " " + str(triangle['vertex2'][2]) +"\n")
        f.write("vertex " + str(triangle['vertex3'][0]) + " " + str(triangle['vertex3'][1]) + " " + str(triangle['vertex3'][2]) +"\n")
        f.write("endloop\n")
        f.write("endfacet\n")   
    f.write('endsolid drawing')
    f.close()



    


# main function to be called, pass a image path and a height for the main object
def trace_and_create_assett(image_path,asset_name,height):

    #create file structure
    returned = create_asset_dir(asset_name)
    if (not returned[0]):
        return returned
    path = returned[1]

    # generate the data for the main object and any embossing
    generate_object(image_path,height)
    generate_embossing(height)
    noramlise_points(points)

    #create the icon for the object
    create_asset_stl(path,object_data)
    create_icon_drawing(points,asset_name,returned[1])

    #dump the data into a .p file to use by tool 2
    dump_data(asset_name,returned[1])

    return [True]





# called by the create gui code to run the asset generation 
# assett height in mm 
def run(image_path,asset_name,small,assett_height):
    global scale, Small

    if small:
        Small = True
        scale = 50
        object_data['size'] = "small"
    else:
        
        Small = False
        scale = 80
        object_data['size'] = "large"

    result =  trace_and_create_assett(image_path, asset_name, assett_height/10)

    if (not result[0]):
        return result
    else:
        return [True]