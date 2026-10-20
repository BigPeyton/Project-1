import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from three_statements import load_inputs,project
from proforma_sensitivity import apply_drivers,evaluate,report
from app import calculate,response_for


class OperatingSensitivityTests(unittest.TestCase):
    def test_defaults_preserve_model_and_source(self):
        raw=load_inputs(); original=copy.deepcopy(raw); changed,_=apply_drivers(raw,'base',{})
        self.assertEqual(changed,raw); self.assertEqual(raw,original)
        self.assertEqual(project(*changed),project(*raw))

    def test_rd_change_known_ebit_effect_and_no_historical_change(self):
        base=evaluate(); changed=evaluate({'rd_scale':110})
        # Extra 10% of the $390m 2030 budget reduces EBIT by exactly $39m.
        self.assertAlmostEqual(changed['metrics']['ebit_2030']-base['metrics']['ebit_2030'],-39)
        self.assertEqual(changed['annual'][0],base['annual'][0])
        self.assertEqual(changed['cutoff_cash'],base['cutoff_cash'])
        self.assertLess(changed['metrics']['fcff_2030'],base['metrics']['fcff_2030'])

    def test_growth_change_compounds_four_years_only(self):
        raw=load_inputs(); changed,_=apply_drivers(raw,'base',{'space_growth':5})
        self.assertEqual(raw[1]['cases']['base']['space_growth_2027_2030'],[.25,.22,.18,.15])
        for old,new in zip(raw[1]['cases']['base']['space_growth_2027_2030'],changed[1]['cases']['base']['space_growth_2027_2030']):
            self.assertAlmostEqual(new-old,.05)
        self.assertEqual(changed[1]['cases']['base']['q3_total'],raw[1]['cases']['base']['q3_total'])

    def test_neutron_scale_preserves_fixed_costs(self):
        raw=load_inputs(); changed,_=apply_drivers(raw,'base',{'neutron_scale':50})
        self.assertEqual(changed[3],raw[3]); self.assertEqual(changed[4],raw[4])
        self.assertEqual(changed[1]['cases']['base']['neutron_revenue_equivalents_2026_2030'],[0,.5,1.5,3,5])

    def test_bounds_fail_loudly(self):
        for params in ({'space_growth':6},{'space_margin':float('nan')},{'rd_scale':79},{'neutron_scale':151}):
            with self.assertRaises(ValueError): apply_drivers(load_inputs(),'base',params)
        self.assertEqual(response_for('/?rd_scale=79')[0],422)

    def test_rankings_use_actual_endpoint_spans_and_alternative_ranges(self):
        r=report()
        for group in r['ranges'].values():
            for c in group['cases']:
                self.assertIsNotNone(c['spans'])
                for key,span in c['spans'].items():
                    self.assertAlmostEqual(span,abs(c['outcomes'][1]['result']['metrics'][key]-c['outcomes'][0]['result']['metrics'][key]))
        self.assertTrue(any(r['ranking_changed'].values()))

    def test_app_operating_change_flows_through_all_statements_and_reset(self):
        base=calculate({}); changed=calculate({'rd_scale':'110'})
        self.assertAlmostEqual(changed['comparison']['ebit_2030']['change'],-39)
        self.assertLess(changed['model']['annual'][-1]['balance_sheet']['cash'],base['model']['annual'][-1]['balance_sheet']['cash'])
        self.assertLess(changed['comparison']['price']['change'],0)
        self.assertEqual(calculate({}),base)


if __name__=='__main__':unittest.main()
