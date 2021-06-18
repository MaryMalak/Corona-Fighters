# Discard obj identifiers
def remove_obj(self, obj_identifier):
    # Remove from all dictionaries the identifier of obj
    del self.objs[obj_identifier]
    del self.gone[obj_identifier]
    del self.bbox[obj_identifier] 
