# Sector Alarm library

#### Example
``` python
import sectoralarmlib.sector as sector

alarm = sector.SectorAlarm("username","password", "siteid", "code")

status = alarm.AlarmStatus()
print(status)

temps = alarm.GetTemps()
for x, y in temps:
  print(x, y)
```