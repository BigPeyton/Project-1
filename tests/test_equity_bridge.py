import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from three_statements import load_inputs,project
from valuation import value,assumptions as va
from equity_bridge import assumptions,bridge,allocation,present_value,straight_debt_floor,report


class EquityBridgeTests(unittest.TestCase):
    def setUp(self):
        self.inputs=load_inputs(); self.cap=self.inputs[-1]; self.a=assumptions()
        self.m=project(*self.inputs); self.v=value(self.m,va())

    def run_bridge(self,**kw):
        return bridge(self.m,self.v,self.cap,self.a,**kw)

    def test_integrated_numerator_and_share_count(self):
        r=self.run_bridge()
        self.assertAlmostEqual(sum(r['lines'].values()),r['equity'])
        self.assertAlmostEqual(r['price']*r['shares'],r['equity'])
        self.assertAlmostEqual(r['shares'],655.006167)
        self.assertAlmostEqual(r['lines']['cutoff_cash'],self.m['cutoff_balance_sheet']['cash'])
        self.assertNotIn('goodwill',r['lines'])
        self.assertNotIn('capex_payable',r['lines'])
        self.assertNotIn('operating_lease_noncurrent',r['lines'])

    def test_known_option_cash_not_added_twice(self):
        r=self.run_bridge()
        known=self.cap['known_september_exercise']['exercise_proceeds_usd']/1e6
        total=self.cap['derived_scenarios']['gross_option_exercise_proceeds_usd']/1e6
        self.assertAlmostEqual(r['option_receipts']+known,total)
        no=self.run_bridge(option_mode='unexercised')
        self.assertAlmostEqual(r['equity']-no['equity'],r['option_receipts'])
        self.assertAlmostEqual(r['shares']-no['shares'],r['option_shares'])

    def test_note_claim_and_conversion_exclusive(self):
        with self.assertRaises(ValueError): self.run_bridge(mode='converted',claim=20)
        with self.assertRaises(ValueError): self.run_bridge(mode='retained')
        conv=self.run_bridge(); ret=self.run_bridge(mode='retained',claim=100)
        self.assertAlmostEqual(conv['shares']-ret['shares'],2.607745)
        self.assertAlmostEqual(conv['equity']-ret['equity'],100)

    def test_cash_change_has_dollar_for_dollar_effect(self):
        r=self.run_bridge(); m=copy.deepcopy(self.m)
        m['cutoff_bridge_inputs']['cash']+=100
        changed=bridge(m,self.v,self.cap,self.a)
        self.assertAlmostEqual(changed['equity']-r['equity'],100)
        self.assertAlmostEqual(changed['price']-r['price'],100/r['shares'])

    def test_payment_before_cutoff_removes_cash_and_claim_once(self):
        m=copy.deepcopy(self.m); amount=m['cutoff_balance_sheet']['seller_payable']
        m['cutoff_balance_sheet']['seller_payable']=0
        m['cutoff_bridge_inputs']['claims_except_notes']-=amount
        m['cutoff_bridge_inputs']['cash']-=amount
        self.assertAlmostEqual(bridge(m,self.v,self.cap,self.a)['price'],self.run_bridge()['price'])

    def test_financing_must_pair_cash_and_shares(self):
        for kw in ({'new_cash':100},{'new_shares':10}):
            with self.assertRaises(ValueError): self.run_bridge(**kw)
        r=self.run_bridge(new_cash=100,new_shares=10); base=self.run_bridge()
        self.assertAlmostEqual(r['equity']-base['equity'],100)
        self.assertAlmostEqual(r['shares']-base['shares'],10)

    def test_fair_price_issuance_neutral_before_fees(self):
        r=self.run_bridge(); gross=100; new_shares=gross/r['price']
        neutral=self.run_bridge(new_cash=gross,new_shares=new_shares)
        self.assertAlmostEqual(neutral['price'],r['price'])
        fees=self.run_bridge(new_cash=gross*.98,new_shares=new_shares)
        self.assertLess(fees['price'],r['price'])

    def test_future_cash_is_discounted_but_shares_are_not(self):
        pv=present_value(474,'2028-04-30',self.a['cutoff'],.16)
        self.assertLess(pv,474)
        base=self.run_bridge(); r=self.run_bridge(new_cash=pv,new_shares=7.4512)
        self.assertAlmostEqual(r['equity']-base['equity'],pv)
        self.assertAlmostEqual(r['shares']-base['shares'],7.4512)
        with self.assertRaises(ValueError): present_value(10,'2026-01-01',self.a['cutoff'],.16)

    def test_customer_recovery_and_reserve_direction(self):
        r=self.run_bridge()
        recovery=self.run_bridge(customer_recovery=32.15)
        self.assertAlmostEqual(recovery['equity']-r['equity'],32.15)
        self.assertLess(self.run_bridge(reserve=300)['price'],r['price'])
        with self.assertRaises(ValueError): self.run_bridge(customer_recovery=100)

    def test_intrinsic_note_and_option_election(self):
        base=self.run_bridge(mode='intrinsic_only',option_mode='intrinsic')
        self.assertFalse(base['note_conversion'])
        self.assertAlmostEqual(base['note_claim'],straight_debt_floor(self.cap,self.a))
        m=project(*self.inputs,case='upside'); v=value(m,va(),'upside')
        up=bridge(m,v,self.cap,self.a,mode='intrinsic_only',option_mode='intrinsic')
        self.assertTrue(up['note_conversion']); self.assertEqual(up['note_claim'],0)
        small=allocation(100,self.cap,'intrinsic_only',option_mode='intrinsic',floor=13)
        self.assertEqual(small['option_receipts'],0); self.assertEqual(small['option_shares'],0)

    def test_limited_liability_displays_shortfall(self):
        r=allocation(5,self.cap,'intrinsic_only',option_mode='intrinsic',floor=13)
        self.assertEqual(r['price'],0)
        self.assertEqual(r['residual_before_limited_liability'],-8)
        self.assertEqual(r['unallocated_claim_shortfall'],8)

    def test_mismatch_and_conditional_funding_rejected(self):
        wrong=dict(self.v,case='upside')
        with self.assertRaises(ValueError): bridge(self.m,wrong,self.cap,self.a)
        bad=dict(self.m,total_net_equity_raised=100)
        with self.assertRaises(ValueError): bridge(bad,self.v,self.cap,self.a)

    def test_bad_amounts_fail(self):
        for amount in (-1,float('nan'),float('inf')):
            with self.assertRaises(ValueError): self.run_bridge(mode='retained',claim=amount)
            with self.assertRaises(ValueError): self.run_bridge(capped_credit=amount)

    def test_claim_reconciliation_and_input_preservation(self):
        original=copy.deepcopy((self.m,self.v,self.cap,self.a))
        self.run_bridge()
        self.assertEqual(original,(self.m,self.v,self.cap,self.a))
        self.m['cutoff_bridge_inputs']['claims_except_notes']+=1
        with self.assertRaises(ValueError): self.run_bridge()


if __name__=='__main__': unittest.main()
