"""
Robot Maintenance Log Analyzer
-------------------------------
Reads an overnight robot log (name, battery level, camera status),
checks each robot for low battery or camera errors, and writes a
morning maintenance report. Invalid battery readings are handled
without stopping the camera check for that robot.
"""


def battery_check(robot, battery):
    if battery < 20:
        return robot + " needs charging"


def cam_check(robot, cam_status):
    if cam_status == "ERROR":
        return robot + " has camera issues"


log_file = open("night_log.txt", "r")
report = open("morning_report.txt", "w")

for line in log_file:
    line = line.strip()
    robot, battery, cam_status = line.split(",")

    try:
        battery = int(battery)

        battery_results = battery_check(robot, battery)

        if battery_results:
            report.write(battery_results + "\n")

    except ValueError:
        report.write(robot + " has invalid battery data\n")

    cam_results = cam_check(robot, cam_status)

    if cam_results:
        report.write(cam_results + "\n")

log_file.close()
report.close()
