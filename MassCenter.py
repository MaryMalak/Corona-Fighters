# importing the required packages
from collections import OrderedDict
import numpy as np

import _add_obj
import _remove_obj
import _modify

class Mass_Centre:
    def __init__(self, max_frames=10, limited_length=50):
        
        self.following_obj_ID = 0          # initialize the unique ID of the next object with zero 
        self.objs = OrderedDict()          # initialize the dictionaries that keeps track of mapping the object ID to its centroid 
        self.gone = OrderedDict()          #initialize the dictionaries that keeps track of mapping the object ID to the number of 
                                           #consecutive frames it has been marked as "disappeared"
        self.bbox = OrderedDict()  

        self.max_frames = max_frames      #maximum number of consecutive "disappeared" frames given to object untill it is deregistered from tracking

        self.limited_length = limited_length #specify max acceptable distance between two centroids of an object above which object will be marked as disappeared
                                             #and will be removed consequently

    def add_obj(self, centroid, inputRect):     #adding an object to be tracked and drawing corresponding tracking rectangle
        return _add_obj.add_obj(self, centroid, inputRect)

    def remove_obj(self, obj_identifier):        #detracking the object through its ID 
        return _remove_obj.remove_obj(self, obj_identifier)

    def modify(self, drawn_rectangles):         #modifying the rectangle drawn around each tracked object
        return _modify.modify(self, drawn_rectangles)
