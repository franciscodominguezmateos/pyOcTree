#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 12/07/2015

@author: Francisco Dominguez
'''
class Point3D:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
    def __str__(self):
        return "(%d,%d,%d)"%(self.x,self.y,self.z)
class Cube:
    def __init__(self,x,y,z,w,h,d):
        self.x=x
        self.y=y
        self.z=z
        self.w=w
        self.h=h
        self.d=d
        self.node=None
    def asTuple(self):
        return (self.x,self.y,self.z,self.x+self.w-1,self.y+self.h-1,self.z+self.d-1)
    def getCenter(self):
        return Point3D(self.x+self.w/2,self.y+self.h/2,self.z+self.d/2)
    def __str__(self):
        return "(%d,%d,%d|%d,%d,%d)"%(self.x,self.y,self.z,self.w,self.h,self.d)

class pyOTree(object):
    '''
    Easy Octree implementation
    '''
    MAX_LEVEL=9
    def __init__(self,level=MAX_LEVEL):
        self.full=False
        self.level=level
        self.nodes=[None,None,None,None,None,None,None,None]
        self.father=None
    def allNodesFull(self):
        for n in self.nodes:
            if n==None:
                return False
            elif not n.full:
                return False
        return True
    def cleanNodes(self):
        self.nodes=[None,None,None,None,None,None,None,None]
    def splitCube(self,c,i):
        wMid=c.w>>1
        hMid=c.h>>1
        dMid=c.d>>1
        xMid=c.x+wMid
        yMid=c.y+hMid
        zMid=c.z+dMid
        if i==0:
            return Cube(c.x ,c.y, c.z ,wMid,hMid,dMid)
        if i==1:
            return Cube(xMid,c.y, c.z ,wMid,hMid,dMid)
        if i==2:
            return Cube(c.x ,yMid,c.z ,wMid,hMid,dMid)
        if i==3:
            return Cube(xMid,yMid,c.z ,wMid,hMid,dMid)
        if i==4:
            return Cube(c.x ,c.y ,zMid,wMid,hMid,dMid)
        if i==5:
            return Cube(xMid,c.y ,zMid,wMid,hMid,dMid)
        if i==6:
            return Cube(c.x ,yMid,zMid,wMid,hMid,dMid)
        if i==7:
            return Cube(xMid,yMid,zMid,wMid,hMid,dMid)
            
    def getCubes(self,c,maxLevel=0):
        if self.full or self.level==maxLevel:
            c.node=self
            return [c]
        else:
            cubs=[]
            for i,n in enumerate(self.nodes):
                if n!=None:
                    ci=self.splitCube(c, i)
                    cubs.extend(n.getCubes(ci,maxLevel))
            return cubs
    def containCube(self,c):
        pass
    def containPoint(self,p):
        if self.full:
            return True
        if self.level==0:
            return True
        nPos=self.getPosNodeAtThisLevel(p)
        if self.nodes[nPos]==None:
            return False
        return self.nodes[nPos].containPoint(p)
    def getPosNodeAtThisLevel(self,p):
        lsb=p.x>>self.level-1 & 1
        msb=p.y>>self.level-1 & 1
        hsb=p.z>>self.level-1 & 1
        return (hsb<<2)+(msb<<1)+lsb
    def insert(self,p):
        if self.full:
            return
        if self.level==0:
            #TODO: Reached a leaf we should insert data p in this node
            self.full=True
        else:
            nPos=self.getPosNodeAtThisLevel(p)
            if self.nodes[nPos]==None:
                self.nodes[nPos]=pyOTree(self.level-1)
            self.nodes[nPos].insert(p)
            if self.allNodesFull():
                self.full=True
                #TODO: Before cleaning we should summary the data
                self.cleanNodes()
    def __str__(self):
        sv="level= %d full=%d"%(self.level,self.full)
        if not self.full:
            for i,n in enumerate(self.nodes):
                sv+=" %d-%d"%(i,self.level)
                if n!=None:
                    sv+="["+n.__str__()+"]"
                else:
                    sv+="[]"
        return sv
       