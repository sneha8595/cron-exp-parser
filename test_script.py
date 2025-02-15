import unittest
from script_bkp import expand_cron_field, parse_cron_expression

class TestCronParser(unittest.TestCase):

    def test_expand_cron_field(self):
        self.assertEqual(expand_cron_field("*/15", "minute"), [0, 15, 30, 45])
        self.assertEqual(expand_cron_field("1-5", "hour"), [1, 2, 3, 4, 5])
        self.assertEqual(expand_cron_field("1,15", "day of month"), [1, 15])
        self.assertEqual(expand_cron_field("*", "month"), list(range(1, 13)))
        self.assertEqual(expand_cron_field("0-6", "day of week"), [0, 1, 2, 3, 4, 5, 6])

    def test_invalid_cron_field(self):
        with self.assertRaises(ValueError):
            expand_cron_field("*/70", "minute")  # Out of range
        with self.assertRaises(ValueError):
            expand_cron_field("10-5", "hour")  # Invalid range
        with self.assertRaises(ValueError):
            expand_cron_field("100", "month")  # Invalid value

    def test_parse_cron_expression(self):
        cron_expr = "*/15 0 1,15 * 1-5 /usr/bin/find"
        expected = {
            "minute": [0, 15, 30, 45],
            "hour": [0],
            "day of month": [1, 15],
            "month": list(range(1, 13)),
            "day of week": [1, 2, 3, 4, 5]
        }
        fields, command = parse_cron_expression(cron_expr)
        self.assertEqual(fields, expected)
        self.assertEqual(command, "/usr/bin/find")

if __name__ == '__main__':
    unittest.main()