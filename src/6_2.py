import csv
import numpy as np



def loadPDGeom3D(filename):
    with open(filename, newline='\n') as f:
        reader = csv.reader(f)
        PDGeo = []
        count = 0;
        try:
            for row in reader:
                row = row[0].split("  ")
                row = row[1:] #eliminates an extra space that the numbers have infront
                parsedRow = []
                for col in range(len(row)):
                    if count == 0:
                        nodeNum = int(row[col])
                    else:
                        parsedRow.append(float(row[col]))  
                    count= count + 1
                PDGeo.append(parsedRow)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
    return nodeNum, np.asarray(PDGeo[1:])



def inputForPDDO():
    dataPath = "../data/"
    with open(dataPath + "PDopr.inp") as fp:
        line = fp.readline() #file name
        PDGeoFileName = fp.readline() #file name
        line = fp.readline() #atype, morder, n1order, n2order, n3order, timeFlag, ftype
        atype = fp.readline().split()
        morder = int(atype[0])
        n1order = int(atype[1])
        n2order = int(atype[2])
        n3order = int(atype[3])
        timeFlag = int(atype[4])
        ftype = int(atype[5])
        line = fp.readline() #family type
        familyType = int(fp.readline())
        line = fp.readline() #delx dely delz
        deltas = fp.readline().split()
        delx = float(deltas[0].replace("d","e"))
        dely = float(deltas[1].replace("d","e"))
        delz = float(deltas[2].replace("d","e"))
        line = fp.readline() #number of diff. operators
        numDiffOps = int(fp.readline())
        line = fp.readline() #n1
        if numDiffOps > 0:
            numberDiffOperators = []
            for i in range(numDiffOps):
                line = fp.readline().split()
                numberDiffOperators.append(list(map(int,line)))
        line = fp.readline() #num of bc
        numBC = int(fp.readline())
        BC = []
        if numBC > 0:
            for i in range(numBC):
                aux = []
                line = fp.readline() #bc1: xmin, xmax, ymin, ymax, num_diff_ops \ n1(1), n2(1), coef(1), ..., val
                line = fp.readline().split()
                for j in range(len(line)):
                    aux.append(float(line[j].replace("d","e")))
                line = fp.readline().split()
                for j in range(len(line)):
                    aux.append(float(line[j].replace("d","e")))
                BC.append(aux) 
        line = fp.readline() #nout
        nout = int(fp.readline())
        nout = 2
        if nout>0:
            line = fp.readline() #n1
            numOut = []
            for i in range(nout):
                line = fp.readline().split()
                numOut.append(list(map(int,line)))



def main():
    
    inputForPDDO()

    a = input('').split(" ")[0]
    #PDGeomPath = '../data/PDgeom3D.dat'
    #[nodeNum, PDGeo] = loadPDGeom3D(PDGeomPath) 
    #print(nodeNum)
    #print(PDGeo[0])
    #np.savetxt("/home/doctajfox/Documents/Thesis_Research/PDDOHeatDiffusionEquationPython/data/PDGeo5.dat",PDGeo,delimiter=",")



if __name__ == "__main__":
    main()




