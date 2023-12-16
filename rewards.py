from Car import Car
import math

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
    if(dis < rad * 0.9 and (i + 1 < len(points))):
        return i + 1
    return i

def rewardCalc(points, pos, i, trackLength, ):
    maxDist = distance((0,0), (800, 500))
    reward = (calcTrackLength(points, i) - distance(pos, points[i]))/ trackLength
    return  0 if reward < 0 else reward
    #return (calcTrackLength(points, i) / trackLength) + (1 - (distance(pos, points[i]) / trackLength)) 

def calcTrackLength(points, end):
    #Gives the total distance of the track 
    #depending on the start and end square
    #location
    totDist = 0
    for i in range(end):
        if(i + 2 == len(points)): #used to work porperly for track full length
            return totDist
        totDist += distance(points[i], points[i + 1])
    return totDist

def angles(points):
    angles = []
    for p in range(len(points) - 1):
        dy = points[p + 1][1] - points[p][1] 
        dx = points[p + 1][0] - points[p][0] + 0.000000001
        angle = math.degrees(math.atan(dy / dx))
        angles.append(int(angle))

    return angles

