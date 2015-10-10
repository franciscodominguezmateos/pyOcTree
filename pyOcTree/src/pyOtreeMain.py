'''
Created on 12/07/2015

@author: Francisco Dominguez
'''
from pyOTree import *

if __name__ == '__main__':
    np=1<<pyOTree.MAX_LEVEL
    ot=pyOTree();    
    ot.insert(Point3D(10,10,10))
    ot.insert(Point3D( 0,10, 0))
    print ot
    print ot.containPoint(Point3D(10,10,10))
    print ot.containPoint(Point3D(10,10,9))
    cs0=ot.getCubes(Cube(0,0,0,np<<0,np<<0,np<<0),0)
    for c in cs0:
        print c
    print cs0
