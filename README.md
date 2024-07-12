# sentral-ics-to-json [![License: MPL 2.0](https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
Simple python script to extract the classes from a Sentral timetable to a json file. 

## Installation and Usage
1. Download the python script "main.py".
2. Install packages icalendar and pytz through pip using <code>pip install icalendar pytz</code>
3. Obtain the Sentral timetable calendar file by going to the Sentral Portal -> My Timetable -> "Export as iCal" button (in the top right)
4. Configure the variables at the top of the script to set the correct time zone, number of periods, and path to the timetable file
5. Run the script with <code>python main.py</code> which will output the timetable as a dictionary as well as to timetable.json

## Limitations
* The script ignores classes from before and after school due as this syntax varies between schools and is not standard. 
* The script does not take into account A/B weeks and will only output the timetable for the first full (Mon-Fri) week scheduled for the term. You can implement A/B week yourself by modifying the code to run <code>getweekdata()</code> twice using a different <code>firsteventdate</code> that has a timedelta of 1 week in the second iteration. 

## License
This project is licensed under the
[Mozilla Public License](https://www.mozilla.org/MPL/2.0/), version 2.0.
