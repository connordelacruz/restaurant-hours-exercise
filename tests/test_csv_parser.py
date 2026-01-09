import unittest
from restaurant_hours import csv_parser

class TestCsvParser(unittest.TestCase):

    # ================================================================================
    # Helpers
    # ================================================================================

    @staticmethod
    def format_assertion_failure_msg(input_params, expected_result, actual_result):
        '''Returns a common assertion failure message format that displays the function input, expected result, and actual result.

        :param input_params: Whatever parameters are being passed to the function we're testing
        :param expected_result: Whatever the test is expecting the function to return
        :param actual_result: What the function actually returned

        :return: Assertion failure message string
        '''
        return f'Input: {str(input_params)}, Expected Result: {str(expected_result)}, Actual Result: {str(actual_result)}'

    @staticmethod
    def format_assertion_failure_msg_from_case(case, actual_result):
        '''Shorthand to call the above helper from common case dictionary structure.

        :param case: Dict with keys 'input' and 'expected'
        :param actual_result: What the function actually returned

        :return: Assertion failure message string
        '''
        return TestCsvParser.format_assertion_failure_msg(case['input'], case['expected'], actual_result)

    # ================================================================================
    # Tests
    # ================================================================================

    def test_convert_time_to_int(self):
        '''Verify convert_time_to_int() returns expected integer values.'''
        cases = [
            {
                'input': ('12', '00', 'am'),
                'expected': 0,
            },
            {
                'input': ('10', '30', 'am'),
                'expected': 1030,
            },
            {
                'input': ('12', '00', 'pm'),
                'expected': 1200,
            },
            {
                'input': ('11', '59', 'pm'),
                'expected': 2359,
            },
        ]
        for case in cases:
            result = csv_parser.convert_time_to_int(*case['input'])
            self.assertEqual(result, case['expected'],
                             self.format_assertion_failure_msg(case['input'], case['expected'], result))

    def test_sanitize_hours_string(self):
        '''Verify that sanitize_hours_string() parses time strings correctly.'''
        cases = [
            {
                'input': '12 am',
                'expected': 0,
            },
            {
                'input': '12:00 am',
                'expected': 0,
            },
            {
                'input': '10:30 am',
                'expected': 1030,
            },
            {
                'input': '12 pm',
                'expected': 1200,
            },
            {
                'input': '11:59 pm',
                'expected': 2359,
            },
        ]
        for case in cases:
            result = csv_parser.sanitize_hours_string(case['input'])
            self.assertEqual(result, case['expected'],
                             self.format_assertion_failure_msg_from_case(case, result))

    def test_parse_hours_range_string(self):
        '''Verify that parse_hours_range_string() parses open/close times into integers as expected.'''
        cases = [
            {
                'input': '12 am - 12:00 pm',
                'expected': (0, 1200),
            },
            {
                'input': '12:00 am - 12 pm',
                'expected': (0, 1200),
            },
            {
                'input': '10:30 am - 2 pm',
                'expected': (1030, 1400),
            },
        ]
        for case in cases:
            result = csv_parser.parse_hours_range_string(case['input'])
            self.assertEqual(result, case['expected'],
                             self.format_assertion_failure_msg_from_case(case, result))

    def test_parse_day_range_string(self):
        '''Verify that parse_day_range_string() returns a list of all weekdays in that range'''
        cases = [
            {
                'input': 'Mon-Sun',
                'expected': ['Mon', 'Tues', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            },
            {
                'input': 'Tues-Thu',
                'expected': ['Tues', 'Wed', 'Thu'],
            },
            {
                'input': 'Fri-Sat',
                'expected': ['Fri', 'Sat'],
            },
        ]
        for case in cases:
            result = csv_parser.parse_day_range_string(case['input'])
            self.assertEqual(result, case['expected'],
                             self.format_assertion_failure_msg_from_case(case, result))

    def test_parse_days_string(self):
        '''Verify that test_parse_days_string() splits out days and day ranges into a list of days as expected.'''
        cases = [
            {
                'input': 'Mon,Wed,Fri',
                'expected': ['Mon', 'Wed', 'Fri'],
            }
        ]

    def test_parse_hours_block_string(self):
        pass

    def test_parse_restaurant_hours_string(self):
        pass
