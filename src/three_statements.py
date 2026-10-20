"""Linked standalone statements and signed FCFF, with explicit funding failure."""
import copy
import json
import math
from datetime import date
from pathlib import Path
from operating_forecast import load_inputs as load_operating, forecast as operating_forecast
from audit_reported_inputs import ASSETS as RAW_ASSETS, LIABILITIES as RAW_LIABILITIES

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ('cash securities receivables contract_assets inventory prepaids ppe intangibles '
          'goodwill rou_operating rou_finance restricted_cash deferred_tax_assets '
          'customer_financing other_noncurrent_assets').split()
LIABILITIES = ('ordinary_liabilities contract_liabilities notes other_debt finance_leases '
               'operating_lease_noncurrent deferred_tax_liabilities capex_payable '
               'contract_loss_provision earnout financing_fee_payable seller_payable').split()
WC_ASSETS = ('receivables', 'contract_assets', 'inventory', 'prepaids')
WC_LIABILITIES = ('ordinary_liabilities', 'contract_liabilities')
IS_KEYS = ('total_revenue cost_of_revenue gross_profit rd sga operating_income interest_income '
           'interest_expense other_income pretax_income tax_expense net_income').split()
FLOW_KEYS = ('depreciation amortization da cash_tax operating_cash_tax deferred_tax_expense '
             'debt_cost_amortization delta_wc contract_provision_release cfo '
             'new_capex old_capex_payment cash_capex security_sale claim_settlement '
             'cfi interest_cash debt_principal fees_paid option_receipts note_conversion '
             'net_equity_raised gross_equity_raised equity_issuance_fees new_funding_shares '
             'cff fcff').split()


class FundingGap(ValueError):
    def __init__(self, period, gap):
        self.period, self.gap = period, gap
        super().__init__(f'{period}: additional external funding of {gap:.3f} million required; no committed facility assumed.')


def load_inputs():
    return (*load_operating(), json.loads((ROOT/'data/statement_assumptions.json').read_text()),
            json.loads((ROOT/'data/capitalization.json').read_text()))


def near(a, b, label):
    if not math.isfinite(a) or not math.isfinite(b) or abs(a-b) > 1e-6:
        raise ValueError(f'{label}: {a} != {b}')


def balance_gap(bs):
    return sum(bs[k] for k in ASSETS)-sum(bs[k] for k in LIABILITIES)-bs['equity']


def check_balance(bs):
    if any(not math.isfinite(bs[k]) or bs[k] < -1e-8 for k in ASSETS+LIABILITIES):
        raise ValueError('Negative or nonfinite balance-sheet asset/liability.')
    near(balance_gap(bs), 0, 'Balance sheet fails')


def working_capital(bs):
    return sum(bs[k] for k in WC_ASSETS)-sum(bs[k] for k in WC_LIABILITIES)


def opening_balance(reported, a):
    raw = reported['h1_2026']['balance_sheet']
    for p in ('fy2025', 'h1_2026'):
        b = reported[p]['balance_sheet']
        near(sum(b[k] for k in RAW_ASSETS), b['total_assets'], p+' filing assets')
        near(sum(b[k] for k in RAW_LIABILITIES), b['total_liabilities'], p+' filing liabilities')
        near(b['total_assets'], b['total_liabilities']+b['equity'], p+' filing balance')
    b = {k:v/1000 for k,v in raw.items()}
    s, c = a['reported_supplement'], a['opening_classification']
    x = {k:b[k] for k in ('cash receivables contract_assets inventory ppe intangibles goodwill '
                          'rou_operating rou_finance restricted_cash deferred_tax_assets equity').split()}
    x.update(securities=b['securities_current']+b['securities_noncurrent'],
             prepaids=b['prepaids_other_current']-s['customer_financing_current'],
             customer_financing=s['customer_financing_current']+s['customer_financing_noncurrent'],
             other_noncurrent_assets=b['other_noncurrent_assets']-s['customer_financing_noncurrent'],
             contract_liabilities=b['contract_liabilities'], notes=b['convertible_notes_net'],
             other_debt=b['other_borrowings_net'],
             finance_leases=b['lease_finance_noncurrent']+c['finance_lease_current_estimate'],
             operating_lease_noncurrent=b['lease_operating_noncurrent'],
             deferred_tax_liabilities=b['deferred_tax_liabilities'],
             capex_payable=s['unpaid_capex'], contract_loss_provision=s['contract_loss_provision'],
             earnout=c['earnout'], financing_fee_payable=c['financing_fee_payable'], seller_payable=c['seller_payable'])
    pool=sum(b[k] for k in ('payables','accrued_expenses','employee_benefits','other_current_liabilities','other_noncurrent_liabilities'))
    x['ordinary_liabilities']=pool-(
        s['unpaid_capex']+s['contract_loss_provision']+c['finance_lease_current_estimate']+
        c['earnout']+c['financing_fee_payable']+c['seller_payable'])
    near(sum(x[k] for k in ASSETS), b['total_assets'], 'Reclassified opening assets')
    near(sum(x[k] for k in LIABILITIES), b['total_liabilities'], 'Reclassified opening liabilities')
    check_balance(x)
    return x


def validate(a, reported, case):
    if a['cutoff'] != reported['valuation_cutoff'] or a['source']['published'] >= a['cutoff'][:10]:
        raise ValueError('Statement cutoff/source mismatch.')
    for key, path in a['cases'][case].items():
        if len(path) != 5 or any(not math.isfinite(v) or v < 0 for v in path):
            raise ValueError('Invalid five-period path: '+key)
        if 'ratio' in key and any(v > 1 for v in path):
            raise ValueError('Ratios must use decimal fractions.')
    c=a['common']
    if any(not math.isfinite(v) or v < 0 for v in c.values()):
        raise ValueError('Invalid common assumption.')
    if c['conditional_equity_price'] <= 0 or not 0 <= c['conditional_equity_fee'] < 1 or c['deferred_tax_runoff_years'] <= 0:
        raise ValueError('Invalid financing or tax runoff assumption.')
    if any(c[k] > 1 for k in ('tax_rate','loss_year_cash_tax_revenue_rate','ppe_depreciation_rate','finance_rou_depreciation_rate')):
        raise ValueError('Invalid percentage units.')


def wc_target(op, a, case, i):
    c=a['cases'][case]
    sales,cost=op['total_revenue'],op['cost_of_revenue']
    return dict(receivables=sales*c['ar_days'][i]/365,
                contract_assets=sales*c['contract_asset_ratio'][i],
                inventory=cost*c['inventory_days'][i]/365,
                prepaids=sales*c['prepaid_ratio'][i],
                ordinary_liabilities=cost*c['ordinary_liability_cost_ratio'][i],
                contract_liabilities=sales*c['advance_revenue_ratio'][i])


def cash_tax(profit, sales, c):
    return max(max(profit,0)*c['tax_rate'], sales*c['loss_year_cash_tax_revenue_rate'])


def period(prior, op, target, additions, amort, duration, label, initial, a,
           *, convert=False, settle=False, settle_earnout=False, option_receipts=0, allow_equity=False):
    c=a['common']; s=a['reported_supplement']; bs=copy.deepcopy(prior)
    bs.update(target)
    r={k:op[k] for k in ('total_revenue','gross_profit','cost_of_revenue','rd','sga')}
    r.update({k:0.0 for k in FLOW_KEYS})
    r['period']=label
    r['core_operating_income']=op['operating_income']
    r['new_capex']=additions
    r['depreciation_ppe']=min(prior['ppe']+additions, c['ppe_depreciation_rate']*duration*(prior['ppe']+additions/2))
    r['depreciation_finance_rou']=min(prior['rou_finance'],c['finance_rou_depreciation_rate']*duration*prior['rou_finance'])
    r['depreciation']=r['depreciation_ppe']+r['depreciation_finance_rou']
    r['amortization']=min(amort,max(0,prior['intangibles']-s['indefinite_intangibles']))
    r['da']=r['depreciation']+r['amortization']
    bs['ppe']+=additions-r['depreciation_ppe']
    bs['rou_finance']-=r['depreciation_finance_rou']
    bs['intangibles']-=r['amortization']
    r['delta_wc']=working_capital(bs)-working_capital(prior)
    if settle:
        r['contract_provision_release']=prior['contract_loss_provision']
        bs['contract_loss_provision']=0.0
    r['gross_profit']+=r['contract_provision_release']
    r['cost_of_revenue']-=r['contract_provision_release']
    r['operating_income']=r['gross_profit']-r['rd']-r['sga']
    # Net book value conversion changes liability and equity, never cash or EBIT.
    r['note_conversion']=prior['notes'] if convert else 0.0
    coupon=0 if convert or prior['notes']==0 else s['notes_principal']*s['notes_coupon']*duration
    note_interest=0 if convert or prior['notes']==0 else prior['notes']*s['notes_effective_rate']*duration
    r['debt_cost_amortization']=note_interest-coupon
    bs['notes']+=r['debt_cost_amortization']-r['note_conversion']
    r['interest_cash']=coupon+duration*(prior['other_debt']*c['debt_interest_rate']+prior['finance_leases']*c['finance_lease_interest_rate'])
    r['interest_expense']=r['interest_cash']+r['debt_cost_amortization']
    r['interest_income']=duration*((prior['cash']+prior['securities'])*c['cash_yield']+prior['customer_financing']*c['customer_financing_yield'])
    r['other_income']=0.0
    r['pretax_income']=r['operating_income']+r['interest_income']-r['interest_expense']
    r['cash_tax']=cash_tax(r['pretax_income']-r['contract_provision_release'],r['total_revenue'],c)
    r['operating_cash_tax']=cash_tax(r['core_operating_income'],r['total_revenue'],c)
    for key in ('deferred_tax_assets','deferred_tax_liabilities'):
        bs[key]-=min(prior[key],initial[key]*duration/c['deferred_tax_runoff_years'])
    r['deferred_tax_expense']=(bs['deferred_tax_liabilities']-prior['deferred_tax_liabilities'])-(bs['deferred_tax_assets']-prior['deferred_tax_assets'])
    r['tax_expense']=r['cash_tax']+r['deferred_tax_expense']
    r['net_income']=r['pretax_income']-r['tax_expense']
    r['cfo']=r['net_income']+r['da']+r['deferred_tax_expense']+r['debt_cost_amortization']-r['delta_wc']-r['contract_provision_release']
    r['old_capex_payment']=prior['capex_payable'] if settle else 0.0
    bs['capex_payable']-=r['old_capex_payment']
    r['cash_capex']=additions+r['old_capex_payment']
    seller=prior['seller_payable'] if settle else 0.0
    earnout=prior['earnout'] if settle_earnout else 0.0
    bs['seller_payable']-=seller; bs['earnout']-=earnout
    r['claim_settlement']=seller+earnout
    r['fees_paid']=prior['financing_fee_payable'] if settle else 0.0
    bs['financing_fee_payable']-=r['fees_paid']
    other_principal=prior['other_debt'] if settle else 0.0
    lease_principal=min(prior['finance_leases'],c['annual_finance_lease_principal']*duration)
    bs['other_debt']-=other_principal; bs['finance_leases']-=lease_principal
    r['debt_principal']=other_principal+lease_principal
    r['option_receipts']=option_receipts
    r['cfi']=-r['cash_capex']-r['claim_settlement']
    r['cff']=option_receipts-r['debt_principal']-r['fees_paid']
    cash_before_funding=prior['cash']+r['cfo']+r['cfi']+r['cff']
    r['security_sale']=min(prior['securities'],max(0,c['cash_floor']-cash_before_funding))
    bs['securities']-=r['security_sale']; r['cfi']+=r['security_sale']
    gap=max(0,c['cash_floor']-cash_before_funding-r['security_sale'])
    if gap>1e-8 and not allow_equity:
        raise FundingGap(label,gap)
    if gap>0:
        r['net_equity_raised']=gap
        r['gross_equity_raised']=gap/(1-c['conditional_equity_fee'])
        r['equity_issuance_fees']=r['gross_equity_raised']-gap
        r['new_funding_shares']=r['gross_equity_raised']/c['conditional_equity_price']
        r['cff']+=gap
    bs['cash']=prior['cash']+r['cfo']+r['cfi']+r['cff']
    bs['equity']=prior['equity']+r['net_income']+r['note_conversion']+option_receipts+r['net_equity_raised']
    r['fcff']=r['core_operating_income']-r['operating_cash_tax']+r['da']-r['delta_wc']-r['cash_capex']
    r['balance_sheet']=bs
    check_period(prior,r,c['cash_floor'])
    return r


def check_period(prior,r,floor):
    bs=r['balance_sheet']; check_balance(bs)
    near(prior['cash']+r['cfo']+r['cfi']+r['cff'],bs['cash'],'Cash roll-forward')
    near(prior['equity']+r['net_income']+r['note_conversion']+r['option_receipts']+r['net_equity_raised'],bs['equity'],'Equity roll-forward')
    near(prior['ppe']+r['new_capex']-r['depreciation_ppe'],bs['ppe'],'PP&E roll-forward')
    near(prior['intangibles']-r['amortization'],bs['intangibles'],'Intangible roll-forward')
    near(r['total_revenue']-r['cost_of_revenue']-r['rd']-r['sga'],r['operating_income'],'Operating income')
    near(r['pretax_income']-r['tax_expense'],r['net_income'],'Net income')
    near(r['cfo']-r['cash_capex']-r['interest_income']+r['interest_cash']+r['cash_tax']-r['operating_cash_tax'],r['fcff'],'Levered CFO to FCFF')
    if bs['cash']<floor-1e-6:
        raise ValueError('Cash floor fails.')


def project(*inputs,case='base',allow_equity=False,end_year=2030):
    if type(end_year) is not int or not 2026<=end_year<=2030:
        raise ValueError('Statement end year must be 2026 through 2030.')
    reported,revenue,normalization,operating,a,capital=inputs
    validate(a,reported,case)
    ops=operating_forecast(reported,revenue,normalization,operating,case)
    initial=opening_balance(reported,a); prior=initial; rows=[]
    targets=wc_target(ops['annual'][0],a,case,0)
    q3targets={k:(prior[k]+v)/2 for k,v in targets.items()}
    known=capital['known_september_exercise']['exercise_proceeds_usd']/1e6
    q3=period(prior,ops['quarters_2026'][0],q3targets,a['cases'][case]['ppe_additions'][0]/2,
              a['reported_supplement']['remaining_2026_intangible_amortization']/2,.25,'2026 Q3',initial,a,option_receipts=known,allow_equity=allow_equity)
    if q3['net_equity_raised'] or q3['security_sale']:
        raise ValueError('Q3 funding event requires dated cash-flow split; cannot interpolate automatically.')
    weight=(date.fromisoformat(a['cutoff'][:10])-date(2026,6,30)).days/92
    if not 0<weight<1:
        raise ValueError('Cutoff must be inside Q3 for this stub convention.')
    cutoff_bs={k:initial[k]+weight*(q3['balance_sheet'][k]-initial[k]) for k in initial}
    # September 2 known exercise occurs wholly before the cutoff.
    cutoff_bs['cash']+=(1-weight)*known; cutoff_bs['equity']+=(1-weight)*known
    check_balance(cutoff_bs)
    pre_cff=q3['cff']*weight+(1-weight)*known
    near(initial['cash']+weight*(q3['cfo']+q3['cfi'])+pre_cff,cutoff_bs['cash'],'Cutoff cash bridge')
    prior=q3['balance_sheet']
    remaining_options=capital['derived_scenarios']['gross_option_exercise_proceeds_usd']/1e6-known
    q4=period(prior,ops['quarters_2026'][1],targets,a['cases'][case]['ppe_additions'][0]/2,
              a['reported_supplement']['remaining_2026_intangible_amortization']/2,.25,'2026 Q4',initial,a,
              convert=True,settle=True,option_receipts=remaining_options,allow_equity=allow_equity)
    # 2026 cash flow includes the actual first half, including restricted cash movements.
    hist=reported['h1_2026']; h=hist['income_statement']; cf=hist['cash_flow']
    annual={'year':2026,'balance_sheet':q4['balance_sheet']}
    hist_is=dict(total_revenue=h['revenue']/1000,cost_of_revenue=h['cost_of_revenue']/1000,
                 gross_profit=h['gross_profit']/1000,rd=h['rd']/1000,sga=h['sga']/1000,
                 operating_income=h['operating_income']/1000,interest_income=h['interest_income']/1000,
                 interest_expense=h['interest_expense']/1000,pretax_income=h['pretax_income']/1000,
                 tax_expense=h['tax_expense']/1000,net_income=h['net_income']/1000)
    hist_is['other_income']=hist_is['pretax_income']-hist_is['operating_income']-hist_is['interest_income']+hist_is['interest_expense']
    for k in IS_KEYS: annual[k]=hist_is[k]+q3[k]+q4[k]
    for k in ('cfo','cfi','cff'): annual[k]=cf[k]/1000+q3[k]+q4[k]
    annual['da']=cf['depreciation_amortization']/1000+q3['da']+q4['da']
    annual['sbc_addback']=cf['sbc']/1000
    annual['other_cfo_adjustments']=annual['cfo']-annual['net_income']-annual['da']-annual['sbc_addback']
    annual['cash_capex']=cf['capex_cash_outflow']/1000+q3['cash_capex']+q4['cash_capex']
    annual['fx_cash']=cf['fx_cash']/1000
    annual['opening_cash_including_restricted']=cf['cash_including_restricted_open']/1000
    annual['net_equity_raised']=q3['net_equity_raised']+q4['net_equity_raised']
    annual['new_funding_shares']=q3['new_funding_shares']+q4['new_funding_shares']
    annual['future_fcff']=(1-weight)*q3['fcff']+q4['fcff']
    annual['post_cutoff_only']=True
    near(annual['opening_cash_including_restricted']+annual['cfo']+annual['cfi']+annual['cff']+annual['fx_cash'],
         q4['balance_sheet']['cash']+q4['balance_sheet']['restricted_cash'],'FY2026 full cash statement')
    rows.append(annual); periods=[q3,q4]; prior=q4['balance_sheet']
    for i,op in enumerate(ops['annual'][1:],start=1):
        if op['year']>end_year: break
        r=period(prior,op,wc_target(op,a,case,i),a['cases'][case]['ppe_additions'][i],
                 a['reported_supplement']['intangible_amortization_2027_2030'][i-1],1,str(op['year']),initial,a,
                 settle_earnout=(i==1),allow_equity=allow_equity)
        r.update(year=op['year'],future_fcff=r['fcff'],post_cutoff_only=True,sbc_addback=0.0,
                 other_cfo_adjustments=r['cfo']-r['net_income']-r['da'],fx_cash=0.0,
                 opening_cash_including_restricted=prior['cash']+prior['restricted_cash'])
        rows.append(r); periods.append(r); prior=r['balance_sheet']
    future_q3_fcff=q3['fcff']*(1-weight)
    near(q3['fcff']*weight+future_q3_fcff,q3['fcff'],'Q3 FCFF timing partition')
    post_cash={k:(1-weight)*q3[k]+q4[k] for k in ('cfo','cfi','cff')}
    post_cash['cff']-=(1-weight)*known
    near(cutoff_bs['cash']+sum(post_cash.values()),q4['balance_sheet']['cash'],'Cutoff-to-year-end cash partition')
    cutoff_day=date.fromisoformat(a['cutoff'][:10])
    schedule=[dict(end='2026-09-30',fcff=future_q3_fcff),dict(end='2026-12-31',fcff=q4['fcff'])]
    schedule += [dict(end=str(r['year'])+'-12-31',fcff=r['future_fcff']) for r in rows[1:]]
    for entry in schedule:
        entry['years_after_cutoff']=(date.fromisoformat(entry['end'])-cutoff_day).days/365
    bridge=dict(cash=cutoff_bs['cash'],securities=cutoff_bs['securities'],
                operating_reserve=a['common']['cash_floor'],
                claims_except_notes=sum(cutoff_bs[k] for k in ('other_debt','finance_leases','earnout','financing_fee_payable','seller_payable')),
                customer_financing_book_reference=cutoff_bs['customer_financing'],
                remaining_hypothetical_option_receipts=remaining_options,
                note_book_value_reference_only=cutoff_bs['notes'],
                converted_note_claim=0.0)
    return dict(case=case,opening=initial,cutoff_balance_sheet=cutoff_bs,annual=rows,periods=periods,
                pre_cutoff_q3_fraction=weight,pre_cutoff_fcff=q3['fcff']*weight,
                remaining_q3_fcff=future_q3_fcff,post_cutoff_2026_cash_flow=post_cash,
                future_fcff_schedule=schedule,cutoff_bridge_inputs=bridge,conditional_funding=allow_equity,
                total_new_funding_shares=sum(r['new_funding_shares'] for r in rows),
                total_net_equity_raised=sum(r['net_equity_raised'] for r in rows))


def render(result):
    rows=result['annual']; b=result['cutoff_balance_sheet']
    lines=['# Linked three-statement forecast — '+result['case'],'',
           'USD millions. Analyst standalone scenarios, not reported future results. '
           'All five annual periods shown; 2026 combines reported H1 with projected H2. '
           'Conditional financing enabled: '+str(result['conditional_funding'])+'.','',
           '## Income statement','', '| Line | 2026 | 2027 | 2028 | 2029 | 2030 |','|---|---:|---:|---:|---:|---:|']
    for k in IS_KEYS:
        lines.append('| '+k.replace('_',' ')+' | '+' | '.join(f'{r[k]:,.3f}' for r in rows)+' |')
    lines+=['','## Balance sheet','', '| Line | 2026 | 2027 | 2028 | 2029 | 2030 |','|---|---:|---:|---:|---:|---:|']
    for k in ASSETS+['total_assets']+LIABILITIES+['total_liabilities','equity','balance_gap']:
        def val(r):
            bs=r['balance_sheet']
            if k=='total_assets': return sum(bs[x] for x in ASSETS)
            if k=='total_liabilities': return sum(bs[x] for x in LIABILITIES)
            if k=='balance_gap': return balance_gap(bs)
            return bs[k]
        lines.append('| '+k.replace('_',' ')+' | '+' | '.join(f'{val(r):,.3f}' for r in rows)+' |')
    lines+=['','## Cash flow and FCFF','', '| Line | 2026 | 2027 | 2028 | 2029 | 2030 |','|---|---:|---:|---:|---:|---:|']
    for k in ('net_income','da','sbc_addback','other_cfo_adjustments','cfo','cash_capex','cfi','cff','fx_cash','net_equity_raised','new_funding_shares','future_fcff'):
        label='FCFF AFTER SEPTEMBER 10 ONLY' if k=='future_fcff' else k.replace('_',' ')
        lines.append('| '+label+' | '+' | '.join(f'{r[k]:,.3f}' for r in rows)+' |')
    lines+=['','The 2026 CFO/CFI/CFF columns cover the full year; its FCFF row covers only remaining Q3 plus Q4. '
            'Do not discount full-year 2026 cash flow as if all of it follows the cutoff. Cash includes restricted cash only in the annual cash-flow roll-forward.','',
            '## Integrated September 10 estimate','',
            f'- Cash: {b["cash"]:,.6f}; marketable securities: {b["securities"]:,.6f}.',
            f'- Balance-sheet gap: {balance_gap(b):.9f}.',
            f'- Q3 fraction before cutoff: {result["pre_cutoff_q3_fraction"]:.9f} (72/92).',
            f'- Q3 FCFF before cutoff, excluded from future valuation: {result["pre_cutoff_fcff"]:,.6f}.',
            f'- Remaining Q3 FCFF: {result["remaining_q3_fcff"]:,.6f}.',
            f'- Total conditional equity raised, net: {result["total_net_equity_raised"]:,.6f}.',
            f'- Additional shares from conditional external funding, millions: {result["total_new_funding_shares"]:,.6f}.','',
            '## Future cash-flow dates','', '| Period end | Years after cutoff (actual/365) | FCFF |', '|---|---:|---:|']
    for entry in result['future_fcff_schedule']:
        lines.append(f'| {entry["end"]} | {entry["years_after_cutoff"]:.6f} | {entry["fcff"]:,.3f} |')
    lines+=['',
            'Every forecast period passed balance-sheet, cash, equity, asset-roll-forward, income and CFO-to-FCFF checks. '
            'This does not verify assumptions or replace the final cold run. No WACC, terminal value or final per-share valuation is produced here.','',
            'Detailed assumptions and limitations: data/statement_assumptions.json and docs/three-statements.md.']
    return '\n'.join(lines)+'\n'


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--case',choices=['base','downside','upside'],default='base')
    parser.add_argument('--allow-conditional-equity',action='store_true')
    args=parser.parse_args()
    print(render(project(*load_inputs(),case=args.case,allow_equity=args.allow_conditional_equity)),end='')
