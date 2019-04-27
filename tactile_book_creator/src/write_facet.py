


def write_facet(fi,x1,y1,z1,x2,y2,z2,x3,y3,z3):
    f = open(fi,"a")
    f.write("facet normal 0.0 0.0 0.0\n")
    f.write("outer loop\n")
    f.write("vertex " + str(x1) + " " + str(y1) + " " + str(z1) +"\n")
    f.write("vertex " + str(x2) + " " + str(y2) + " " + str(z2) +"\n")
    f.write("vertex " + str(x3) + " " + str(y3) + " " + str(z3) +"\n")
    f.write("endloop\n")
    f.write("endfacet\n") 
    f.close()