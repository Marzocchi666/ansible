import unittest

from ansible.parsing.utils.addresses import parse_address

class TestParseAddress(unittest.TestCase):

    tests = {
        # IPv4 addresses
        '192.0.2.3': ['192.0.2.3', None],
        '192.0.2.3:23': ['192.0.2.3', 23],

        # IPv6 addresses
        '::': ['::', None],
        '::1': ['::1', None],
        '[::1]:442': ['::1', 442],
        'abcd:ef98:7654:3210:abcd:ef98:7654:3210': ['abcd:ef98:7654:3210:abcd:ef98:7654:3210', None],
        '[abcd:ef98:7654:3210:abcd:ef98:7654:3210]:42': ['abcd:ef98:7654:3210:abcd:ef98:7654:3210', 42],

        # Hostnames
        'some-host': ['some-host', None],
        'some-host:80': ['some-host', 80],
        'some.host.com:492': ['some.host.com', 492],
        '[some.host.com]:493': ['some.host.com', 493],

        # Various errors
        '': [None, None],
        'some..host': [None, None],
        'some.': [None, None],
        '[example.com]': [None, None],
    }

    range_tests = {
        '192.0.2.[3:10]': ['192.0.2.[3:10]', None],
        '192.0.2.[3:10]:23': ['192.0.2.[3:10]', 23],
        'abcd:ef98::7654:[1:9]': ['abcd:ef98::7654:[1:9]', None],
        '[abcd:ef98::7654:[6:32]]:2222': ['abcd:ef98::7654:[6:32]', 2222],
        'foo[a:b]:42': ['foo[a:b]', 42],
        'foo[a-b]:32': [None, None],
        'foo[x-y]': [None, None],
    }

    def test_without_ranges(self):
        for t in self.tests:
            test = self.tests[t]

            (host, port) = parse_address(t)
            assert host == test[0]
            assert port == test[1]

    def test_with_ranges(self):
        for t in self.range_tests:
            test = self.range_tests[t]

            (host, port) = parse_address(t, allow_ranges=True)
            assert host == test[0]
            assert port == test[1]
