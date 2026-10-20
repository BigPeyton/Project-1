import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from three_statements import (load_inputs, project, period, opening_balance, balance_gap,
                              check_period, FundingGap)


class StatementTests(unittest.TestCase):
    def setUp(self):
        self.a=load_inputs()

    def test_opening_reclassification_preserves_filing_and_inputs(self):
        original=copy.deepcopy(self.a[0])
        b=opening_balance(self.a[0],self.a[4])
        self.assertAlmostEqual(balance_gap(b),0)
        self.assertAlmostEqual(b['customer_financing'],32.15)
        self.assertAlmostEqual(b['ordinary_liabilities'],152.573)
        self.assertEqual(original,self.a[0])
        self.a[0]['h1_2026']['balance_sheet']['cash']+=1000
        with self.assertRaises(ValueError): opening_balance(self.a[0],self.a[4])

    def test_all_scenarios_balance_when_funding_is_explicit(self):
        for case in ('base','downside','upside'):
            r=project(*self.a,case=case,allow_equity=(case=='downside'))
            self.assertEqual(len(r['annual']),5)
            for row in r['annual']:
                self.assertAlmostEqual(balance_gap(row['balance_sheet']),0)
                end=row['opening_cash_including_restricted']+row['cfo']+row['cfi']+row['cff']+row['fx_cash']
                self.assertAlmostEqual(end,row['balance_sheet']['cash']+row['balance_sheet']['restricted_cash'])
                self.assertAlmostEqual(row['pretax_income']-row['tax_expense'],row['net_income'])

    def test_deliberate_cash_and_equity_corruption_fail(self):
        r=project(*self.a)
        for field in ('cash','equity'):
            bad=copy.deepcopy(r['periods'][0]); bad['balance_sheet'][field]+=1
            with self.assertRaises(ValueError): check_period(r['opening'],bad,200)

    def test_cutoff_partitions_future_flows_and_option_receipt(self):
        r=project(*self.a); q3,q4=r['periods'][:2]
        self.assertAlmostEqual(r['pre_cutoff_q3_fraction'],72/92)
        self.assertAlmostEqual(r['pre_cutoff_fcff']+r['remaining_q3_fcff'],q3['fcff'])
        self.assertAlmostEqual(r['annual'][0]['future_fcff'],r['remaining_q3_fcff']+q4['fcff'])
        self.assertAlmostEqual(r['cutoff_balance_sheet']['cash']+sum(r['post_cutoff_2026_cash_flow'].values()),q4['balance_sheet']['cash'])
        self.assertAlmostEqual(q3['option_receipts']+q4['option_receipts'],3.85649521)
        self.assertAlmostEqual(r['future_fcff_schedule'][0]['years_after_cutoff'],20/365)
        self.assertNotAlmostEqual(r['annual'][0]['future_fcff'],q3['fcff']+q4['fcff'])

    def test_unpaid_capex_does_not_create_a_second_asset(self):
        r=project(*self.a); q3,q4=r['periods'][:2]
        self.assertAlmostEqual(q4['cash_capex'],60+15.371)
        self.assertEqual(q4['balance_sheet']['capex_payable'],0)
        self.assertAlmostEqual(q4['balance_sheet']['ppe']-q3['balance_sheet']['ppe'],60-q4['depreciation_ppe'])

    def test_claim_settlement_is_not_a_second_fcff_deduction(self):
        result=project(*self.a); prior=result['periods'][0]['balance_sheet']; a=self.a[4]
        q4=result['periods'][1]
        op={k:q4[k] for k in ('total_revenue','gross_profit','cost_of_revenue','rd','sga','operating_income')}
        release=q4['contract_provision_release']
        op['gross_profit']-=release; op['cost_of_revenue']+=release; op['operating_income']-=release
        target={k:q4['balance_sheet'][k] for k in ('receivables','contract_assets','inventory','prepaids','ordinary_liabilities','contract_liabilities')}
        common=(prior,op,target,60,23.205/2,.25,'test',result['opening'],a)
        unpaid=period(*common,convert=True,settle=False)
        paid=period(*common,convert=True,settle=True)
        self.assertAlmostEqual(paid['cfo'],unpaid['cfo'])
        self.assertAlmostEqual(paid['fcff']-unpaid['fcff'],-15.371)
        self.assertAlmostEqual(paid['cff']-unpaid['cff'],-12.763-1.716)
        self.assertAlmostEqual(paid['net_income']-unpaid['net_income'],4.657)

    def test_customer_advance_reduction_consumes_cash(self):
        before=project(*self.a)['annual'][1]
        self.a[4]['cases']['base']['advance_revenue_ratio'][1]-=.01
        after=project(*self.a)['annual'][1]
        self.assertAlmostEqual(after['future_fcff']-before['future_fcff'],-.01*before['total_revenue'])
        self.assertEqual(after['operating_income'],before['operating_income'])

    def test_funding_failure_and_conditional_dilution_are_visible(self):
        with self.assertRaises(FundingGap) as caught: project(*self.a,case='downside')
        self.assertEqual(caught.exception.period,'2030')
        r=project(*self.a,case='downside',allow_equity=True)
        last=r['annual'][-1]
        self.assertAlmostEqual(last['balance_sheet']['cash'],200)
        self.assertAlmostEqual(last['net_equity_raised'],caught.exception.gap)
        self.assertAlmostEqual(last['new_funding_shares']*30.98*.98,last['net_equity_raised'])
        self.assertGreater(last['new_funding_shares'],0)

    def test_negative_fcff_preserved_even_when_accounting_profit_positive(self):
        r=project(*self.a)
        last=r['annual'][-1]
        self.assertGreater(last['net_income'],0)
        self.assertLess(last['future_fcff'],0)
        self.assertTrue(all(x['future_fcff']<0 for x in r['annual']))

    def test_cutoff_claims_exclude_items_already_in_fcff(self):
        r=project(*self.a); b=r['cutoff_balance_sheet']; bridge=r['cutoff_bridge_inputs']
        expected=b['other_debt']+b['finance_leases']+b['earnout']+b['financing_fee_payable']+b['seller_payable']
        self.assertAlmostEqual(bridge['claims_except_notes'],expected)
        self.assertEqual(bridge['converted_note_claim'],0)
        self.assertGreater(b['capex_payable'],0)
        self.assertAlmostEqual(bridge['cash'],b['cash'])

    def test_bad_paths_and_financing_inputs_fail(self):
        for change in ('nan','ratio','price'):
            a=copy.deepcopy(self.a)
            if change=='nan': a[4]['cases']['base']['ppe_additions'][0]=float('nan')
            elif change=='ratio': a[4]['cases']['base']['advance_revenue_ratio'][0]=36
            else: a[4]['common']['conditional_equity_price']=0
            with self.assertRaises(ValueError): project(*a)


if __name__=='__main__': unittest.main()
