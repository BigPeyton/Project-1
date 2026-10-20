"""Cash-definition, double-counting and financing-pair checks (AI assisted)."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from cash_bridge import estimate, load_inputs


class CashBridgeTests(unittest.TestCase):
    def setUp(self):
        self.r, self.c, self.a = load_inputs()

    def test_no_burn_cash_excludes_restricted_and_unused_funding(self):
        a = copy.deepcopy(self.a)
        a['valuation_date'] = a['opening_date']
        v = estimate(self.r, self.c, a)
        self.assertEqual(v['estimated_cash_m'], 2129.485)
        self.assertAlmostEqual(v['total_liquidity_m'], 2387.590)
        self.assertEqual(v['hypothetical_atm_net_m'], 0)

    def test_portfolio_transfer_preserves_liquidity(self):
        changed = copy.deepcopy(self.r)
        bs = changed['h1_2026']['balance_sheet']
        bs['cash'] += 10000
        bs['securities_current'] -= 10000
        v = estimate(changed, self.c, self.a)
        base = estimate(self.r, self.c, self.a)
        self.assertAlmostEqual(v['total_liquidity_m'], base['total_liquidity_m'])

    def test_financing_pairs_shares_with_net_proceeds(self):
        v = estimate(self.r, self.c, self.a, atm_fraction=1)
        self.assertAlmostEqual(v['hypothetical_atm_new_shares_m'] * 61.96, 1944.369826)
        self.assertAlmostEqual(v['hypothetical_atm_net_m'], 1905.48242948)
        base = estimate(self.r, self.c, self.a)
        self.assertAlmostEqual(v['estimated_cash_m']-base['estimated_cash_m'], 1905.48242948)

    def test_option_proceeds_not_counted_twice(self):
        v = estimate(self.r, self.c, self.a)
        self.assertAlmostEqual(v['known_option_receipt_m'] + v['hypothetical_remaining_option_receipts_m'], 3.85649521)

    def test_stress_lowers_available_liquidity(self):
        base = estimate(self.r, self.c, self.a)
        stress = estimate(self.r, self.c, self.a, burn_multiplier=1.5, reserve_m=300, securities_haircut=.02)
        self.assertLess(stress['standalone_liquidity_after_reserve_m'], base['standalone_liquidity_after_reserve_m'])

    def test_invalid_inputs_fail_loudly(self):
        for kwargs in ({'atm_fraction':1.01}, {'issue_price':0}, {'reserve_m':float('nan')},
                       {'securities_haircut':-0.1}, {'reserve_m':100000}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                estimate(self.r, self.c, self.a, **kwargs)


if __name__ == '__main__':
    unittest.main()
