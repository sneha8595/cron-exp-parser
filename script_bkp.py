import argparse
import sys

CRON_LIMITS = {
    "minute": (0, 59),
    "hour": (0, 23),
    "day of month": (1, 31),
    "month": (1, 12),
    "day of week": (0, 6)
}

def expand_cron_field(field, field_name):
    """Expands a cron field based on ranges, steps, and lists."""
    min_val, max_val = CRON_LIMITS[field_name]
    
    values = set()
    parts = field.split(',')
    
    for part in parts:
        if part == '*':
            values.update(range(min_val, max_val + 1))
        elif part.startswith("*/"):  # Step values (*/N)
            step = int(part[2:])
            if step < 1 or step > max_val:
                raise ValueError(f"Invalid step value: {step} in {field_name}")
            values.update(range(min_val, max_val + 1, step))
        elif '-' in part:  # Ranges (N-M)
            start, end = map(int, part.split('-'))
            if start > end or start < min_val or end > max_val:
                raise ValueError(f"Invalid range: {part} in {field_name}")
            values.update(range(start, end + 1))
        else:  # Single values (N)
            num = int(part)
            if num < min_val or num > max_val:
                raise ValueError(f"Invalid value: {num} in {field_name}")
            values.add(num)

    return sorted(values)

def parse_cron_expression(cron_expr):
    """Parses a cron expression into expanded values."""
    parts = cron_expr.strip().split()
    if len(parts) < 6:
        raise ValueError("Invalid cron expression: must have 5 fields + command")

    fields = ["minute", "hour", "day of month", "month", "day of week"]
    expanded_fields = {}

    for i in range(5):
        expanded_fields[fields[i]] = expand_cron_field(parts[i], fields[i])

    command = " ".join(parts[5:])
    
    return expanded_fields, command

def format_output(expanded_fields, command):
    """Formats the expanded cron expression output as a table."""
    max_field_length = max(len(field) for field in expanded_fields)  # Align columns

    for field, values in expanded_fields.items():
        print(f"{field.ljust(max_field_length)} {' '.join(map(str, values))}")
    print(f"{'command'.ljust(max_field_length)} {command}")

def main():
    parser = argparse.ArgumentParser(
        description="Cron Expression Parser - Expands cron syntax into readable times."
    )
    parser.add_argument("cron_string", type=str, help="The cron expression to be parsed. Example: '*/15 0 1,15 * 1-5 /usr/bin/find'")

    args = parser.parse_args()

    try:
        expanded_fields, command = parse_cron_expression(args.cron_string)
        format_output(expanded_fields, command)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
