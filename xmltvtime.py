
def minute(time):
    return int(time[10:12])

def hour(time):
    return int(time[8:10])

def day(time):
    return int(time[6:8])

def dayTime(time):
    return hour(time) * 60 + minute(time)

def dayType(time):
    if(hour(time)>5):
        return "viikonloppu" if day(time) in (19, 20, 26, 27) else "arki"      
    else: 
        return "viikonloppu" if day(time) in (20, 21, 27, 28) else "arki"      