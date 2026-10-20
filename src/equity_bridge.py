"""Integrated standalone equity allocation and clearly labeled instrument sensitivities."""
import json
import math
from datetime import date
from pathlib import Path
from three_statements import load_inputs, project
from valuation import assumptions as valuation_assumptions, value

ROOT=Path(__file__).resolve().parents[1]


def assumptions():
    return json.loads((ROOT/'data/equity_bridge_assumptions.json').read_text())


def nonnegative(**items):
    if any(not math.isfinite(x) or x<0 for x in items.values()):
        raise ValueError('Amounts must be finite and nonnegative: '+', '.join(items))


def present_value(amount, settlement, cutoff, rate):
    nonnegative(amount=amount,rate=rate)
    years=(date.fromisoformat(settlement)-date.fromisoformat(cutoff)).days/365
    if years<0: raise ValueError('Settlement precedes cutoff; use actual cutoff cash instead.')
    return amount/(1+rate)**years


def straight_debt_floor(capital,a):
    p=capital['remaining_notes']['principal_usd_millions_at_june_30']
    n=a['notes']; coupon=p*n['coupon_rate']/2
    return sum(present_value(coupon+(p if d==n['maturity'] else 0),d,a['cutoff'],n['straight_debt_discount_rate'])
               for d in n['remaining_payment_dates'])


def allocation(available,capital,mode,claim=None,option_mode='exercise',floor=None):
    """Allocate equity before existing options and notes, in USD/share.

    intrinsic_only solves common price + option intrinsic + note floor/parity;
    it deliberately does not price either instrument's time value.
    """
    if not math.isfinite(available): raise ValueError('Nonfinite available equity.')
    if option_mode not in ('exercise','unexercised','intrinsic'):
        raise ValueError('Unsupported option mode.')
    c=capital['august_7_reported']; known=capital['known_september_exercise']
    ordinary=(c['common_outstanding']+c['preferred_conversion_shares']+known['shares']+c['rsus'])/1e6
    options=(c['options']-known['shares'])/1e6
    strike=c['option_weighted_average_strike_usd']
    note_shares=capital['remaining_notes']['conversion_shares']/1e6
    # Additional participating shares are supplied in the copy used for a sensitivity.
    ordinary+=capital.get('scenario_new_shares_m',0)
    nonnegative(ordinary=ordinary,options=options,strike=strike,note_shares=note_shares)
    if ordinary<=0: raise ValueError('Positive ordinary share count required.')
    if mode=='converted':
        if claim not in (None,0): raise ValueError('Conversion shares and retained note claim cannot coexist.')
        deduction=0; converted=True
    elif mode=='retained':
        if claim is None: raise ValueError('Retained notes require an explicit economic claim.')
        nonnegative(claim=claim); deduction=claim; converted=False
    elif mode=='intrinsic_only':
        if floor is None or claim is not None or option_mode!='intrinsic':
            raise ValueError('Intrinsic diagnostic requires a debt floor, intrinsic options and no separate claim.')
        nonnegative(floor=floor)
        if available<=floor:
            return dict(mode=mode,equity=0,shares=ordinary,price=0,note_claim=floor,
                        note_conversion=False,option_receipts=0,option_shares=0,
                        residual_before_limited_liability=available-floor,conversion_supported=False,
                        option_exercise_supported=False,unallocated_claim_shortfall=floor-available)
        lo,hi=0,available/ordinary
        for _ in range(150):
            p=(lo+hi)/2
            used=ordinary*p+options*max(p-strike,0)+max(floor,note_shares*p)
            if used>available: hi=p
            else: lo=p
        p=(lo+hi)/2
        converted=note_shares*p>=floor
        deduction=0 if converted else floor
        option_mode='exercise' if p>strike else 'unexercised'
    else:
        raise ValueError('Unsupported note treatment.')
    if option_mode=='intrinsic':
        raise ValueError('Intrinsic option election belongs to the intrinsic-only diagnostic.')
    opt_shares=options if option_mode=='exercise' else 0
    receipts=opt_shares*strike
    shares=ordinary+opt_shares+(note_shares if converted else 0)
    residual=available+receipts-deduction
    equity=max(residual,0); price=equity/shares
    threshold=capital['remaining_notes']['principal_usd_millions_at_june_30']/note_shares
    return dict(mode=mode,equity=equity,shares=shares,price=price,note_claim=deduction,
                note_conversion=converted,option_receipts=receipts,option_shares=opt_shares,
                residual_before_limited_liability=residual,unallocated_claim_shortfall=max(-residual,0),
                conversion_supported=price>=threshold,option_exercise_supported=price>=strike)


def bridge(model,valuation,capital,a,*,mode='converted',claim=None,option_mode='exercise',
           reserve=None,customer_recovery=0,capped_credit=0,new_cash=0,new_shares=0):
    if model['case']!=valuation['case']: raise ValueError('Operating and statement scenarios must match.')
    if model['total_net_equity_raised']>0:
        raise ValueError('Conditional financing needs an explicit funding/ownership valuation.')
    b=model['cutoff_bridge_inputs']; bs=model['cutoff_balance_sheet']
    reserve=b['operating_reserve'] if reserve is None else reserve
    nonnegative(reserve=reserve,customer_recovery=customer_recovery,capped_credit=capped_credit,
                new_cash=new_cash,new_shares=new_shares)
    if (new_cash>0)!=(new_shares>0): raise ValueError('Financing cash and shares must be paired.')
    if customer_recovery>b['customer_financing_book_reference']:
        raise ValueError('This recovery sensitivity is bounded at the disclosed book reference.')
    claim_lines={k:bs[k] for k in ('other_debt','finance_leases','earnout','financing_fee_payable','seller_payable')}
    if abs(sum(claim_lines.values())-b['claims_except_notes'])>1e-8:
        raise ValueError('Integrated claims do not reconcile.')
    lines=dict(operating_value=valuation['enterprise_value'],cutoff_cash=b['cash'],securities=b['securities'],
               operating_cash_reserve=-reserve,customer_financing=customer_recovery,capped_calls=capped_credit,
               new_financing_cash_pv=new_cash)
    lines.update({k:-v for k,v in claim_lines.items()})
    available=sum(lines.values())
    cap=dict(capital,scenario_new_shares_m=new_shares)
    result=allocation(available,cap,mode,claim,option_mode,
                      straight_debt_floor(capital,a) if mode=='intrinsic_only' else None)
    lines['remaining_option_receipts']=result['option_receipts']
    lines['retained_note_claim']=-result['note_claim']
    if abs(sum(lines.values())-result['residual_before_limited_liability'])>1e-7:
        raise ValueError('Enterprise-equity bridge fails.')
    return dict(case=model['case'],lines=lines,**result)


def report():
    inputs=load_inputs(); cap=inputs[-1]; a=assumptions(); va=valuation_assumptions()
    cases={}; sensitivities=[]
    for case in ('base','upside'):
        m=project(*inputs,case=case); v=value(m,va,case)
        branches={
            'if_converted':bridge(m,v,cap,a),
            'retained_at_quote_parity':bridge(m,v,cap,a,mode='retained',claim=cap['remaining_notes']['conversion_shares']/1e6*va['discount_rate']['reference_price']),
            'retained_at_stale_june_fair_value':bridge(m,v,cap,a,mode='retained',claim=cap['derived_scenarios']['retained_case_note_fair_value_june_usd_millions']),
            'intrinsic_only_diagnostic':bridge(m,v,cap,a,mode='intrinsic_only',option_mode='intrinsic')}
        cases[case]=branches
        # All instrument sensitivities hold the if-converted operating case fixed.
        def add(label,**kwargs):
            r=bridge(m,v,cap,a,**kwargs)
            sensitivities.append(dict(case=case,label=label,price=r['price'],shares=r['shares'],
                                      net_adjustment_to_reference=r['equity']-branches['if_converted']['equity']))
        add('no remaining option exercise',option_mode='unexercised')
        for reserve in (100,300): add(f'operating reserve {reserve}',reserve=reserve)
        add('customer loan book recovery',customer_recovery=m['cutoff_bridge_inputs']['customer_financing_book_reference'])
        cc=a['capped_call']
        add('capped call maximum payoff, discounted',capped_credit=present_value(cc['maximum_payoff'],cc['assumed_settlement'],a['cutoff'],cc['discount_rate']))
        f=a['forward']
        for label in ('minimum_proceeds','maximum_proceeds'):
            add('forward '+label,new_cash=present_value(f[label],f['assumed_settlement'],a['cutoff'],f['discount_rate']),
                new_shares=cap['other_capital_items']['existing_forward_max_shares']/1e6)
        atm=a['atm']
        for price in atm['illustrative_issue_prices']:
            add(f'hypothetical full ATM at {price}',new_cash=atm['gross_capacity']*(1-atm['fee_rate']),new_shares=atm['gross_capacity']/price)
    base=project(*inputs); grid=[]
    for w in va['discount_rate']['wacc_grid']:
        for g in va['discount_rate']['terminal_growth_grid']:
            r=bridge(base,value(base,va,wacc=w,growth=g),cap,a)
            grid.append(dict(wacc=w,growth=g,price=r['price']))
    return dict(cases=cases,sensitivities=sensitivities,grid=grid,
                straight_debt_floor_diagnostic=straight_debt_floor(cap,a),
                status='Working standalone instrument sensitivities. The separate downside-exit, comparables and committee memo provide the conditional range/action; instrument and transaction qualifications remain.')


def render(r):
    lines=['# Working enterprise-to-equity bridge','',r['status'],'',
           'USD millions / million shares; prices USD per share. Reference excludes customer-loan recovery, capped-call credit, forward settlement and unverified additional ATM issuance. '
           'Pending Iridium operations and transaction funding/consideration are excluded together. These omissions limit comparison with market price.','',
           '| Case / instrument treatment | Equity | Shares | Per share | Model value supports conversion at principal threshold? |',
           '|---|---:|---:|---:|---|']
    for case,branches in r['cases'].items():
        for name,b in branches.items():
            lines.append(f'| {case}: {name} | {b["equity"]:,.3f} | {b["shares"]:,.6f} | {b["price"]:.4f} | {b["conversion_supported"]} |')
    lines+=['','Retained quote parity is not a note quote; June fair value is stale. The intrinsic-only diagnostic uses a '
            f'{r["straight_debt_floor_diagnostic"]:.6f} straight-debt floor and conversion parity, omitting option time value and detailed terms. '
            'It is NOT a market fair-value estimate. Base if-converted results are conditional on conversion, not an automatic economic election.','',
            '## Reference bridge detail','', '| Row | Base | Upside |','|---|---:|---:|']
    for k in r['cases']['base']['if_converted']['lines']:
        lo=r['cases']['base']['if_converted']['lines'][k]; hi=r['cases']['upside']['if_converted']['lines'][k]
        lines.append(f'| {k} | {lo:,.6f} | {hi:,.6f} |')
    lines+=['','## One change at a time, relative to if-converted reference','',
            '| Case | Change | Per share | Shares | Equity adjustment |','|---|---|---:|---:|---:|']
    for x in r['sensitivities']:
        lines.append(f'| {x["case"]} | {x["label"]} | {x["price"]:.4f} | {x["shares"]:,.6f} | {x["net_adjustment_to_reference"]:,.3f} |')
    lines+=['','Future forward cash is discounted; full new share participation is counted now. ATM cases are hypothetical immediate financing '
            'at specified prices, not verified completed transactions. These are not probabilities or an independently defensible high/low valuation range.','',
            '## Base if-converted WACC-growth sensitivity','', '| WACC | Growth | Per share |','|---|---:|---:|']
    for x in r['grid']: lines.append(f'| {x["wacc"]:.0%} | {x["growth"]:.0%} | {x["price"]:.4f} |')
    lines+=['','Continuing downside still fails funding; the separate downside-exit report values a conditional alternative. See the committee memo for WATCH/DEFER, with transaction scope unresolved. '
            'Known September option cash is already in cutoff cash; only remaining hypothetical exercise receipts appear above. '
            'Future financing proceeds and extra funding dilution from the conditional statements are not added on top of negative FCFF.','',
            'Full assumptions and limitations: docs/equity-bridge.md and data/equity_bridge_assumptions.json.']
    return '\n'.join(lines)+'\n'


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--save',action='store_true',help='Save visible Markdown and JSON in outputs.')
    args=parser.parse_args()
    result=report()
    if args.save:
        (ROOT/'outputs/equity-bridge.md').write_text(render(result),encoding='utf-8')
        (ROOT/'outputs/equity-bridge.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        print('Saved outputs/equity-bridge.md and outputs/equity-bridge.json')
    else:
        print(render(result),end='')
