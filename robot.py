import sys

#Constants
robotSpeed = 0.2
waypointDelay = 10
endPosition = [100, 100]
delayMatrix = []

#Robot class used for spawning test robots to follow a path
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
        return (((newX**2 + newY**2))**(1/float(2))) * robotSpeed

    #This function takes in a waypoint index for the
    # robot to traverse to and returns the total time required
    # for the robot to get there (plus penalty)
    def GetWaypointTravelTime(self, waypointIndex):
        penaltyTime = 0
        #Find the time required to travel to new X,Y location
        timeReq = self.CalculateTime(self.waypoints[waypointIndex][0] - self.Loc[0], self.waypoints[waypointIndex][1] - self.Loc[1])
        #Calculate the possible penalties
        for penaltyIndex in range(self.WPIndex+1, waypointIndex):
            penaltyTime += self.waypoints[penaltyIndex][2]
            
        return (timeReq + penaltyTime)



    #Move the robot to the indexed waypoint location and update stats
    def TravelToWaypointIndex(self, index):
        global waypointDelay
        self.timer += self.GetWaypointTravelTime(index) + waypointDelay
        self.Loc = [self.waypoints[index][0], self.waypoints[index][1]]
        self.WPIndex = index
        self.availWP = self.availWP[index+1:]

    def TravelToEndPoint(self):
        global endPosition
        #Add end point to array
        self.availWP.append([(endPosition[0], endPosition[1],0)])
        #Travel to end point
        self.timer += self.GetWaypointTravelTime(len(self.availWP)-1)
        self.Loc = [endPosition[0], endPosition[1]]
        self.WPIndex = -2
        self.availWP = []

        

def ParseMap(filePtr):
    global delayMatrix
    waypoints = []
    numCheckpoints = filePtr.readline();
    for i in range(int(numCheckpoints)):
        (x, y, p) = filePtr.readline().split(" ")
        waypoints.append( (int(x), int(y), int(p)) )
    delayMatrix = [[-1 for x in range(len(waypoints))] for x in range(len(waypoints))]
    return waypoints

#if __name__ == "__main__":
    #Check for file argument
#    if(len(sys.argv) < 2):
#        print "Please specify input file."
#        exit();
#    filePtr = open(sys.argv[1])
#    waypoints = ParseMap(filePtr)


def FillDelayArray():
    global delayMatrix
    robot1 = Robot(waypoints)
    for i in range(len(waypoints)):
        for j in range(len(waypoints)):
            delayMatrix[i][j] = robot1.GetWaypointTravelTime(j)
        robot1.TravelToWaypointIndex(0)


# Create X number of threads for calculating paths
# Each thread will calculate a minimum time
# If a path exceeds the current minimum path time, STOP following it

#recursively:
#       Check for available paths at current waypoint
#       If taking the [index] available is less than minimum path time, take it
#   If we make it to the finish
#       return path edge(s) taken
#   else
#       Return as invalid path
def GeneratePaths(robot):
    #For every available waypoint remainin
    #for path in range(len(robot.availWP)):
     
    return


def DijkstraPath():
    global waypoints
    robot1 = Robot(waypoints)
    for i in range(len(waypoints)):
        robot1.TravelToWaypointIndex(i)
    robot1.TravelToEndPoint()
    print robot1.timer
    


def PrintWaypoints():
    if(len(waypoints) < 1):
        return
    print "Index\tX\tY\tPenalty"
    for index, waypoint in enumerate(waypoints):
        print "{}\t{}\t{}\t{}".format(index+1,waypoint[0],waypoint[1],waypoint[2])
        

#####Debuging 
filePtr = open('sample_input_medium.txt', 'r')
waypoints = ParseMap(filePtr)
availWP = waypoints[:]
