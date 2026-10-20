import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from claims_bridge import reconcile_claims, note_treatment
from cash_bridge import estimate, load_inputs


class ClaimsTests(unittest.TestCase):
    def setUp(self):
        self.r, self.c, self.a = load_inputs()
        self.cash = estimate(self.r, self.c, self.a)
        self.claims = json.loads((ROOT / 'data/claims.json').read_text())

    def test_lease_principal_payment_reduces_cash_and_claim_equally(self):
        before = reconcile_claims(self.claims, self.cash)
        later = dict(self.cash)
        later['estimated_lease_principal_m'] += .1
        later['standalone_liquidity_after_reserve_m'] -= .1
        after = reconcile_claims(self.claims, later)
        self.assertAlmostEqual(before['liquidity_after_selected_claims_m'], after['liquidity_after_selected_claims_m'])

    def test_conversion_exchanges_claim_for_shares(self):
        shares_c, debt_c = note_treatment('converted', self.c, self.claims)
        shares_r, debt_r = note_treatment('retained', self.c, self.claims, 280.789)
        self.assertAlmostEqual(shares_c-shares_r, 2.607745)
        self.assertEqual(debt_c, 0)
        self.assertEqual(debt_r, 280.789)
        with self.assertRaises(ValueError):
            note_treatment('converted', self.c, self.claims, 13.366)
        with self.assertRaises(ValueError):
            note_treatment('retained', self.c, self.claims)

    def test_earnout_rollforward_rejects_missing_addition(self):
        bad = copy.deepcopy(self.claims)
        bad['contingent_consideration']['acquisition_addition'] = 0
        with self.assertRaises(ValueError):
            reconcile_claims(bad, self.cash)

    def test_claims_do_not_subtract_undrawn_commitment_or_operating_leases(self):
        v = reconcile_claims(self.claims, self.cash)
        self.assertAlmostEqual(v['deductions_total_m'], 43.71472928176795)
        self.assertGreater(v['note_conversion_parity_diagnostic_m'], 10*v['note_principal_reference_only_m'])


if __name__ == '__main__':
    unittest.main()
