# coding: utf-8
import subprocess
import re
import datetime

class PowerDetails(object):
    def __init__(self, source, connected, charging, percentage, remaining):
        self.source = source
        self.connected = connected
        self.charging = charging
        self.percentage = percentage
        self.remaining = remaining

class ParseException(StandardError):
    pass

PMSET_RE = re.compile("""^Now drawing from '([ A-Za-z]+)'\n -InternalBattery-\d \(id=\d+\)\s*(\d{1,3})%; ([A-Za-z ]+); ([A-Za-z()0-9: ]+) present""", re.MULTILINE)

STATE = {
    'Battery Power': 'battery',
    'AC Power': 'power'
}

def _parse_pmset(output):
    match = PMSET_RE.match(output)
    if match:
        source=STATE[match.groups()[0]]
        charging_state = match.groups()[2]
        if charging_state == "AC attached":
            charging_state = 'attached'
        remaining_raw = match.groups()[3]
        if remaining_raw == "(no estimate)":
            remaining = None
        elif remaining_raw == "not charging":
            remaining = None
        else:
            hour = int(remaining_raw.split(':')[0])
            minute = int(remaining_raw.split(':')[1].split(' ')[0])
            remaining = datetime.timedelta(hours=hour, minutes=minute)
        return PowerDetails(
            source=source,
            connected= False if source == 'battery' else True,
            charging=charging_state,
            percentage=int(match.groups()[1]),
            remaining=remaining)
    else:
        raise ParseException()

def get_power_management_details():
    output = subprocess.check_output(['pmset', '-g', 'batt'], shell=False)
    return _parse_pmset(output)

def nice_format():
    details = get_power_management_details()
    if details.remaining:
        s = details.remaining.total_seconds()
        remaining = '{:02.0f}:{:02.0f}'.format(s // 3600, s % 3600 // 60)
    else:
        remaining = "-:--"

    if details.source == "battery":
        icon = "🔋"
        extra = remaining
    else:
        icon = "🔌"
        extra = "{:.0%}".format(details.percentage / 100.0)

    return "{}  | {}".format(icon, extra)

def basic_format():
    details = get_power_management_details()
    if details.remaining:
        s = details.remaining.total_seconds()
        remaining = u'{:02.0f}:{:02.0f}'.format(s // 3600, s % 3600 // 60)
    else:
        remaining = u"-:--"

    if details.source == "battery":
        icon = u"battery"
        extra = remaining
    else:
        icon = u"power"
        extra = u"{:.0%}".format(details.percentage/100.0)

    return u"{} | {}".format(icon, extra)
