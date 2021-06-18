import numpy as np
from scipy.spatial import distance as dist

def modify(self, drawn_rectangles):
    # check to see if the list of input bounding box rectangles
    # is empty
    if len(drawn_rectangles) == 0:
        # loop over any existing tracked objects and mark them
        # as disappeared
        for obj_identifier in list(self.gone.keys()):
            self.gone[obj_identifier] += 1

            # if we have reached a maximum number of consecutive
            # frames where a given object has been marked as
            # missing, deregister it
            if self.gone[obj_identifier] > self.max_frames:
                self.remove_obj(obj_identifier)

        # return early as there are no centroids or tracking info
        # to update
        # return self.objs
        return self.bbox

    # initialize an array of input centroids for the current frame
    centre_in = np.zeros((len(drawn_rectangles), 2), dtype="int")
    rectangles_in = []
    # loop over the bounding box rectangles
    for (i, (startX, startY, endX, endY)) in enumerate(drawn_rectangles):
        # use the bounding box coordinates to derive the centroid
        cX = int((startX + endX) / 2.0)
        cY = int((startY + endY) / 2.0)
        centre_in[i] = (cX, cY)
        rectangles_in.append(drawn_rectangles[i])  # CHANGE

    # if we are currently not tracking any objects take the input
    # centroids and register each of them
    if len(self.objs) == 0:
        for i in range(0, len(centre_in)):
            self.add_obj(centre_in[i], rectangles_in[i])  # CHANGE

    # otherwise, are are currently tracking objects so we need to
    # try to match the input centroids to existing object
    # centroids
    else:
        # grab the set of object IDs and corresponding centroids
        obj_identifiers = list(self.objs.keys())
        objectCentroids = list(self.objs.values())

        # compute the distance between each pair of object
        # centroids and input centroids, respectively -- our
        # goal will be to match an input centroid to an existing
        # object centroid
        D = dist.cdist(np.array(objectCentroids), centre_in)

        # in order to perform this matching we must (1) find the
        # smallest value in each row and then (2) sort the row
        # indexes based on their minimum values so that the row
        # with the smallest value as at the *front* of the index
        # list
        rows = D.min(axis=1).argsort()

        # next, we perform a similar process on the columns by
        # finding the smallest value in each column and then
        # sorting using the previously computed row index list
        cols = D.argmin(axis=1)[rows]

        # in order to determine if we need to update, register,
        # or deregister an object we need to keep track of which
        # of the rows and column indexes we have already examined
        rows_required = set()
        columns_required = set()

        # loop over the combination of the (row, column) index
        # tuples
        for (row, col) in zip(rows, cols):
            # if we have already examined either the row or
            # column value before, ignore it
            if row in rows_required or col in columns_required:
                continue

            # if the distance between centroids is greater than
            # the maximum distance, do not associate the two
            # centroids to the same object
            if D[row, col] > self.limited_length:
                continue

            # otherwise, grab the object ID for the current row,
            # set its new centroid, and reset the disappeared
            # counter
            obj_identifier = obj_identifiers[row]
            self.objs[obj_identifier] = centre_in[col]
            self.bbox[obj_identifier] = rectangles_in[col]  # CHANGE
            self.gone[obj_identifier] = 0

            # indicate that we have examined each of the row and
            # column indexes, respectively
            rows_required.add(row)
            columns_required.add(col)

        # compute both the row and column index we have NOT yet
        # examined
        rows_unrequired = set(range(0, D.shape[0])).difference(rows_required)
        columns_unrequired = set(range(0, D.shape[1])).difference(columns_required)

        # in the event that the number of object centroids is
        # equal or greater than the number of input centroids
        # we need to check and see if some of these objects have
        # potentially disappeared
        if D.shape[0] >= D.shape[1]:
            # loop over the unused row indexes
            for row in rows_unrequired:
                # grab the object ID for the corresponding row
                # index and increment the disappeared counter
                obj_identifier = obj_identifiers[row]
                self.gone[obj_identifier] += 1

                # check to see if the number of consecutive
                # frames the object has been marked "disappeared"
                # for warrants deregistering the object
                if self.gone[obj_identifier] > self.max_frames:
                    self.remove_obj(obj_identifier)

        # otherwise, if the number of input centroids is greater
        # than the number of existing object centroids we need to
        # register each new input centroid as a trackable object
        else:
            for col in columns_unrequired:
                self.add_obj(centre_in[col], rectangles_in[col])

    # return the set of trackable objects
    # return self.objects
    return self.bbox