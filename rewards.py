from Car import Car
import math

distance = Car.distance

class RewardSys():
    def __init__(self, points):
        self.points = points
        self.trackLength = None

    #Run this function first to set up self.points
    def rewardPoints(self, rad = 30):
        i, j = 0, 0
        while(i < len(self.points) - 1):
            j = i + 1
            while(j < len(self.points)):
                if(distance(self.points[i], self.points[j]) <= rad):
                    self.points.remove(self.points[j])
                    j -= 1
                j += 1
            i += 1   

        # return points
    
    #calculates the length between the start(element index in points)
    # to the end
    def calcTrackLength(self, start = 0, end = None):
        totDist = 0
        if end == None:
            end = len(self.points) - 1
        for i in range(start, end):
            totDist += distance(self.points[i], self.points[i + 1])
        return totDist

    #If it is close enough based on the first condition it
    #will go to the next reward Location
    def rewardLocation(self, position, i, rad = 30):
        dist = distance(self.points[i], position)
        if(dist < rad and (i + 1 < len(self.points))):
            return i + 1
        return i

    #Returns the precentage of the track completed [0,1]
    def rewardCalc(self, position, start, current_point):
       
        reward = (self.calcTrackLength(start, end = current_point) - distance(position, self.points[current_point])) / self.trackLength
        return reward #0 if reward < 0 else reward

        
    
    #returns a list of angles based on 
    #the current point and the next point
    def angles(points):
        angles = []
        for p in range(len(points) - 1):
            dy = points[p + 1][1] - points[p][1] 
            dx = points[p + 1][0] - points[p][0] + 0.000000001 # so no /0 error
            angle = math.degrees(math.atan(dy / dx))
            if(points[p] > points[p + 1]):
                angles.append(int(angle) + 180)
            else:
                angles.append(int(angle))

        return angles

