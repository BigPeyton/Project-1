import copy
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from three_statements import load_inputs, project, FundingGap
from valuation import assumptions, discount_rate, terminal_value, discounted_value, transition, value


class ValuationTests(unittest.TestCase):
    def setUp(self):
        self.inputs=load_inputs()
        self.model=project(*self.inputs)
        self.a=assumptions()

    def test_official_lab05_known_answer(self):
        # Published source: course lessons/week-03/lab-05-dcf-build.md.
        # Training provides FCFF after reinvestment; NOPAT conversion below
        # simply makes the same terminal helper receive that specified FCFF.
        cash=100; schedule=[]
        for year,growth in enumerate([.08,.06,.05,.04,.03],1):
            cash*=1+growth
            schedule.append(dict(fcff=cash,years_after_cutoff=year))
        tv=terminal_value(cash*1.03/(1-.03/.15),.03,.15,.10)
        r=discounted_value(schedule,tv['value'],5,.10)
        actual=[x['fcff'] for x in schedule]+[r['pv_explicit_fcff'],tv['value'],r['pv_terminal'],
                r['enterprise_value'],r['enterprise_value']+50-300,
                (r['enterprise_value']+50-300)/50,r['terminal_share']]
        expected=[108,114.48,120.204,125.0122,128.7625,448.4408,1894.6486,
                  1176.4277,1624.8685,1374.8685,27.4974,.7240]
        for got,want in zip(actual,expected):
            self.assertAlmostEqual(got,want,delta=.0001)

    def test_wacc_market_weight_and_old_erp_comparison(self):
        d=discount_rate(self.model,self.inputs[-1],self.a)
        self.assertAlmostEqual(d['cost_of_equity'],.156354)
        self.assertLess(d['debt_weight'],.001)
        self.assertLess(d['calculated_wacc'],d['cost_of_equity'])
        changed=copy.deepcopy(self.a); changed['discount_rate']['equity_risk_premium']=.05
        self.assertGreater(discount_rate(self.model,self.inputs[-1],changed)['calculated_wacc'],d['calculated_wacc'])

    def test_no_pre_cutoff_flows_or_duplicate_years(self):
        r=value(self.model,self.a)
        self.assertEqual(r['schedule'][:6],self.model['future_fcff_schedule'])
        self.assertEqual([x['year'] for x in r['transition']],list(range(2031,2041)))
        self.assertGreater(r['schedule'][0]['years_after_cutoff'],0)

    def test_terminal_continuity_and_paid_growth(self):
        for case in ('base','upside'):
            r=value(project(*self.inputs,case=case),self.a,case)
            last=r['transition'][-1]; tv=r['terminal']
            self.assertAlmostEqual(tv['fcff'],last['fcff']*1.03)
            self.assertAlmostEqual(tv['reinvestment'],tv['nopat']*.03/self.a['cases'][case]['mature_incremental_roic'])
            self.assertGreater(tv['reinvestment'],0)

    def test_negative_2030_is_preserved_and_base_not_floored(self):
        self.assertLess(self.model['annual'][-1]['fcff'],0)
        r=value(self.model,self.a)
        self.assertLess(r['enterprise_value'],0)
        self.assertIsNone(r['terminal_share'])
        self.assertEqual(next(x['year'] for x in r['transition'] if x['fcff']>0),2034)

    def test_terminal_boundary_nonfinite_and_negative_profit_fail(self):
        for args in [(100,.16,.20,.16),(100,.03,.03,.16),(-100,.03,.16,.16),
                     (100,-.01,.16,.16),(100,.03,.16,float('nan'))]:
            with self.assertRaises(ValueError): terminal_value(*args)

    def test_invalid_cashflow_dates_fail(self):
        for schedule in [[dict(fcff=10,years_after_cutoff=0)],
                         [dict(fcff=10,years_after_cutoff=2)],
                         [dict(fcff=float('nan'),years_after_cutoff=1)],
                         [dict(fcff=10,years_after_cutoff=1)]*2]:
            with self.assertRaises(ValueError): discounted_value(schedule,100,1,.16)

    def test_wacc_direction_on_selected_domain(self):
        for case in ('base','upside'):
            m=project(*self.inputs,case=case)
            for g in [.02,.03,.04]:
                values=[value(m,self.a,case,wacc=w,growth=g)['enterprise_value'] for w in [.14,.16,.18,.20]]
                self.assertTrue(all(x>y for x,y in zip(values,values[1:])))

    def test_growth_direction_depends_on_economic_returns(self):
        # At 14% WACC, 16% return growth creates value; at 20%, it destroys value.
        for w,direction in [(.14,1),(.20,-1)]:
            lo=value(self.model,self.a,wacc=w,growth=.02)['enterprise_value']
            hi=value(self.model,self.a,wacc=w,growth=.04)['enterprise_value']
            self.assertGreater((hi-lo)*direction,0)

    def test_capital_overrun_reduces_value(self):
        changed=copy.deepcopy(self.a)
        changed['cases']['base']['mature_incremental_roic']=.10
        self.assertLess(value(self.model,changed)['enterprise_value'],value(self.model,self.a)['enterprise_value'])

    def test_margin_shortfall_reduces_value(self):
        changed=copy.deepcopy(self.a)
        changed['cases']['base']['mature_ebit_margin']=.08
        self.assertLess(value(self.model,changed)['enterprise_value'],value(self.model,self.a)['enterprise_value'])

    def test_downside_funding_cannot_be_bypassed(self):
        with self.assertRaises(FundingGap): project(*self.inputs,case='downside')
        funded=project(*self.inputs,case='downside',allow_equity=True)
        with self.assertRaises(ValueError): transition(funded,self.a,'base')

    def test_no_silent_input_mutation(self):
        original=copy.deepcopy((self.model,self.a))
        value(self.model,self.a)
        self.assertEqual(original,(self.model,self.a))

    def test_wacc_override_controls_all_validation(self):
        reference=value(self.model,self.a,wacc=.16)
        self.a['discount_rate']['selected_wacc']=.02
        # Recovery from an invalid default must work when the supplied rate is valid.
        self.assertEqual(value(self.model,self.a,wacc=.16),reference)
        with self.assertRaises(ValueError): value(self.model,self.a)
        self.a['discount_rate']['selected_wacc']=.16
        with self.assertRaises(ValueError): value(self.model,self.a,wacc=.02)

    def test_mixed_scenarios_fail(self):
        with self.assertRaisesRegex(ValueError,'scenario.*match'):
            value(self.model,self.a,case='upside')

    def test_nonfinite_terminal_values_and_dates_fail(self):
        schedule=[dict(fcff=10,years_after_cutoff=1)]
        for bad in (float('nan'),float('inf'),-float('inf')):
            with self.assertRaises(ValueError): discounted_value(schedule,bad,1,.16)
            with self.assertRaises(ValueError): discounted_value(schedule,100,bad,.16)


if __name__=='__main__':
    unittest.main()
