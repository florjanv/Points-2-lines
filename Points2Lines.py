import arcpy
import math

#parameters
f = r"C:\Users\user\Desktop\test\points\temp.gdb\Points" #input points feature class
lines_f = r"C:\Users\user\Desktop\test\points\temp.gdb\Lines" #empty line feature class
tolerance = 4 #the tolerance in meters

#variables
feature_id = []
total_x = []
total_y=[]
lines = []

def main():
    desc = arcpy.Describe(f)
    noZvalue()
    #add joined fields
    try:
        arcpy.AddField_management(lines_f,"from_id","LONG")
        arcpy.AddField_management(lines_f,"from_xy","TEXT",250)
        arcpy.AddField_management(lines_f,"to_id","LONG")
        arcpy.AddField_management(lines_f,"to_xy","TEXT",250)
        arcpy.AddField_management(lines_f,"length","DOUBLE")
        arcpy.AddField_management(lines_f,"dub","TEXT",50)
    except:
        print("fields exists")


    with arcpy.da.InsertCursor(lines_f,["SHAPE@","from_id","from_xy","to_id","to_xy"]) as cursor:
        for i in feature_id:
            if lines[i]:
                for j in lines[i]:
                    array = arcpy.Array([arcpy.Point(total_x[i], total_y[i]), arcpy.Point(total_x[j], total_y[j])])
                    cursor.insertRow([arcpy.Polyline(array),i+1,str(total_x[i])+", "+str(total_y[i]),j+1,str(total_x[j])+", "+str(total_y[j])])

    #remove dublicated lines
    arcpy.CalculateField_management(lines_f,"length","!SHAPE_Length!","PYTHON_9.3")
    arcpy.CalculateField_management(lines_f,"dub",'str(!length!) +", " +str(abs( !from_id! - !to_id! ))',"PYTHON_9.3")
    arcpy.DeleteIdentical_management(lines_f, "dub")

        
 
def noZvalue(): #function for calculating the distances with Z coordinate
    oid = 0
    for a in arcpy.da.SearchCursor(f,["SHAPE@X","SHAPE@Y"]):
        total_x.append(round(a[0],4))
        total_y.append(round(a[1],4))
        feature_id.append(oid)
        oid+=1
    #fill the variable with id's that are nearer than 4m
    for i in feature_id:
        v1=[]
        for j in feature_id:
            dist=0
            dist = math.sqrt(math.pow(total_x[j]-total_x[i],2)+math.pow(total_y[j]-total_y[i],2))
            if dist<=tolerance:
                if dist ==0: continue
                v1.append(feature_id[j])
        lines.append(v1)



if __name__ == "__main__":
    main()
