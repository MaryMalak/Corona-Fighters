# obj registration
def add_obj(self, centroid, inputRect):
    # Put the center
    self.objs[self.following_obj_ID] = centroid
    self.bbox[self.following_obj_ID] = inputRect  
    self.gone[self.following_obj_ID] = 0
    # Using identifier of following accessible
    self.following_obj_ID += 1
