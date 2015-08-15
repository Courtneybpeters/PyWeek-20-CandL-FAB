import math
current_id_value = 0
def get_id():
    global current_id_value
    current_id_value += 1
    return current_id_value
def lerp(pos1, pos2):
    items = []
    #calculate every sub point between pos1 and pos2 (only supports U, D, L, R motion
    # not general interpolation at the moment.)
    #determine if we should interpolate X or Y
    if pos1[0] == pos2[0]:
        for i in range(int(math.fabs(pos2[1]-pos1[1]))):
            if (pos2[1] > pos1[1]): #interpolation in positive direction
                items.append((pos1[0], pos1[1]+i))
            else: #interpolation in the negative direction
                items.append((pos1[0], pos1[1]-i))

    else:
        for i in range(int(math.fabs(pos2[0]-pos1[0]))):
            if (pos2[0] > pos1[0]): #interpolation in positive direction
                items.append((pos1[0]+i, pos1[1]))
            else: #interpolation in the negative direction
                items.append((pos1[0]-i, pos1[1]))
    return items

def aim_at(pos1, pos2):
    deltax = pos1[0] - pos2[0]
    deltay = pos1[1] - pos2[1]
    angle = math.atan2(deltax, deltay)/math.pi*180.0
    return angle

def distance(pos1, pos2):
    return math.hypot(pos2[0] - pos1[0], pos2[1] - pos1[1])
