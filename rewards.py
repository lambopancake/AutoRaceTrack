from Car import Car

distance = Car.distance
def rewardPoints(points, rad = 30):
    #distance = Car.distance
    i, j = 0, 0
    
    while(i < len(points) - 1):
        j = i + 1
        while(j < len(points)):
            if(distance(points[i], points[j]) <= rad):
                points.remove(points[j])
                j -= 1
            j += 1
        i += 1   

    return points

def rewardLocation(points, pos, i, rad = 30):
    dis = distance(points[i], pos)
    #print(dis,  end = "  ")
    if(dis < rad * 0.9 and (i + 1 < len(points))):
        return i + 1
    return i

def rewardCalc(points, pos, i):
    dis = distance(points[i], pos)
    point = (1 - (dis / distance((0,0), (800,500)))) * 1
    return point

def calcTrackLength(points, end):
    #Gives the total distance of the track 
    #depending on the start and end square
    #location
    totDist = 0
    for i in range(end):
        if(i + 2 > len(points)):
            return totDist
        totDist += distance(points[i], points[i + 1])
    return totDist

    