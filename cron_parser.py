import argparse

CRON_LIMITS = {
    "minute": (0, 59),
    "hour": (0, 23),
    "day_of_month": (1, 31),
    "month": (1, 12),
    "day_of_week": (0, 6)
}

def parse_cron_field(field, field_name):
    min, max = CRON_LIMITS[field_name]
    if field == "*":
        return list(range(min, max+1))
    if "-" in field:
        start, end = field.split("-")
        if start.isdigit() and end.isdigit():
            if int(start) > int(end) or int(start) < min or int(end) > max:
                raise ValueError(f"Invalid range: {field} in {field_name}")
            return list(range(int(start), int(end)+1))
        else:
            raise ValueError(f"Invalid range format: {field} in {field_name}")
    if "/" in field:
        start, step = field.split("/")
        if step.isdigit() and (int(step) < 1 or int(step) > max):
            raise ValueError(f"Invalid step value: {step} in {field_name}")
        if start == "*":
            return list(range(min, max+1, int(step)))
        elif start.isdigit():
            if int(start) < min or int(start) > max:
                raise ValueError(f"Invalid start value: {start} in {field_name}")
            return list(range(int(start), max+1, int(step)))
        else:
            raise ValueError(f"Invalid start value: {field} in {field_name}")
    if "," in field:
        values = field.split(",")
        result = []
        for value in values:
            if value.isdigit():
                if int(value) < min or int(value) > max:
                    raise ValueError(f"Invalid value: {value} in {field_name}")
                result.append(int(value))
            else:
                raise ValueError(f"Invalid value format: {value} in {field_name}")
        return result
    if field.isdigit():
        if int(field) >= min and int(field) <= max:
            return [int(field)]
        else:
            raise ValueError(f"Invalid value: {field} in {field_name}")
    raise ValueError(f"Invalid cron expression: {field} in {field_name}")

def parse_cron_expression(cron_expression):
    commands = cron_expression.split(" ")
    if len(commands) != 6:
        raise ValueError("Invalid cron expression. Expected 5 fields and a command.")
    minute, hour, day, month, day_of_week, command = commands

    minute = parse_cron_field(minute, "minute")
    hour = parse_cron_field(hour, "hour")
    day_of_month = parse_cron_field(day, "day_of_month")
    month = parse_cron_field(month, "month")
    day_of_week = parse_cron_field(day_of_week, "day_of_week")
    return minute, hour, day_of_month, month, day_of_week, command

def main(args):
    fields = parse_cron_expression(args.cron_expression)
    # The output should be formatted as a table with the field name taking the first 14 columns and the times as a space-separated list following it.
    for field, value in zip(["minute", "hour", "day of month", "month", "day of week"], fields[:-1]):
        print(f"{field:<14} {' '.join(map(str, value))}")
    print(f"{'command':<14} {fields[-1]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse a cron expression.')
    parser.add_argument('cron_expression', type=str, help='The cron expression to parse.')
    args = parser.parse_args()
    main(args)