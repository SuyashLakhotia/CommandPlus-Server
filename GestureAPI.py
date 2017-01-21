#!/usr/bin/python

import math
import numpy as np

class Gesture(object):
    def __init__(self,name):
        self.name=name
    def getName(self):
        return self.name
    def set_palm(self,hand_center,hand_radius):
        self.hand_center=hand_center
        self.hand_radius=hand_radius
    def set_finger_pos(self,finger_pos):
        self.finger_pos=finger_pos
        self.finger_count=len(finger_pos)
    def calc_angles(self):
        self.angle=np.zeros(self.finger_count,dtype=int)
        for i in range(self.finger_count):
            y = self.finger_pos[i][1]
            x = self.finger_pos[i][0]
            self.angle[i]=abs(math.atan2((self.hand_center[1]-y),(x-self.hand_center[0]))*180/math.pi)

def DefineGestures():
    dict={}
    # 1. BEGIN ------------------------------------#
    V=Gesture("V")
    V.set_palm((475,225),45)
    V.set_finger_pos([(490,90),(415,105)])
    V.calc_angles()
    dict[V.getName()]=V
    Loser=Gesture("Loser")
    Loser.set_palm((475,225),50)
    Loser.set_finger_pos([(450,62),(345,200)])
    Loser.calc_angles()
    dict[Loser.getName()]=Loser
    Fist_Close=Gesture("Fist_Close")
    Fist_Close.set_palm((480,230),50)
    Fist_Close.set_finger_pos([])
    Fist_Close.calc_angles()
    dict[Fist_Close.getName()]=Fist_Close
    Thumb=Gesture("Thumb")
    Thumb.set_palm((475,225),50)
    Thumb.set_finger_pos([(345,200)])
    Thumb.calc_angles()
    dict[Thumb.getName()]=Thumb
    Middle_Finger=Gesture("Middle_Finger")
    Middle_Finger.set_palm((475,225),50)
    Middle_Finger.set_finger_pos([(475,80)])
    Middle_Finger.calc_angles()
    dict[Middle_Finger.getName()]=Middle_Finger
    Open_Fist=Gesture("Open_Fist")
    Open_Fist.set_palm((475,225),50)
    Open_Fist.set_finger_pos([(475,80),(475,80), (475,80), (475,80), (475,80)])
    Open_Fist.calc_angles()
    dict[Open_Fist.getName()]=Open_Fist
    
    return dict

def CompareGestures(src1,src2):
    if(src1.finger_count==src2.finger_count):
        if(src1.finger_count==1):
            angle_diff=src1.angle[0]-src2.angle[0]
            if(angle_diff>20):
                result=0
            else:
                len1 = np.sqrt((src1.finger_pos[0][0]- src1.hand_center[0])**2 + (src1.finger_pos[0][1] - src1.hand_center[1])**2)
                len2 = np.sqrt((src2.finger_pos[0][0]- src2.hand_center[0])**2 + (src2.finger_pos[0][1] - src2.hand_center[1])**2)
                length_diff=len1/len2
                radius_diff=src1.hand_radius/src2.hand_radius
                length_score=abs(length_diff-radius_diff)
                if(length_score<0.09):
                    result=src2.getName()
                else:
                    result=0

        elif(src1.finger_count==0):
            result=src2.getName()

        elif(src1.finger_count==5):
            result=src2.getName()

        else:
            angle_diff=[]
            for i in range(src1.finger_count):
                angle_diff.append(src1.angle[i]-src2.angle[i])
            angle_score=max(angle_diff)-min(angle_diff)
            if(angle_score<15):
                length_diff=[]
                for i in range(src1.finger_count):
                    len1 = np.sqrt((src1.finger_pos[i][0]- src1.hand_center[0])**2 + (src1.finger_pos[i][1] - src1.hand_center[1])**2)
                    len2 = np.sqrt((src2.finger_pos[i][0]- src2.hand_center[0])**2 + (src2.finger_pos[i][1] - src2.hand_center[1])**2)
                    length_diff.append(len1/len2)
                length_score=max(length_diff)-min(length_diff)
                if(length_score<0.06):
                    result=src2.getName()
                else:
                    result=0
            else:
                result=0
    else:
        result=0
    return result

def DecideGesture(src,GestureDictionary):
    result_list=[]
    for k in GestureDictionary.keys():
        src2='"'+k+'"'
        result=CompareGestures(src,GestureDictionary[k])
        if(result!=0):
            return result
    return "NONE"
