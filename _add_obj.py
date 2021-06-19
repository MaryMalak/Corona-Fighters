# obj registration
def add_obj(self, centroid, inputRect):
    # Put the center
    # Using the identifier of following accessible obj to register
    self.objs[self.following_obj_ID] = centroid
    self.bbox[self.following_obj_ID] = inputRect  
    self.gone[self.following_obj_ID] = 0
    self.following_obj_ID += 1
