import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from reverse_dcf import bounded_root, terminal_requirement, report, render
from three_statements import load_inputs, project
from valuation import assumptions, value
from equity_bridge import bridge, assumptions as bridge_assumptions


class ReverseTests(unittest.TestCase):
    def test_known_linear_roots_both_directions(self):
        self.assertAlmostEqual(bounded_root(lambda x:2*x+1,5,[0,4])['root'],2)
        self.assertAlmostEqual(bounded_root(lambda x:9-2*x,5,[0,4])['root'],2)

    def test_unbracketed_does_not_extrapolate(self):
        self.assertIsNone(bounded_root(lambda x:x+1,20,[0,4])['root'])

    def test_invalid_bounds_and_outputs(self):
        for bounds in ([2,1],[0,float('nan')]):
            with self.assertRaises(ValueError): bounded_root(lambda x:x,1,bounds)
        with self.assertRaises(ValueError): bounded_root(lambda x:float('inf'),1,[0,2])
        with self.assertRaises(ValueError): bounded_root(lambda x:(x-1)**2,1,[0,2])
        with self.assertRaises(ValueError): bounded_root(lambda x:1 if x<1 else 3,2,[0,2])

    def test_terminal_algebra_known_answer(self):
        # Equity 100 = operating EV 80 + net bridge 20; 10 shares, target 10.
        # Explicit PV 30 means terminal PV 50; year-one terminal 55 at 10%.
        v=dict(growth=.02,wacc=.10,enterprise_value=80,pv_explicit_fcff=30,
               transition=[dict(years_after_cutoff=1,revenue=100)],terminal=dict(fcff=4.4))
        b=dict(mode='converted',unallocated_claim_shortfall=0,equity=100,shares=10)
        r=terminal_requirement(v,b,10,.10,.25)
        self.assertAlmostEqual(r['required_terminal_value'],55)
        self.assertAlmostEqual(r['required_2041_fcff'],4.4)
        self.assertAlmostEqual(r['implied_2041_ebit_margin'],(4.4/.8/.75)/102)
        self.assertAlmostEqual(r['reconstructed_price'],10)

    def test_existing_forecast_round_trip_and_unchanged(self):
        inputs=load_inputs(); m=project(*inputs); a=assumptions(); original=copy.deepcopy(a)
        v=value(m,a); b=bridge(m,v,inputs[-1],bridge_assumptions())
        r=terminal_requirement(v,b,b['price'],.16,.25)
        self.assertAlmostEqual(r['required_2041_fcff'],v['terminal']['fcff'])
        self.assertAlmostEqual(r['implied_2041_ebit_margin'],.12)
        self.assertEqual(a,original)

    def test_terminal_rejects_invalid_economics(self):
        inputs=load_inputs(); m=project(*inputs); v=value(m,assumptions())
        b=bridge(m,v,inputs[-1],bridge_assumptions())
        for target,roic,tax in [(0,.16,.25),(float('nan'),.16,.25),(60,.02,.25),(60,.16,1)]:
            with self.assertRaises(ValueError): terminal_requirement(v,b,target,roic,tax)

    def test_integrated_price_reproduction_and_rate_comparison(self):
        r=report()
        for case,c in r['cases'].items():
            self.assertAlmostEqual(c['wacc_root']['reproduced_price'],r['target_price'],places=7)
            self.assertAlmostEqual(c['terminal_requirement']['reconstructed_price'],r['target_price'],places=7)
            self.assertIsNone(c['margin_root']['root'])
            self.assertTrue(c['terminal_requirement']['exceeds_100_percent_margin'])
        self.assertLess(r['cases']['base']['wacc_root']['root'],r['risk_free'])
        self.assertGreater(r['cases']['upside']['wacc_root']['root'],r['risk_free'])

    def test_visible_report_preserves_rate_distinction(self):
        text=render(report())
        self.assertIn('The root is below Treasury.',text)
        self.assertIn('The root is only slightly above Treasury.',text)


if __name__=='__main__': unittest.main()
