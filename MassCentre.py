# import the necessary packages
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np


class Mass_Centre:
    def __init__(self, max_frames=10, limited_length=50):
        # initialize the next unique object ID along with two ordered
        # dictionaries used to keep track of mapping a given object
        # ID to its centroid and number of consecutive frames it has
        # been marked as "disappeared", respectively
        self.following_obj_ID = 0
        self.objs = OrderedDict()
        self.gone = OrderedDict()
        self.bbox = OrderedDict()  # CHANGE

        # store the number of maximum consecutive frames a given
        # object is allowed to be marked as "disappeared" until we
        # need to deregister the object from tracking
        self.max_frames = max_frames

        # store the maximum distance between centroids to associate
        # an object -- if the distance is larger than this maximum
        # distance we'll start to mark the object as "disappeared"
        self.limited_length = limited_length

    def add_obj(self, centroid, inputRect):
        # when registering an object we use the next available object
        # ID to store the centroid
        self.objs[self.following_obj_ID] = centroid
        self.bbox[self.following_obj_ID] = inputRect  # CHANGE
        self.gone[self.following_obj_ID] = 0
        self.following_obj_ID += 1

    def remove_obj(self, obj_identifier):
        # to deregister an object ID we delete the object ID from
        # both of our respective dictionaries
        del self.objs[obj_identifier]
        del self.gone[obj_identifier]
        del self.bbox[obj_identifier]  # CHANGE
