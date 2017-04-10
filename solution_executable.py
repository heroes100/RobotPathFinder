import sys
import math
import copy

minPathTime = 999999999

#Constants
robotSpeed = 0.2
waypointDelay = 10
endPosition = (100, 100, 0)
delayMatrix = []
penaltyMatrix = []

#Robot class used for spawning test robots to traverse a path
class Robot:
    Loc = [0,0]
    WPIndex = -1
    timer = 0.0
    availWP = []
    waypoints = []

    def __init__(self, waypoints):
        self.availWP = waypoints[:]
        self.waypoints = waypoints[:]

    #Finds the hypotnuse of newX and newY
    def CalculateTime(self, newX, newY):
        global robotSpeed
        return math.sqrt(((newX**2 + newY**2))) * float(robotSpeed)

    #This function takes in a waypoint index for the
    # robot to traverse to and returns the total time required
    # for the robot to get there (plus penalty)
    def GetWaypointTravelTime(self, waypointIndex):
        #Find the time required to travel to new X,Y location
        return self.CalculateTime(self.Loc[0] - self.availWP[waypointIndex][0], self.Loc[1] - self.availWP[waypointIndex][1])


    def GetWaypointPenaltyTime(self, waypointIndex):
        penaltyTime = 0
        #Calculate the possible penalties
        for penaltyIndex in range(self.WPIndex+1, waypointIndex):
            penaltyTime += self.availWP[penaltyIndex][2]
        return penaltyTime

    def GetWaypointTotalTime(self, waypointIndex):
        return (self.GetWaypointTravelTime(waypointIndex)
                    + self.GetWaypointPenaltyTime(waypointIndex) )

    #Move the robot to the indexed waypoint location and update stats
    def TravelToWaypointIndex(self, index):
        global waypointDelay
        self.timer += self.GetWaypointTotalTime(index) + waypointDelay
        self.Loc = [self.availWP[index][0], self.availWP[index][1]]
        self.WPIndex = index
        self.availWP = self.availWP[index+1:]


    def TravelToEndPoint(self):
        global endPosition
        #Add end point to array
        self.availWP.append(((endPosition[0], endPosition[1],0)))
        #Travel to end point
        self.timer += self.GetWaypointTotalTime(len(self.availWP)-1)
        self.Loc = [endPosition[0], endPosition[1]]
        self.WPIndex = -2
        self.availWP = []

    def AppendEndPoint(self):
        global endPosition
        self.availWP.append((endPosition[0], endPosition[1],0))
        self.waypoints.append((endPosition[0], endPosition[1],0))

        
#This function parses the text file and declares the set of waypoints
# into a list. It also defines an empty list for delayMatrix and penaltyMatrix
def ParseMap(filePtr):
    global delayMatrix, penaltyMatrix
    waypoints = []
    numCheckpoints = filePtr.readline();
    for i in range(int(numCheckpoints)):
        (x, y, p) = filePtr.readline().split(" ")
        waypoints.append( (int(x), int(y), int(p)) )
    delayMatrix = [[-1 for x in range(len(waypoints)+1)] for x in range(len(waypoints)+1)]
    penaltyMatrix = [-1 for x in range(len(waypoints)+1)]
    return waypoints


#This function will fill a list with the delays for moving between waypoints
def FillDelayMatrix():
    global delayMatrix, penaltyMatrix, endPosition
    robot1 = Robot(waypoints)
    robot1.AppendEndPoint()
    for i in range(len(robot1.waypoints)):
        for j in range(i, len(robot1.waypoints)):
            delayMatrix[i][j] = robot1.GetWaypointTravelTime(j-i) + waypointDelay
            if(j+1 == len(robot1.waypoints)):
                delayMatrix[i][j] -= waypointDelay
        penaltyMatrix[i] = robot1.availWP[0][2]
        robot1.TravelToWaypointIndex(0)
    #Implement penalty into delay matrix
    for i in range(len(robot1.waypoints)):
        for j in range(i, len(robot1.waypoints)):
            delayMatrix[i][j] += sum(penaltyMatrix[i:j])
        

def PrintMatrix(matrix):
    for i in range(len(matrix)):
        print matrix[i]


def depthFirst(timer = 0, depth = 0):
    global delayMatrix, minPathTime, times, waypointDelay
    for col in range(depth, len(delayMatrix)):
        if(timer + delayMatrix[depth][col] < minPathTime):
            t, endOfPath = depthFirst(timer + delayMatrix[depth][col], depth+1)
            if(t < minPathTime and endOfPath):
                minPathTime = t
                
    if(depth == len(delayMatrix)):
        return timer, True
    else:
        return timer, False


def PrintWaypoints():
    if(len(waypoints) < 1):
        return
    print "Index\tX\tY\tPenalty"
    for index, waypoint in enumerate(waypoints):
        print "{}\t{}\t{}\t{}".format(index+1,waypoint[0],waypoint[1],waypoint[2])
        

if __name__ == "__main__":
    #Check for file argument
    if(len(sys.argv) < 2):
        print "Please specify input file."
        exit();
    filePtr = open(sys.argv[1])
    waypoints = ParseMap(filePtr)
    while(waypoints != []):
        waypoints = ParseMap(filePtr)
        FillDelayMatrix()
        depthFirst()
        print round(minPathTime, 3)
        minPathTime = 999999

