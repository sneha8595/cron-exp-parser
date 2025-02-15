# Cron Expression Parser

## Overview

This script parses a standard cron expression and prints the expanded schedule in a readable tabular format. It supports different cron syntax elements like `*`, `,`, `-`, and `/` for defining execution schedules.

## Features

- Parses standard 5-field cron expressions (minute, hour, day of month, month, day of week)
- Expands fields into explicit values
- Supports special cron syntax:
  - `*` (wildcard, all values)
  - `-` (range)
  - `/` (step values)
  - `,` (list of values)
- Outputs a neatly formatted table

## Usage

### Running the Script
python cron_parser.py "*/15 0 1,15 * 1-5 /usr/bin/find"

### Example Output
minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find

## Requirements

- Python 3.x

## Troubleshooting

### Python Not Found

If `python` is not recognized, try:

python3 cron_parser.py "*/15 0 1,15 * 1-5 /usr/bin/find"