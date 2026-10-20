import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from operating_forecast import forecast, load_inputs


class OperatingTests(unittest.TestCase):
    def setUp(self):
        self.inputs = load_inputs()

    def test_reported_history_and_normalized_view_stay_separate(self):
        snapshot = copy.deepcopy(self.inputs[0])
        result = forecast(*self.inputs)
        first = result['annual'][0]
        self.assertAlmostEqual(first['operating_income'], -244.633)
        self.assertAlmostEqual(first['normalized_operating_income'], -233.453)
        self.assertAlmostEqual(first['sga'], 111.610+61+64)
        self.assertAlmostEqual(first['rd'], 162.942+85+88)
        for row in result['annual'][1:]:
            self.assertEqual(row['historical_cancellation_adjustment'], 0)
        self.assertEqual(snapshot, self.inputs[0])

    def test_rd_increase_reduces_ebit_dollar_for_dollar(self):
        before = forecast(*self.inputs)['annual']
        self.inputs[3]['cases']['base']['rd'][2] += 10
        after = forecast(*self.inputs)['annual']
        self.assertAlmostEqual(after[3]['operating_income']-before[3]['operating_income'], -10)
        self.assertEqual(after[3]['gross_profit'], before[3]['gross_profit'])
        self.assertEqual(after[3]['total_revenue'], before[3]['total_revenue'])
        for i in (0, 1, 2, 4):
            self.assertEqual(before[i], after[i])

    def test_zero_neutron_does_not_erase_readiness_or_rd(self):
        before = forecast(*self.inputs)['annual']
        self.inputs[1]['cases']['base']['neutron_revenue_equivalents_2026_2030'] = [0]*5
        after = forecast(*self.inputs)['annual']
        for i in range(1, 5):
            b, a = before[i], after[i]
            self.assertEqual(a['neutron_gross_profit'], -b['neutron_fixed_commercial_cost'])
            self.assertEqual(a['rd'], b['rd'])
            self.assertEqual(a['sga_fixed'], b['sga_fixed'])
            expected = -b['neutron_contribution'] + .08*b['incremental_neutron']
            self.assertAlmostEqual(a['operating_income']-b['operating_income'], expected)

    def test_margin_change_flows_to_gross_profit_and_ebit_once(self):
        before = forecast(*self.inputs)['annual'][3]
        self.inputs[3]['cases']['base']['space_margin'][2] -= .01
        after = forecast(*self.inputs)['annual'][3]
        expected = -.01*before['space_systems']
        self.assertAlmostEqual(after['gross_profit']-before['gross_profit'], expected)
        self.assertAlmostEqual(after['operating_income']-before['operating_income'], expected)
        self.assertEqual(after['rd'], before['rd'])

    def test_guidance_is_an_anchor_not_a_constraint_on_downside(self):
        base = forecast(*self.inputs)
        downside = forecast(*self.inputs, case='downside')
        self.assertTrue(base['q3_margin_in_guidance'])
        self.assertTrue(base['q3_opex_in_guidance'])
        self.assertFalse(downside['q3_margin_in_guidance'])
        self.assertFalse(downside['q3_opex_in_guidance'])
        for b, d in zip(base['annual'][1:], downside['annual'][1:]):
            self.assertGreater(d['rd'], b['rd'])

    def test_bad_units_values_and_cutoff_fail(self):
        for key, value in [('space_margin', [35]*4), ('rd', [-1]*4),
                           ('sga_fixed', [float('nan')]*4), ('rd', [10]*3)]:
            bad = copy.deepcopy(self.inputs)
            bad[3]['cases']['base'][key] = value
            with self.assertRaises(ValueError):
                forecast(*bad)
        bad = copy.deepcopy(self.inputs)
        bad[3]['cutoff'] = '2026-09-30T16:00:00-04:00'
        with self.assertRaises(ValueError):
            forecast(*bad)
        bad = copy.deepcopy(self.inputs)
        bad[3]['sources']['Q26']['published'] = '2026-09-15'
        with self.assertRaises(ValueError):
            forecast(*bad)


if __name__ == '__main__':
    unittest.main()
