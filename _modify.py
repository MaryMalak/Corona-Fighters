import numpy as np
from scipy.spatial import distance as dist

def modify(self, drawn_rectangles):
    # is rectangles list empty?
    if len(drawn_rectangles) == 0:
        # mark items as gone
        for obj_identifier in list(self.gone.keys()):
            self.gone[obj_identifier] += 1
            if self.gone[obj_identifier] > self.max_frames:
                self.remove_obj(obj_identifier)
        # nothing to update
        return self.bbox

    # initialize an array for the current frame
    centre_in = np.zeros((len(drawn_rectangles), 2), dtype="int")
    rectangles_in = []
    for (i, (startX, startY, endX, endY)) in enumerate(drawn_rectangles):
        # use the bounding box coordinates to derive the centroid
        cX = int((startX + endX) / 2.0)
        cY = int((startY + endY) / 2.0)
        centre_in[i] = (cX, cY)
        rectangles_in.append(drawn_rectangles[i])  # CHANGE

    # not tracking any objects add new centers
    if len(self.objs) == 0:
        for i in range(0, len(centre_in)):
            self.add_obj(centre_in[i], rectangles_in[i])  # CHANGE

    # Matching the input to existing object
    else:
        # get the set of object IDs and their centers
        obj_identifiers = list(self.objs.keys())
        objectCentroids = list(self.objs.values())

        # compute the distance between each pair of objects
        # find the smallest value in each row 
        # sort the row indexes ascendingly
        # sort columns according to rows
        D = dist.cdist(np.array(objectCentroids), centre_in)
        rows = D.min(axis=1).argsort()
        cols = D.argmin(axis=1)[rows]

        rows_required = set()
        columns_required = set()

        for (row, col) in zip(rows, cols):
            # ignore what was examined before
            if row in rows_required or col in columns_required:
                continue

            if D[row, col] > self.limited_length:
                # if the distance is > max distance, they are not close
                continue
                #if close to each other
            obj_identifier = obj_identifiers[row]
            self.objs[obj_identifier] = centre_in[col]
            self.bbox[obj_identifier] = rectangles_in[col]  # CHANGE
            self.gone[obj_identifier] = 0
            # add already examined objects
            rows_required.add(row)
            columns_required.add(col)

        # compute what we haven't examined
        rows_unrequired = set(range(0, D.shape[0])).difference(rows_required)
        columns_unrequired = set(range(0, D.shape[1])).difference(columns_required)
        
        # checking potentially gone objects
        if D.shape[0] >= D.shape[1]:
            for row in rows_unrequired:
                obj_identifier = obj_identifiers[row]
                self.gone[obj_identifier] += 1
                # frames the object has been marked "gone" is removed
                if self.gone[obj_identifier] > self.max_frames:
                    self.remove_obj(obj_identifier)

        # else the number of input > number of existing object, add them 
        else:
            for col in columns_unrequired:
                self.add_obj(centre_in[col], rectangles_in[col])

    # return the objects
    return self.bbox
