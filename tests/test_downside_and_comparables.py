import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from three_statements import load_inputs,project,FundingGap
from downside_exit import assumptions,evaluate
from comparables import inputs,multiples,report


class DownsideTests(unittest.TestCase):
    def test_stop_before_failure_without_new_funding(self):
        r=evaluate()
        self.assertEqual(r['new_financing'],0)
        self.assertEqual(r['schedule'][-1]['end'],'2029-12-31')
        self.assertGreater(r['exit_cash_sufficiency'],0)
        with self.assertRaises(FundingGap): project(*load_inputs(),case='downside')

    def test_truncation_preserves_prior_cashflows(self):
        x=load_inputs(); full=project(*x,case='downside',allow_equity=True)
        stopped=project(*x,case='downside',end_year=2029)
        self.assertEqual(stopped['future_fcff_schedule'],full['future_fcff_schedule'][:-1])
        self.assertEqual(stopped['annual'],full['annual'][:-1])
        with self.assertRaises(ValueError): project(*x,end_year=2031)

    def test_recovery_and_closure_cost_direction(self):
        base=evaluate(); a=assumptions(); a['recoveries']['ppe']=.10
        self.assertLess(evaluate(a)['equity_if_converted']['price'],base['equity_if_converted']['price'])
        a=assumptions(); a['closure_cost']=250
        self.assertLess(evaluate(a)['equity_if_converted']['price'],base['equity_if_converted']['price'])

    def test_no_cash_double_recovery(self):
        a=assumptions(); a['recoveries']['cash']=1
        with self.assertRaises(ValueError): evaluate(a)

    def test_no_claim_double_settlement(self):
        a=assumptions(); a['settle_operating_liabilities'].append('finance_leases')
        with self.assertRaises(ValueError): evaluate(a)

    def test_insolvent_exit_fails_loudly(self):
        a=assumptions(); a['closure_cost']=1000
        with self.assertRaisesRegex(ValueError,'cannot pay'): evaluate(a)

    def test_reserve_release_and_option_warning(self):
        r=evaluate()
        self.assertAlmostEqual(r['terminal_exit_cashflow'],r['net_exit_recovery']+r['reserve_release'])
        self.assertFalse(r['equity_if_converted']['option_exercise_supported'])
        self.assertEqual(r['intrinsic_only_diagnostic']['option_receipts'],0)


class ComparableTests(unittest.TestCase):
    def test_equity_and_ev_definitions_reconcile(self):
        a=inputs(); rows=multiples(a)
        for p,r in zip(a['peers'],rows):
            self.assertAlmostEqual(r['equity'],p['price']*p['shares_m'])
            self.assertAlmostEqual(r['ev']-r['equity'],sum(p['claims'].values())-p['cash']-p['liquid_investments'])
            self.assertAlmostEqual(r['price_sales']*p['revenue'],r['equity'])
            self.assertAlmostEqual(r['ev_sales']*p['revenue'],r['ev'])

    def test_currency_scale_invariance(self):
        a=inputs(); before=multiples(a); p=a['peers'][1]
        for k in ('price','revenue','reported_operating_income','cash','liquid_investments'): p[k]*=2
        p['claims']={k:v*2 for k,v in p['claims'].items()}
        after=multiples(a)
        self.assertAlmostEqual(before[1]['ev_sales'],after[1]['ev_sales'])
        self.assertAlmostEqual(before[1]['price_sales'],after[1]['price_sales'])

    def test_no_future_same_day_unknown_or_currency_mismatch(self):
        for field,bad in [('published','2026-09-11'),('published','2026-09-10'),
                          ('published','2026-09-10T23:00:00+02:00'),
                          ('financial_currency','GBP'),('revenue_period','2026-06-30'),('price_date','2026-09-11')]:
            a=inputs(); a['peers'][1][field]=bad
            with self.assertRaises(ValueError): multiples(a)
        self.assertEqual(len(multiples(inputs())),2)  # verified 16:45 CEST is before 4 PM ET

    def test_duplicates_bad_denominator_and_treasury_shares(self):
        a=inputs(); a['peers'].append(copy.deepcopy(a['peers'][0]))
        with self.assertRaises(ValueError): multiples(a)
        for bad in (0,-1,float('nan')):
            a=inputs(); a['peers'][0]['revenue']=bad
            with self.assertRaises(ValueError): multiples(a)
        a=inputs(); a['peers'][1]['shares_m']=a['peers'][1]['issued_shares']/1e6
        with self.assertRaises(ValueError): multiples(a)

    def test_ps_does_not_receive_a_second_cash_bridge(self):
        r=report()
        for peer,x in zip(r['peers'],r['indications']):
            self.assertAlmostEqual(x['ps_method_price_basic_equivalent'],peer['price_sales']*r['target_sales']/r['target_basic_equivalent_shares'])

    def test_leave_one_out_does_not_invent_a_range(self):
        r=report()
        self.assertTrue(all(len(x['remaining'])==1 for x in r['leave_one_out']))
        a=inputs(); a['peers']=[]
        self.assertEqual(report(a)['indications'],[])

    def test_less_excess_peer_cash_increases_ev_not_ps(self):
        a=inputs(); base=multiples(a); a['peers'][0]['cash']/=2; changed=multiples(a)
        self.assertGreater(changed[0]['ev_sales'],base[0]['ev_sales'])
        self.assertEqual(changed[0]['price_sales'],base[0]['price_sales'])


if __name__=='__main__': unittest.main()
