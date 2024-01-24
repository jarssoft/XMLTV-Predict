
def minute(time):
    return int(time[10:12])

def hour(time):
    return int(time[8:10])

def day(time):
    return int(time[6:8])

def dayTime(time):
    return hour(time) * 60 + minute(time)

def totalTime(time):
    return (day(time) * 24 + hour(time)) * 60 + minute(time)

def dayType(time):
    if(hour(time)>5):
        return "viikonloppu" if day(time) in (19, 20, 26, 27) else "arki" 
    else: 
        return "viikonloppu" if day(time) in (20, 21, 27, 28) else "arki"
    
def timeDistance(start, stop):
    return totalTime(stop) - totalTime(start)

def addMinuts(time, delta):
    minuts = dayTime(time) + delta
    return time[:8] + str(int(minuts/60)).zfill(2) + str(minuts%60).zfill(2) + time[12:]

def nextFullHour(datetime):
    tunti=hour(datetime) + 1
    paiva=day(datetime) + (1 if tunti>23 else 0)
    return datetime[:6]+str(paiva).zfill(2)+str(tunti%24).zfill(2)+"0000"+datetime[14:]