import unittest
import pypower
import sys

from datetime import timedelta

DISCHARGING="""Now drawing from 'Battery Power'
 -InternalBattery-0 (id=4391011)        87%; discharging; 6:17 remaining present: true"""

NOT_CHARGING="""Now drawing from 'AC Power'
 -InternalBattery-0 (id=4391011)        87%; AC attached; not charging present: true"""

CHARGING="""Now drawing from 'AC Power'
 -InternalBattery-0 (id=4391011)        87%; charging; (no estimate) present: true"""

CHARGED="""Now drawing from 'AC Power'
 -InternalBattery-0 (id=4391011)       100%; charged; 0:00 remaining present: true"""

class PowerTest(unittest.TestCase):
    def testDisconnected(self):
        power_details = pypower._parse_pmset(DISCHARGING)
        self.assertEqual(power_details.source, 'battery')
        self.assertFalse(power_details.connected)
        self.assertEqual(power_details.charging, 'discharging')
        self.assertEqual(power_details.percentage, 87)
        self.assertEqual(power_details.remaining, timedelta(hours=6, minutes=17))

    def testNotCharging(self):
        power_details = pypower._parse_pmset(NOT_CHARGING)
        self.assertEqual(power_details.source, 'power')
        self.assertTrue(power_details.connected)
        self.assertEqual(power_details.charging, 'attached')
        self.assertEqual(power_details.percentage, 87)
        self.assertIsNone(power_details.remaining)

    def testCharging(self):
        power_details = pypower._parse_pmset(CHARGING)
        self.assertEqual(power_details.source, 'power')
        self.assertTrue(power_details.connected)
        self.assertTrue(power_details.charging)
        self.assertEqual(power_details.percentage, 87)
        self.assertIsNone(power_details.remaining)

    def testCharged(self):
        power_details = pypower._parse_pmset(CHARGED)
        self.assertEqual(power_details.source, 'power')
        self.assertTrue(power_details.connected)
        self.assertEqual(power_details.charging, 'charged')
        self.assertEqual(power_details.percentage, 100)
        self.assertEqual(power_details.remaining, timedelta(0, 0))
