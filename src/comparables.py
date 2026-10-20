"""Qualified FY2025 revenue multiples with explicitly lease-inclusive EV."""
import copy
import json
import math
from datetime import datetime
from pathlib import Path
from three_statements import load_inputs,project
from equity_bridge import bridge,assumptions as bridge_assumptions
ROOT=Path(__file__).resolve().parents[1]


def inputs(): return json.loads((ROOT/'data/peer_inputs.json').read_text())


def multiples(a):
    seen=set(); rows=[]; cutoff=datetime.fromisoformat(a['cutoff'])
    for p in a['peers']:
        if p['ticker'] in seen: raise ValueError('Duplicate peer.')
        seen.add(p['ticker'])
        if p['price_date']!=a['price_date'] or p['revenue_period']!=a['revenue_period']:
            raise ValueError('Price or fiscal-period mismatch.')
        published=datetime.fromisoformat(p['published'])
        if published.tzinfo is None:
            if published.date()>=cutoff.date(): raise ValueError('Same-day evidence needs verified publication time.')
        elif published>cutoff: raise ValueError('Post-cutoff information.')
        if p['currency']!=p['financial_currency']: raise ValueError('Mixed currency numerator and denominator.')
        if any(not math.isfinite(p[k]) or p[k]<=0 for k in ('price','shares_m','revenue')):
            raise ValueError('Price, shares and revenue must be positive and finite.')
        if any(not math.isfinite(x) or x<0 for x in [p['cash'],p['liquid_investments'],*p['claims'].values()]):
            raise ValueError('Invalid claim/cash input.')
        if 'issued_shares' in p and abs(p['shares_m']-(p['issued_shares']-p['treasury_shares'])/1e6)>1e-8:
            raise ValueError('Treasury shares must be excluded from issued capital.')
        equity=p['price']*p['shares_m']
        ev=equity+sum(p['claims'].values())-p['cash']-p['liquid_investments']
        rows.append(dict(ticker=p['ticker'],currency=p['currency'],equity=equity,ev=ev,
                         price_sales=equity/p['revenue'],ev_sales=ev/p['revenue'],
                         reported_operating_margin=p['reported_operating_income']/p['revenue']))
    return rows


def report(a=None):
    a=inputs() if a is None else a; rows=multiples(a)
    x=load_inputs(); m=project(*x); cap=x[-1]
    sales=x[0]['fy2025']['income_statement']['revenue']/1000
    ordinary=(cap['derived_scenarios']['august_common_plus_preferred']+cap['known_september_exercise']['shares'])/1e6
    lease=m['cutoff_balance_sheet']['operating_lease_noncurrent']+a['target_current_operating_lease_proxy']
    indications=[]
    for p in rows:
        # Peer EV capitalizes all leases. Subtract operating lease claim once
        # to express target value on our after-rent DCF bridge convention.
        ev_including_leases=p['ev_sales']*sales
        v=dict(case='base',enterprise_value=ev_including_leases-lease)
        b=bridge(m,v,cap,bridge_assumptions())
        indications.append(dict(ticker=p['ticker'],ev_method_price_if_converted=b['price'],
                                ps_method_price_basic_equivalent=p['price_sales']*sales/ordinary,
                                implied_lease_inclusive_ev=ev_including_leases,
                                current_lease_plus5_price=b['price']-5/b['shares'],
                                current_lease_minus5_price=b['price']+5/b['shares']))
    leave_out=[]
    for p in rows:
        remaining=[x for x in indications if x['ticker']!=p['ticker']]
        leave_out.append(dict(removed=p['ticker'],remaining=remaining,
                              interpretation='Single-peer indication only; no remaining cross-peer range.' if len(remaining)==1 else 'No eligible indication.' if not remaining else 'Remaining peer set.'))
    cash_stress=[]
    for p in a['peers']:
        changed=copy.deepcopy(a)
        for item in changed['peers']:
            if item['ticker']==p['ticker']: item['cash']*=.5
        adjusted=next(x for x in multiples(changed) if x['ticker']==p['ticker'])
        price=bridge(m,dict(case='base',enterprise_value=adjusted['ev_sales']*sales-lease),cap,bridge_assumptions())['price']
        cash_stress.append(dict(ticker=p['ticker'],cash_deducted_fraction=.5,ev_sales=adjusted['ev_sales'],target_price=price))
    return dict(peers=rows,indications=indications,leave_one_out=leave_out,peer_cash_stress=cash_stress,
                target_sales=sales,target_basic_equivalent_shares=ordinary,
                target_operating_lease_adjustment=lease)


def render(r):
    lines=['# Qualified comparable-company results','',
           'September 10 prices; FY2025 reported consolidated revenue. EV includes ALL lease liabilities; cash/claim/share dates and qualifications are in data/peer_inputs.json. '
           'P/S uses issued common-equivalent market equity; it is not a diluted earnings multiple.','',
           '| Peer | Currency | Market equity (m) | Lease-inclusive EV (m) | EV/revenue | P/S | Reported operating margin |',
           '|---|---|---:|---:|---:|---:|---:|']
    for p in r['peers']:
        lines.append(f'| {p["ticker"]} | {p["currency"]} | {p["equity"]:,.3f} | {p["ev"]:,.3f} | {p["ev_sales"]:.3f}x | {p["price_sales"]:.3f}x | {p["reported_operating_margin"]:.2%} |')
    lines+=['','## Rocket Lab indications, USD/share','',
            '| Peer | EV/revenue, if-converted bridge | P/S, basic-equivalent basis |','|---|---:|---:|']
    for x in r['indications']:
        lines.append(f'| {x["ticker"]} | {x["ev_method_price_if_converted"]:.4f} | {x["ps_method_price_basic_equivalent"]:.4f} |')
    lines+=['',f'EV method subtracts {r["target_operating_lease_adjustment"]:.3f} million of target operating lease claims before the existing bridge; finance leases are already in that bridge. '
            'P/S maps directly to equity and receives no extra cash/debt bridge. Share bases differ explicitly; these are not interchangeable price targets.','',
            '## Leave-one-peer-out','']
    for x in r['leave_one_out']:
        lines.append('- Remove '+x['removed']+': '+x['interpretation']+' Remaining: '+', '.join(y['ticker'] for y in x['remaining']))
    lines+=['','## Peer cash classification stress','',
            'Deduct only half of each peer cash balance, holding all other inputs fixed. This is an analyst sensitivity, not an assertion that half is restricted.','',
            '| Peer | EV/revenue | Target EV-method indication |','|---|---:|---:|']
    for x in r['peer_cash_stress']:
        lines.append(f'| {x["ticker"]} | {x["ev_sales"]:.3f}x | {x["target_price"]:.4f} |')
    lines+=['','Peer prices capitalize future expectations whereas the denominator is historical sales; DCF explicitly charges for operating losses and reinvestment. '
            'Acquisition scope, net cash, margins and capital structure explain further disagreement. P/S gives no automatic credit for target excess cash; EV does. '
            'Do not average these outputs. Neither peer currently demonstrates a repeatable 12%-20% consolidated operating margin; the DCF maturity assumptions remain ambitious, unverified analyst judgments.','',
            'P/E remains unusable for loss-making RKLB; Avio historical P/E does not fix that. No transaction multiple is used: pending Iridium and other acquisition evidence lack a matched control/synergy/time basis for this standalone comparison.','',
            'Policy and source interpretation: docs/peer-policy.md and docs/downside-and-comparables.md. These two qualified firms do not establish a statistically defensible fair-value interval.']
    return '\n'.join(lines)+'\n'


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(); p.add_argument('--save',action='store_true'); args=p.parse_args(); r=report()
    if args.save:
        (ROOT/'outputs/comparables.md').write_text(render(r),encoding='utf-8')
        (ROOT/'outputs/comparables.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
        print('Saved comparable outputs.')
    else: print(render(r),end='')
