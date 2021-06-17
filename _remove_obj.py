
def remove_obj(self, obj_identifier):
    # to deregister an object ID we delete the object ID from
    # both of our respective dictionaries
    del self.objs[obj_identifier]
    del self.gone[obj_identifier]
    del self.bbox[obj_identifier]  # CHANGE