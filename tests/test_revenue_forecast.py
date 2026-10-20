import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from revenue_forecast import forecast, load_inputs


class RevenueTests(unittest.TestCase):
    def setUp(self):
        self.reported, self.a = load_inputs()

    def test_historical_plus_forecast_once(self):
        snapshot = copy.deepcopy(self.reported)
        rows = forecast(self.reported, self.a)
        self.assertAlmostEqual(rows[0]['total_revenue'], 434.414+257.5+280)
        for row in rows:
            self.assertAlmostEqual(row['total_revenue'], row['total_launch']+row['space_systems'])
        self.assertEqual(snapshot, self.reported)

    def test_neutron_delay_removes_only_incremental_revenue(self):
        base = forecast(self.reported, self.a)
        self.a['cases']['base']['neutron_revenue_equivalents_2026_2030'] = [0]*5
        delayed = forecast(self.reported, self.a)
        for before, after in zip(base, delayed):
            self.assertEqual(before['space_systems'], after['space_systems'])
            self.assertEqual(before['continuing_launch'], after['continuing_launch'])
            self.assertAlmostEqual(before['total_revenue']-after['total_revenue'], before['incremental_neutron'])

    def test_bad_segment_allocation_and_history_fail(self):
        self.a['cases']['base']['q3_launch'] = 1000
        with self.assertRaises(ValueError):
            forecast(self.reported, self.a)
        self.reported, self.a = load_inputs()
        self.a['facts']['h1_2026_launch'] += 1
        with self.assertRaises(ValueError):
            forecast(self.reported, self.a)

    def test_scenarios_are_ordered_but_not_probabilities(self):
        lo, base, hi = [forecast(self.reported, self.a, c) for c in ('downside', 'base', 'upside')]
        for l, b, h in zip(lo, base, hi):
            self.assertLess(l['total_revenue'], b['total_revenue'])
            self.assertLess(b['total_revenue'], h['total_revenue'])

    def test_bad_path_and_hindsight_fail(self):
        self.a['cases']['base']['space_growth_2027_2030'] = [0.2]*3
        with self.assertRaises(ValueError):
            forecast(self.reported, self.a)
        self.reported, self.a = load_inputs()
        self.a['sources']['Q26']['published'] = '2026-09-15'
        with self.assertRaises(ValueError):
            forecast(self.reported, self.a)


if __name__ == '__main__':
    unittest.main()
