import argparse

DAYS= {"SUN": 0, "MON": 1, "TUE": 2, "WED": 3, "THU": 4, "FRI": 5, "SAT": 6}
MONTHS = {"JAN":1, "FEB":2, "MAR":3, "APR":4,"MAY":5, "JUN":6,"JUL":7, "AUG":8, "SEP":9, "OCT":10, "NOV":11, "DEC":12}

def parse_cron_field(field, min, max, field_name):
    if field == "*":
        return list(range(min, max+1))
    if "-" in field:
        start, end = field.split("-")
        return list(range(int(start), int(end)+1))
    if "*" in field:
        start, step = field.split("/")
        return list(range(min, max+1, int(step)))
    if "," in field:
        return [int(x) for x in field.split(",")]
    return [int(field)] if validate_limits(int(field), min, max, field_name) is None else None

def validate_limits(field, min, max, field_name):
    if field < min:
        raise ValueError(f"Value {field} is less than the minimum value {min} for field {field_name}")
    if field > max:
        raise ValueError(f"Value {field} is greater than the maximum value {max} for field {field_name}")

def parse_cron_expression(cron_expression):
    commands = cron_expression.split(" ")
    if len(commands) != 6:
        raise ValueError("Invalid cron expression. Expected 5 fields and a command.")
    minute, hour, day, month, day_of_week, command = commands

    minute = parse_cron_field(minute, 0, 59, "minute")
    hour = parse_cron_field(hour, 0, 23, "hour")
    day = parse_cron_field(day, 1, 31, "day")
    month = parse_cron_field(month, 1, 12, "month")
    day_of_week = parse_cron_field(day_of_week, 0, 6, "day_of_week")
    return minute, hour, day, month, day_of_week, command

def main(args):
    fields = parse_cron_expression(args.cron_expression)
    # The output should be formatted as a table with the field name taking the first 14 columns and the times as a space-separated list following it.
    for field, value in zip(["minute", "hour", "day of month", "month", "day of week"], fields[:-1]):
        print(f"{field:<14} {' '.join(map(str, value))}")
    print(f"{'command':<14} {fields[-1]}")

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parse a cron expression.')
    # */15 0 1,15 * 1-5 /usr/bin/find
    parser.add_argument('cron_expression', type=str, help='The cron expression to parse.')
    args = parser.parse_args()
    main(args)