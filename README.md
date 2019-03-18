# Sector Alarm library

#### Example

``` python
import sectoralarmlib.sector as sector

alarm = sector.SectorAlarm("username","password",  "siteid",  "code")

# Get status
status = alarm.AlarmStatus()
print(status)

# Get temperatures
temps = alarm.GetTemps()
for x, y in temps:
	print(x, y)

# Turn on alarm
alarm.Arm()

# Turn off alarm
alarm.Disarm()

```