def add_obj(self, centroid, inputRect):
    # when registering an object we use the next available object
    # ID to store the centroid
    self.objs[self.following_obj_ID] = centroid
    self.bbox[self.following_obj_ID] = inputRect  # CHANGE
    self.gone[self.following_obj_ID] = 0
    self.following_obj_ID += 1