# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from icalendar import *
import datetime
import pytz
import json

#### MODIFY THESE CONFIGURATIONS BEFORE RUNNING THE PROGRAM ###
timezone="Australia/Sydney"
numberofperiods=6
timetablepath="PATH TO ICS FILE"

# Find date of first Monday in icalendar events
def findfirstmonday(timetable):
    # Iterate over icalendar events
    for component in timetable.walk():
        if component.name=="VEVENT":
            # Get date of current iterated item
            loopdate=component.get("dtstart").dt.astimezone(pytz.timezone(timezone)).date()
            # Check if date is a Monday
            if loopdate.strftime('%A')=='Monday':
                return loopdate

# Create dictionary of final timetable details
def createtimetabledictionary(classlist,weekdates):
    timetabledictionary={}
    x=0
    for i in range(len(weekdates)):
        daydictionary={}
        daycompleted=False
        while daycompleted==False:
            classlistitemtemp=classlist[x] 
            if str(classlistitemtemp[0])==weekdates[i]:
                daydictionary[classlistitemtemp[1]]=[classlistitemtemp[2],classlistitemtemp[3],classlistitemtemp[4]]
                try:
                    classlist[x+1]
                    x+=1
                except:
                    timetabledictionary[datetime.datetime.strptime(weekdates[i],'%Y-%m-%d').strftime('%A')]=daydictionary
                    daycompleted=True
            else:
                timetabledictionary[datetime.datetime.strptime(weekdates[i],'%Y-%m-%d').strftime('%A')]=daydictionary
                daycompleted=True
        i+=1
    print(timetabledictionary)
    jsontimetable=json.dumps(timetabledictionary, indent=4)
    with open('timetable.json','w') as jsonexport:
        jsonexport.write(jsontimetable)


# Create unsorted list of class details
def getweekdata(timetabledetails):
    classlist=[]
    weekdates=[]
    timetable=Calendar.from_ical(timetabledetails.read())

    firsteventdate=findfirstmonday(timetable)
    lasteventdate=firsteventdate+datetime.timedelta(days=4)
    currentitemloopdate=firsteventdate
    icalparseloop=1
    while currentitemloopdate<=lasteventdate:
        currentitemloop=timetable.walk()[icalparseloop]
        if currentitemloop.name=="VEVENT":
            currentitemloopdate=currentitemloop.get("dtstart").dt.astimezone(pytz.timezone('Australia/Sydney')).date()
            if currentitemloopdate<=lasteventdate and currentitemloopdate>=firsteventdate:
                # Create list containing iterated class details
                tempclassdetailsdate=currentitemloop.get("dtstart").dt.astimezone(pytz.timezone('Australia/Sydney')).date()
                tempclassdetailsperiod=str(currentitemloop.get("description")).split("\n")[1].replace("Period: ","")
                tempclassdetailsname=str(currentitemloop.get("summary"))
                tempclassdetailslocation=str(currentitemloop.get("location")).replace("Room: ","")
                tempclassdetailsteacher=str(currentitemloop.get("description")).split("\n")[0].replace("Teacher:  ","").lower().title()
                # Check if class is before/after school and skips if it is
                if len(tempclassdetailsperiod)<=numberofperiods:
                    if int(tempclassdetailsperiod[-1])>0 and int(tempclassdetailsperiod[-1])<9:
                        # Set period to single digit
                        tempclassdetailsperiod=tempclassdetailsperiod[-1]
                        # Add class details to unsorted class list
                        tempclassdetails=[tempclassdetailsdate,tempclassdetailsperiod,tempclassdetailsname,tempclassdetailslocation,tempclassdetailsteacher]
                        classlist.append(tempclassdetails)
                        # Create list of unique dates which classlist contains
                        if str(currentitemloopdate) not in weekdates:
                            weekdates.append(str(currentitemloop.get("dtstart").dt.astimezone(pytz.timezone('Australia/Sydney')).date()))
        icalparseloop+=1
    createtimetabledictionary(classlist,weekdates)

with open(timetablepath,'rb') as f:
    getweekdata(f)
