import unittest
from cron_parser import parse_cron_field, parse_cron_expression

class TestCronParser(unittest.TestCase):

    def test_parse_cron_field(self):
        self.assertEqual(parse_cron_field("*/15", "minute"), [0, 15, 30, 45])
        self.assertEqual(parse_cron_field("1-5", "hour"), [1, 2, 3, 4, 5])
        self.assertEqual(parse_cron_field("1,15", "day_of_month"), [1, 15])
        self.assertEqual(parse_cron_field("*", "month"), list(range(1, 13)))
        self.assertEqual(parse_cron_field("0-6", "day_of_week"), [0, 1, 2, 3, 4, 5, 6])

    def test_invalid_cron_field(self):
        with self.assertRaises(ValueError):
            parse_cron_field("*/70", "minute")  # Out of range
        with self.assertRaises(ValueError):
            parse_cron_field("10-5", "hour")  # Invalid range
        with self.assertRaises(ValueError):
            parse_cron_field("100", "month")  # Invalid value
        with self.assertRaises(ValueError):
            parse_cron_field("50", "day_of_month")  # Invalid value
        with self.assertRaises(ValueError):
            parse_cron_field("8", "day_of_week")  # Invalid value
        with self.assertRaises(ValueError):
            parse_cron_field("SUN", "day_of_week")  # Invalid value
        with self.assertRaises(ValueError):
            parse_cron_field("JAN", "month")  # Invalid value

    def test_parse_cron_expression(self):
        cron_expr = "*/15 0 1,15 * 1-5 /usr/bin/find"
        expected_fields = (
            [0, 15, 30, 45],  # minute
            [0],              # hour
            [1, 15],          # day of month
            list(range(1, 13)),  # month
            [1, 2, 3, 4, 5]   # day of week
        )
        expected_command = "/usr/bin/find"
        fields = parse_cron_expression(cron_expr)
        self.assertEqual(fields[:-1], expected_fields)
        self.assertEqual(fields[-1], expected_command)

if __name__ == '__main__':
    unittest.main()