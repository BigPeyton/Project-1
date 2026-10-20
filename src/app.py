"""Local, read-only valuation application. Standard library only; no credentials."""
import argparse
import copy
import html
import json
import math
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit
from three_statements import load_inputs, project, balance_gap, ASSETS, LIABILITIES, IS_KEYS
from valuation import assumptions as valuation_assumptions, value
from equity_bridge import assumptions as bridge_assumptions, bridge
from proforma_sensitivity import apply_drivers, assumptions as sensitivity_assumptions

ROOT=Path(__file__).resolve().parents[1]
FIELDS={'case','wacc','growth','margin','roic','space_growth','space_margin','rd_scale','neutron_scale'}
EVIDENCE={
    'decision':('docs/committee-decision.md','Committee rationale'),
    'validation':('docs/validation-and-ai-use.md','Validation and AI use'),
    'sources':('docs/source-audit.md','Source audit'),
    'drivers':('data/valuation_assumptions.json','Valuation assumptions and challenges'),
    'reverse':('outputs/reverse-dcf.md','Reverse DCF'),
    'peers':('outputs/comparables.md','Peer comparison'),
    'exit':('outputs/downside-exit.md','Conditional orderly exit'),
    'bridge':('outputs/equity-bridge.md','Instrument sensitivities'),
    'operating':('outputs/proforma-sensitivity.md','Operating sensitivities and rankings'),
    'bounds':('data/proforma_sensitivity_assumptions.json','Control bounds and challenges'),
}


def controls(params):
    if set(params)-FIELDS: raise ValueError('Unknown control. Reset to base and try again.')
    case=params.get('case','base')
    if case not in ('base','upside','downside'): raise ValueError('Choose base, upside or downside.')
    a=valuation_assumptions(); c=a['cases'].get(case,a['cases']['base'])
    defaults=dict(wacc=16,growth=3,margin=100*c['mature_ebit_margin'],roic=100*c['mature_incremental_roic'])
    bounds=dict(wacc=(3,30),growth=(0,8),margin=(4,40),roic=(5,40))
    for key,spec in sensitivity_assumptions()['drivers'].items():
        defaults[key]=spec['default']; bounds[key]=spec['bounds']
    result=dict(case=case)
    for key,default in defaults.items():
        raw=params.get(key,default)
        try: number=float(raw)
        except (ValueError,TypeError): raise ValueError(f'{key}: enter a finite percentage.') from None
        low,high=bounds[key]
        if not math.isfinite(number) or not low <= number <= high:
            raise ValueError(f'{key}: allowed range is {low} to {high} in the displayed units.')
        result[key]=number
    if result['growth'] >= result['wacc']: raise ValueError('Terminal growth must be below WACC. No valuation produced.')
    if result['growth'] >= result['roic']: raise ValueError('Terminal growth must be below marginal ROIC. No valuation produced.')
    return result


def calculate(params):
    c=controls(params); raw_inputs=load_inputs(); a=copy.deepcopy(valuation_assumptions())
    inputs,_=apply_drivers(raw_inputs,c['case'],{k:c[k] for k in sensitivity_assumptions()['drivers']})
    # Unfunded downside must fail here, before any unsupported going-concern terminal value.
    model=project(*inputs,case=c['case'])
    a['cases'][c['case']]['mature_ebit_margin']=c['margin']/100
    a['cases'][c['case']]['mature_incremental_roic']=c['roic']/100
    v=value(model,a,c['case'],wacc=c['wacc']/100,growth=c['growth']/100)
    b=bridge(model,v,inputs[-1],bridge_assumptions())
    gap=max(abs(balance_gap(row['balance_sheet'])) for row in model['annual'])
    continuity=abs(v['terminal']['fcff']-v['transition'][-1]['fcff']*(1+v['growth']))
    bridge_gap=abs(sum(b['lines'].values())-b['residual_before_limited_liability'])
    if max(gap,continuity,bridge_gap)>1e-6: raise ValueError('Accounting or valuation reconciliation failed.')
    reference_model=project(*raw_inputs); reference_value=value(reference_model,valuation_assumptions())
    reference_bridge=bridge(reference_model,reference_value,raw_inputs[-1],bridge_assumptions())
    reference=dict(ebit_2030=reference_model['annual'][-1]['operating_income'],fcff_2030=reference_model['annual'][-1]['fcff'],price=reference_bridge['price'])
    custom=dict(ebit_2030=model['annual'][-1]['operating_income'],fcff_2030=model['annual'][-1]['fcff'],price=b['price'])
    comparison={key:dict(base=reference[key],custom=custom[key],change=custom[key]-reference[key]) for key in reference}
    return dict(controls=c,cutoff=a['cutoff'],reference_price=a['discount_rate']['reference_price'],comparison=comparison,
                model=model,valuation=v,bridge=b,
                checks=dict(max_balance_sheet_gap=gap,terminal_continuity_gap=continuity,bridge_gap=bridge_gap),
                decision='Adopted reference recommendation: WATCH / DEFER. Custom scenarios do not automatically change it.')


def esc(value): return html.escape(str(value),quote=True)
def fmt(value): return f'{value:,.3f}'


CSS='''
:root{color-scheme:light;font-family:system-ui,Segoe UI,sans-serif;color:#182c3b;background:#f2f5f8}
*{box-sizing:border-box}body{margin:0}main{max-width:1180px;margin:auto;padding:30px 24px 60px}
h1{font-size:2.15rem;letter-spacing:-.04em;margin:8px 0}h2{font-size:1.15rem;margin-top:0}
.eyebrow{font-size:.78rem;font-weight:750;letter-spacing:.12em;color:#356579;text-transform:uppercase}
.muted,small{color:#4f6575}p{line-height:1.6}a{color:#075b87}header{margin-bottom:24px}
.panel{background:white;border:1px solid #d7e0e7;border-radius:12px;padding:22px;margin:18px 0}
.decision{border-left:5px solid #ad7919;background:#fffcf5}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.metric{padding:18px;background:#f4f8fb;border-radius:9px}.metric strong{display:block;font-size:1.7rem;margin-top:7px}
form{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}label{font-size:.84rem;font-weight:650}
input,select{display:block;width:100%;font:inherit;padding:10px;margin:7px 0;border:1px solid #8d9eac;border-radius:5px;background:white;color:#182c3b}
.actions{grid-column:1/-1;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
button,.button{font:inherit;font-weight:650;padding:11px 18px;border-radius:6px;border:0;background:#125574;color:white;cursor:pointer;text-decoration:none}
.button.secondary{background:#e4edf2;color:#183e53}.error{border-left:5px solid #b52e31;background:#fff4f4;color:#842024}
.checks{display:flex;flex-wrap:wrap;gap:12px}.check{background:#e7f4ed;color:#1f6040;padding:7px 12px;border-radius:20px;font-size:.85rem}
.scroll{overflow:auto}table{width:100%;border-collapse:collapse;font-size:.86rem}th,td{text-align:right;padding:10px;border-bottom:1px solid #e0e7ed;white-space:nowrap}
th:first-child,td:first-child{text-align:left}thead{background:#edf3f7}summary{cursor:pointer;font-weight:650;padding:9px 0}details{margin:12px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.55;font-size:.9rem}
nav{display:flex;gap:16px;flex-wrap:wrap}li{line-height:1.6}a:focus,button:focus,input:focus,select:focus,summary:focus{outline:3px solid #d49f34;outline-offset:3px}
@media(max-width:800px){form{grid-template-columns:repeat(2,1fr)}.grid{grid-template-columns:repeat(2,1fr)}main{padding:20px 14px}h1{font-size:1.7rem}}
'''


def shell(content,title='Rocket Lab | Committee workbench'):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><style>{CSS}</style></head><body><main>{content}</main></body></html>'


def table(headers,rows):
    return '<div class="scroll"><table><thead><tr>'+''.join(f'<th scope="col">{esc(h)}</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{esc(x)}</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'


def page(params,result=None,error=None):
    raw=dict(case='base',wacc=16,growth=3,margin=12,roic=16,space_growth=0,space_margin=0,rd_scale=100,neutron_scale=100)
    if params.get('case')=='upside': raw.update(margin=20,roic=20)
    raw.update(params)
    if result: raw.update(result['controls'])
    content='<header><div class="eyebrow">FIN 439 · Project 1</div><h1>Rocket Lab committee workbench</h1><p class="muted">Information cutoff: September 10, 2026 · 4 PM ET · Nominal USD</p></header>'
    content+='<section class="panel decision"><h2>WATCH / DEFER · No initiation at the $61.96 reference price</h2><p>Student-adopted rationale. Reference standalone scenarios: approximately <strong>$1–$7 per share</strong>. This conditional range excludes pending Iridium economics and is not a guaranteed floor. Custom scenarios inform a review; they do not automatically replace the recommendation.</p></section>'
    content+='<section class="panel"><h2>Explore an assumption</h2><p class="muted">Change one control at a time to interpret its effect. Enter 16 for 16%. Operating shifts affect 2027–2030; mature margin and marginal ROIC affect the 2031–2040 transition. A shift of 1 pp means one percentage point. A 100% spending/revenue scale preserves the selected path.</p><form method="get" action="/"><label>Operating scenario<select name="case" aria-label="Operating scenario">'
    for case in ('base','upside','downside'):
        content+=f'<option value="{case}"'+(' selected' if raw['case']==case else '')+f'>{case.title()}</option>'
    content+='</select></label>'
    for key,label in [('wacc','WACC (%)'),('growth','Terminal growth (%)'),('margin','Mature EBIT margin (%)'),('roic','Marginal ROIC (%)')]:
        content+=f'<label>{label}<input name="{key}" type="number" step="any" required value="{esc(raw[key])}" aria-label="{label}"></label>'
    for key,label in [('space_growth','Space growth shift (pp; -5 to 5)'),('space_margin','Space gross-margin shift (pp; -3 to 3)'),('rd_scale','R&D scale (%; 80 to 120)'),('neutron_scale','Neutron revenue scale (%; 50 to 150)')]:
        content+=f'<label>{label}<input name="{key}" type="number" step="any" required value="{esc(raw[key])}" aria-label="{label}"></label>'
    content+='<div class="actions"><button type="submit">Recalculate</button><a class="button secondary" href="/">Reset to base</a><a href="/?case=upside">Load upside defaults</a><a href="/?case=base&amp;wacc=3&amp;growth=3">Test invalid boundary</a><a href="/?case=downside">Test downside funding</a></div></form><p class="muted"><small>Changing the scenario selector preserves entered valuation controls. “Load upside defaults” loads its 20% margin and 20% return assumptions. Inputs are temporary and do not overwrite source files.</small></p></section>'
    if error:
        content+=f'<section class="panel error" role="alert"><h2>Cannot value this scenario</h2><p>{esc(error)}</p><p>No result is displayed for the failed run. Correct the inputs or reset to base. For downside alternatives, review the separate conditional orderly-exit evidence.</p></section>'
    if result:
        b=result['bridge']; v=result['valuation']; model=result['model']; rows=model['annual']
        share='Not meaningful' if v['terminal_share'] is None else f'{v["terminal_share"]:.1%}'
        content+='<section class="panel"><h2>Scenario result · '+esc(raw['case'])+'</h2><div class="grid">'
        for label,val in [('Conditional value / share',f'${b["price"]:.2f}'),('Operating EV (USD m)',fmt(v['enterprise_value'])),('Participating shares (m)',fmt(b['shares'])),('Terminal share of EV',share)]:
            content+=f'<div class="metric"><span>{esc(label)}</span><strong>{esc(val)}</strong></div>'
        content+='</div><p>Full award vesting / option exercise / note conversion assumed. '+('This model value does not support note conversion at its principal threshold. ' if not b['conversion_supported'] else '')+'See retained-note and other instrument sensitivities before treating this as an unconditional common-stock value. A negative operating EV is the net present cost of the modeled strategy.</p>'
        content+='<div class="checks">'+''.join(f'<span class="check">{s}</span>' for s in ['Statement articulation passed','No new equity required','Terminal continuity passed','Equity bridge reconciled'])+'</div><p><small>These checks validate arithmetic and modeled funding, not the truth of forecasts or completion of the final cold run.</small></p>'
        content+='<h2>Compare with restored base</h2>'+table(['Metric','Base','This run','Change'],[(label,fmt(result['comparison'][key]['base']),fmt(result['comparison'][key]['custom']),fmt(result['comparison'][key]['change'])) for key,label in [('ebit_2030','2030 EBIT (USD m)'),('fcff_2030','2030 FCFF (USD m)'),('price','Conditional value (USD/share)')]])
        content+='<p><small>Comparison uses the same original base every time. R&D reductions hold revenue fixed for attribution; they are not a claim that spending can be cut without affecting products. Bounds are analyst stress limits, not historical confidence intervals. Read the bounds/ranking evidence below.</small></p>'
        content+=f'<p><a href="/result.json?{esc(urlencode(result["controls"]))}">Download this run (JSON)</a></p></section>'
        content+='<section class="panel"><h2>Trace the result</h2><details open><summary>Enterprise-to-equity bridge · USD millions</summary>'
        content+=table(['Component','USD millions'],[(k.replace('_',' ').capitalize(),fmt(n)) for k,n in b['lines'].items()]+[('Equity allocated to participating shares',fmt(b['equity']))])+'</details>'
        headers=['USD millions']+[r['year'] for r in rows]
        content+='<details><summary>Five-year income statement</summary>'+table(headers,[(k.replace('_',' ').capitalize(),*[fmt(r[k]) for r in rows]) for k in IS_KEYS])+'</details>'
        def bs_value(r,k):
            bs=r['balance_sheet']
            if k=='total_assets': return sum(bs[x] for x in ASSETS)
            if k=='total_liabilities': return sum(bs[x] for x in LIABILITIES)
            if k=='balance_gap': return balance_gap(bs)
            return bs[k]
        keys=ASSETS+['total_assets']+LIABILITIES+['total_liabilities','equity','balance_gap']
        content+='<details><summary>Five-year balance sheet</summary>'+table(headers,[(k.replace('_',' ').capitalize(),*[fmt(bs_value(r,k)) for r in rows]) for k in keys])+'</details>'
        keys=['net_income','da','sbc_addback','other_cfo_adjustments','cfo','cash_capex','cfi','cff','fx_cash','net_equity_raised','future_fcff']
        content+='<details><summary>Five-year cash flow and FCFF</summary><p>2026 statement flows cover the full year; 2026 future FCFF includes only cash flows after September 10. Restricted cash is included in the accounting cash-flow roll-forward.</p>'+table(headers,[(('Post-cutoff FCFF' if k=='future_fcff' else k.replace('_',' ').capitalize()),*[fmt(r[k]) for r in rows]) for k in keys])+'</details>'
        content+='<details><summary>2031–2040 transition</summary>'+table(['Year','Revenue (m)','EBIT margin','Reinvestment (m)','FCFF (m)'],[(r['year'],fmt(r['revenue']),f'{r["ebit_margin"]:.1%}',fmt(r['reinvestment']),fmt(r['fcff'])) for r in v['transition']])+'</details></section>'
    content+='<section class="panel"><h2>Evidence and limitations</h2><p>Reference excludes pending Iridium operations and funding, optional forward/ATM financing, capped-call proceeds and customer-loan recovery. Cutoff cash is estimated. Discount-rate, margin and capital-return inputs remain analyst judgments. Peer indications use different methods and must not be averaged mechanically.</p><nav>'+''.join(f'<a href="/evidence/{key}">{esc(label)}</a>' for key,(_,label) in EVIDENCE.items())+'</nav></section>'
    return shell(content)


def response_for(path):
    parsed=urlsplit(path)
    if parsed.path.startswith('/evidence/'):
        key=parsed.path.removeprefix('/evidence/')
        if key not in EVIDENCE: return 404,'text/plain; charset=utf-8','Evidence not found.'
        location,label=EVIDENCE[key]; file=ROOT/location
        if not file.is_file(): return 404,'text/plain; charset=utf-8','Evidence is not available yet.'
        return 200,'text/html; charset=utf-8',shell(f'<a href="/">Back to workbench</a><h1>{esc(label)}</h1><pre>{esc(file.read_text(encoding="utf-8"))}</pre>',label)
    if parsed.path not in ('/','/result.json'): return 404,'text/plain; charset=utf-8','Not found.'
    params={}
    try:
        if len(parsed.query)>2048: raise ValueError('Input is too long.')
        pairs=parse_qs(parsed.query,keep_blank_values=True,max_num_fields=10)
        if any(len(v)!=1 for v in pairs.values()): raise ValueError('Duplicate input controls are not allowed.')
        params={k:v[0] for k,v in pairs.items()}
        result=calculate(params)
    except (ValueError,ArithmeticError) as error:
        if parsed.path=='/result.json': return 422,'application/json; charset=utf-8',json.dumps(dict(error=str(error)))
        return 422,'text/html; charset=utf-8',page(params,error=str(error))
    if parsed.path=='/result.json': return 200,'application/json; charset=utf-8',json.dumps(result,indent=2,allow_nan=False)
    return 200,'text/html; charset=utf-8',page(params,result=result)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try: status,kind,body=response_for(self.path)
        except Exception:
            status,kind,body=500,'text/plain; charset=utf-8','Unexpected application failure. No result produced; inspect the terminal and reset after repair.'
            import traceback; traceback.print_exc()
        data=body.encode('utf-8'); self.send_response(status)
        self.send_header('Content-Type',kind); self.send_header('Content-Length',str(len(data)))
        self.send_header('Cache-Control','no-store'); self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Content-Security-Policy',"default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'")
        if self.path.startswith('/result.json') and status==200:
            self.send_header('Content-Disposition','attachment; filename="scenario-result.json"')
        self.end_headers(); self.wfile.write(data)


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--port',type=int,default=8765); args=parser.parse_args()
    if not 1024 <= args.port <= 65535: parser.error('Use a port between 1024 and 65535.')
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    print(f'Open http://127.0.0.1:{args.port} in your browser. Ctrl+C stops the app.',flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
