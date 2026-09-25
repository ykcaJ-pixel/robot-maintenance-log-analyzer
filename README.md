# Robot Maintenance Log Analyzer

A Python script that reads an overnight robot log, checks each robot for low
battery or camera errors, and writes a morning maintenance report — while
still handling bad or missing data gracefully.

## What it does

For each robot in the log, the script:

1. Parses the robot's name, battery level, and camera status
2. Converts the battery reading to a number
3. Flags the robot if its battery is below 20
4. Flags the robot if its camera status is `ERROR`
5. If the battery reading is invalid (not a number), logs that instead of
   crashing — and still runs the camera check for that robot
6. Writes every issue found to `morning_report.txt`

## Example input (`night_log.txt`)

```
Atlas_01,88,ONLINE
Atlas_02,14,ONLINE
Atlas_03,65,ERROR
Atlas_04,9,ONLINE
Atlas_05,unknown,ERROR
Atlas_06,72,ONLINE
```

## Example output (`morning_report.txt`)

```
Atlas_02 needs charging
Atlas_03 has camera issues
Atlas_04 needs charging
Atlas_05 has invalid battery data
Atlas_05 has camera issues
```

## How to run it

```
python robot_inspection.py
```

(Make sure `night_log.txt` is in the same folder as the script. The report
will be created/overwritten as `morning_report.txt`.)

## The `Atlas_05` edge case — why it matters

`Atlas_05` has a battery value of `unknown`, which can't be converted to a
number. Handling this correctly took a bit of trial and error: my first
version put the camera check *inside* the same `try` block as the battery
conversion, so when the battery conversion failed, Python skipped straight
to `except` — and the camera check never ran, even though the camera data
was perfectly valid.

The fix was to move the camera check *outside* the `try/except`, so a bad
battery reading for one robot doesn't stop the script from still checking
that robot's camera status. This is a small example of a broader lesson:
one bad field in a data record shouldn't prevent the rest of the record
from being checked.

## Python concepts used

- Functions, parameters, and `return` values
- Calling one function from within a loop
- File reading and file writing
- `.strip()` and `.split(",")` for parsing structured text
- Type conversion with `int()`
- `try` / `except` for handling invalid data
- Separating checks into small, reusable functions

## Why this is relevant to robotics operations

This models a real maintenance workflow: pulling overnight equipment data,
flagging what needs attention before a shift starts, and producing a report
a technician or operator can act on — without the whole process breaking
because one robot logged bad data.
