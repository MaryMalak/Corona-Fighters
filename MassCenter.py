# import the necessary packages
from collections import OrderedDict
import numpy as np

import _add_obj
import _remove_obj
import _modify

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
        return _add_obj.add_obj(self, centroid, inputRect)

    def remove_obj(self, obj_identifier):
        return _remove_obj.remove_obj(self, obj_identifier)

    def modify(self, drawn_rectangles):
        return _modify.modify(self, drawn_rectangles)