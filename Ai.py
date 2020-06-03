import xlrd as x
import math

Days = ["sat","sun","mon","tue","wed","thu","fri"]

class Node:
    flightName = ""
    cityName = ""
    departureTime = 0
    arrivalTime = 0
    day=""
    depTime = ""
    arrTime = ""
    parent = None
    h = 0
    g = 0
    
class Flight:
    sourceCity=""
    destinationCity=""
    depTime = ""
    arrTime = ""
    departureTime = 0
    arrivalTime = 0
    flightNumber=""
    days=[]
    def setSourceCity(self,source):
        self.sourceCity=source
        
    def setDestinationCity(self,destination):
        self.destinationCity=destination
        
    def setdepartureTime(self,departureTime):
        self.departureTime=departureTime
        
    def setarrivalTime(self,arrivalTime):
        self.arrivalTime=arrivalTime
        
    def setflightNumber(self,flightNumber):
        self.flightNumber=flightNumber
     
    def setDays(self,days):
        self.days=days    
        
def saveFlight(l):
  loc = ("Flights.xlsx") 
  wb = x.open_workbook(loc) 
  sheet = wb.sheet_by_index(0) 
  for i in range((sheet.nrows)-1): 
    f = Flight()
    for j in range(sheet.ncols):
            if(j==0):f.setSourceCity(sheet.cell_value(i+1,j))
            elif( j==1):f.setDestinationCity(sheet.cell_value(i+1,j))
            elif( j==2):
                f.depTime = sheet.cell_value(i+1,j)
                depTime = sheet.cell_value(i+1,j).split(":")
                hours = int(depTime[0])*60
                hours += int(depTime[1])
                f.setdepartureTime(hours)   
            elif( j==3):
                f.arrTime = sheet.cell_value(i+1,j)
                depTime = sheet.cell_value(i+1,j).split(":")
                hours = int(depTime[0])*60
                hours += int(depTime[1])
                f.setarrivalTime(hours)
            elif( j==4):f.setflightNumber(sheet.cell_value(i+1,j))
            elif( j==5):
                cell = sheet.cell_value(i+1,j)
                dd=[]
                dd = cell.split("[")
                dd = dd[1].split("]")
                f.days = dd[0].split(",")
                for k in range(len(f.days)):
                    f.days[k] = f.days[k].replace(" ","")
                
    list.append(f)  
     
def saveCities(dic):
    loc = ("Cities.xlsx") 
    wb = x.open_workbook(loc) 
    sheet = wb.sheet_by_index(0)
    for i in range((sheet.nrows)-1):
        lat_lon = []
        lat_lon.append(sheet.cell_value(i+1,1))
        lat_lon.append(sheet.cell_value(i+1,2))
        dic[sheet.cell_value(i+1,0)] = lat_lon
    
def getDistanceTime(away , goal , dic):
    R = 6373.0
    away_city = dic.get(away)
    goal_city = dic.get(goal)
    lat1 = away_city[0]
    lon1 = away_city[1]
    lat2 = goal_city[0]
    lon2 = goal_city[1]
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    time  = round((distance/700)*60)
    return time
 
def getChild(source, dayList , goal):
    child = []
    for obj in list:
        if(obj.sourceCity==source.cityName):
            if(source.day==""):
                firstDayIndex =  Days.index(dayList[0])
            else:
                firstDayIndex =Days.index(source.day)
            secondDayIndex = Days.index(dayList[1])
            for i in obj.days:
                checkIndex = Days.index(i)
                if(checkIndex >= firstDayIndex and checkIndex <= secondDayIndex):
                    if(source.day==""):
                        firstDayIndex  = checkIndex                                
                    if(obj.departureTime+((checkIndex-firstDayIndex)*60*24) > source.arrivalTime):
                        node = Node()
                        waitingTime = obj.departureTime - source.arrivalTime
                        if(obj.arrivalTime >= obj.departureTime):
                            if(waitingTime < 0):
                                waitingTime = obj.departureTime+60*24 - source.arrivalTime
                            node.g = obj.arrivalTime - obj.departureTime
                            node.day = i
                        else:
                            node.g = obj.arrivalTime+60*24 - obj.departureTime
                            
                            checkIndex+=1
                            if(checkIndex >len(Days)-1 ):
                                break
                            node.day = Days[checkIndex]
                        node.g+=source.g+source.h+waitingTime    
                        if(checkIndex <= secondDayIndex):    
                            node.flightName = obj.flightNumber
                            node.cityName = obj.destinationCity
                            node.departureTime = obj.departureTime
                            node.arrivalTime = obj.arrivalTime
                            node.arrTime = obj.arrTime
                            node.depTime = obj.depTime
                            
                            node.parent = source
                            node.h = getDistanceTime(source.cityName, goal, cities_dic)
                            child.append(node)
                            break
                        
                        
                                        
    return child

#flightName
#cityName 
#departureTime 
#arrivalTime 
#day
#parent
#h
#g 

def minimum(l):
     node = Node();
     node = l[0]
     for i in l:
         if((i.h+i.g)<(node.h+node.g)):
             node = i       
     return node
 
def aStar(start,goal,dayList):
    openlist = []
    closelist = []
    node = Node()
    node.cityName = start
    openlist.append(node)
    while openlist:
        current  = minimum(openlist)
        openlist.remove(current)
        if(current.cityName == goal):
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]
        elif(current.cityName in closelist):
            continue
           
        else:
            children =getChild(current,dayList,goal)
            for i in children:
                
                openlist.append(i)
                      
        closelist.append(current.cityName)
    
    return []       


if __name__ == '__main__':
    firstDay = input("first day :")
    secondDay = input("Second day :")
    sourceCity = input("sourceCity :")
    goalCity = input("goalCity :")
    list=[]  
    saveFlight(list)   
    cities_dic = {}
    saveCities(cities_dic) 
    lk = aStar(sourceCity,goalCity,[firstDay,secondDay])
    while(len(lk)==0):
        index1 = Days.index(firstDay)
        index2 = Days.index(secondDay)
        if(index1 !=0):
            index1-=1
        elif(index2 !=len(Days)-1):
            index2+=1
        print(sourceCity ,"|",goalCity)    
        lk = aStar(sourceCity,goalCity,[Days[index1],Days[index2]])
    for i in range(len(lk)-1):
        print("step",i+1,": use flight ",lk[i+1].flightName,"from ",lk[i].cityName," to ",lk[i+1].cityName," Departure time ",lk[i+1].depTime," arrival time ",lk[i+1].arrTime," in",lk[i+1].day)



    