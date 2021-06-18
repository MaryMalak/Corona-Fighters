import datetime
import numpy as np


def non_max_suppression_fast(boxes, overlapThresh):
    try:
        # Obtain empty list in case of no boxes
        if len(boxes) == 0:
            return []
        # Transform it into float
        if boxes.dtype.kind == "i":
            boxes = boxes.astype("float")

        pick = []
        
        # Boxes points
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]

        area = (x2 - x1 + 1) * (y2 - y1 + 1)
        idxs = np.argsort(y2)
        
        # Iterate over the list
        while len(idxs) > 0:

            last = len(idxs) - 1
            i = idxs[last]
            pick.append(i)
            # Calculate max couple of box start and min couple box end
            xx1 = np.maximum(x1[i], x1[idxs[:last]])
            yy1 = np.maximum(y1[i], y1[idxs[:last]])
            xx2 = np.minimum(x2[i], x2[idxs[:last]])
            yy2 = np.minimum(y2[i], y2[idxs[:last]])
            # Calculate box height and width 
            w = np.maximum(0, xx2 - xx1 + 1)
            h = np.maximum(0, yy2 - yy1 + 1)
            overlap = (w * h) / area[idxs[:last]] - 1200
            idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))

        return boxes[pick].astype("int")
    except Exception as e:
        print("Exception occurred in non_max_suppression : {}".format(e))
