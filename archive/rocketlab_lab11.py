"""Lab 11 sensitivity; run beside unchanged rocketlab_lab10.py. Standard library only."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'rocketlab_lab10.py'
DRIVERS = {'GROWTH': ('Revenue growth', 0.05), 'RD': ('R&D expense', 0.20)}
METRICS = {'operating_profit': 'FY2030 operating profit ($m)',
           'fcfe': 'FY2030 FCFE ($m)', 'value_per_share': 'Signed-FCFE value ($/share)'}


def fresh_model():
    spec = importlib.util.spec_from_file_location('lab10_independent_run', SOURCE)
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    return model


def inputs(model):
    return deepcopy({k: v for k, v in vars(model).items() if k.isupper()})


def run(base_inputs, driver=None, shift=0.0):
    model = fresh_model()
    # Separate immutable-in-practice baseline snapshot, deep copied on EVERY run.
    for key, val in deepcopy(base_inputs).items():
        setattr(model, key, val)
    if driver:
        # Growth shifts are percentage points; R&D shifts are relative percentages.
        setattr(model, driver, [v * (1 + shift) if driver == 'RD' else v + shift
                                for v in base_inputs[driver]])
    actual = inputs(model)
    changed = [k for k in base_inputs if actual[k] != base_inputs[k]]
    assert changed == ([driver] if shift else []), changed
    result = dict(inputs=actual, changed_inputs=changed, checks=[], rows=[],
                  outputs={k: None for k in METRICS}, valid=False)
    try:
        rows = model.project()
        prior = model.OPENING
        for row in rows:
            model.check(row, prior)
            result['checks'].append(dict(year=row['year'], balance_gap=model.balance_gap(row),
                cash=row['cash'], cash_floor=model.MINIMUM_CASH, status='PASS'))
            prior = row
        result.update(rows=rows, valid=True)
        result['outputs'].update(operating_profit=rows[-1]['operating_income'], fcfe=rows[-1]['fcfe'])
    except ValueError as error:
        result['error'] = str(error)
        return result
    try:
        valuation = model.value(rows)
        result['valuation'] = valuation
        # Include negative forecast years; retain course convention only in detail.
        result['outputs']['value_per_share'] = valuation['adjusted_per_share']
    except ValueError as error:
        result['valuation_unavailable'] = str(error)
    assert inputs(model) == actual, 'Model mutated independent assumptions'
    return result


def number(val, signed=False):
    return 'Unavailable' if val is None else format(val, '+.3f' if signed else '.3f')


def main():
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    base_inputs = inputs(fresh_model())
    base_snapshot = deepcopy(base_inputs)
    base = run(base_inputs)
    assert base['valid'], base.get('error')
    runs, spans = {}, {}
    for driver, (label, width) in DRIVERS.items():
        runs[driver] = {}
        for scenario, shift in [('Lower', -width), ('Base', 0.0), ('Higher', width)]:
            outcome = run(base_inputs, driver, shift)
            outcome['deltas'] = {k: (v - base['outputs'][k]
                if v is not None and base['outputs'][k] is not None else None)
                for k, v in outcome['outputs'].items()}
            runs[driver][scenario] = outcome
        spans[driver] = {}
        for key in METRICS:
            values = [r['outputs'][key] for r in runs[driver].values()
                      if r['valid'] and r['outputs'][key] is not None]
            spans[driver][key] = dict(span=max(values)-min(values) if len(values) >= 2 else None,
                                     valid_count=len(values))
    restored = run(base_inputs)
    assert base_inputs == base_snapshot, 'Baseline assumptions changed'
    assert restored == base, 'Restored base differs (exact comparison)'
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == source_hash
    payload = dict(generated_utc=datetime.now(timezone.utc).isoformat(),
        source_sha256=source_hash, base=base, runs=runs, spans=spans, restored_base=restored,
        restored_base_exact_match=True)
    (ROOT / 'rocketlab_lab11_details.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    lines = ['# Rocket Lab Lab 11 — visible sensitivity output', '',
        'Generated UTC: ' + payload['generated_utc'], '',
        'Dollar amounts are USD millions except value per share. Paths are FY2026–FY2030.',
        'Value uses Lab 10 funding-adjusted signed FCFE plus initial excess liquidity.',
        'Annual-baseline classroom scenario; not an updated market valuation.', '',
        '## Inputs, results and changes from the original base', '',
        '| Driver / case | Actual input path (units shown) | Operating profit | Change | FCFE | Change | Value/share | Change | Checks |',
        '|---|---|---:|---:|---:|---:|---:|---:|---|']
    for driver, cases in runs.items():
        for name, r in cases.items():
            vals = []
            for key in METRICS:
                vals.extend([number(r['outputs'][key]), number(r['deltas'][key], True)])
            path = (', '.join(f'{v:.0f}' for v in r['inputs'][driver]) + ' USD million'
                    if driver == 'RD' else
                    ', '.join(f'{100*v:.0f}' for v in r['inputs'][driver]) + ' %')
            status = 'PASS all 5 years' if r['valid'] else 'INVALID: ' + r['error']
            lines.append('| ' + ' | '.join([DRIVERS[driver][0]+' / '+name, path]+vals+[status])+' |')
            if 'valuation_unavailable' in r:
                lines.append('\nValue unavailable: '+r['valuation_unavailable']+'\n')
    lines += ['', '## Output spans: maximum minus minimum', '',
              '| Output | Revenue-growth span | R&D-expense span | Larger driver over these ranges |',
              '|---|---:|---:|---|']
    for key, label in METRICS.items():
        a, b = (spans[d][key] for d in DRIVERS)
        complete = a['valid_count'] == b['valid_count'] == 3
        winner = ('Revenue growth' if a['span'] > b['span'] else
                  'R&D expense' if b['span'] > a['span'] else 'Tie') if complete else 'Not ranked: incomplete valid runs'
        lines.append(f"| {label} | {number(a['span'])} ({a['valid_count']}/3 valid) | {number(b['span'])} ({b['valid_count']}/3 valid) | {winner} |")
    lines += ['', '## Accounting and isolation evidence', '',
        'Every run starts from a deep independent copy of all base inputs.',
        'Only the named driver differs; this is asserted before running the linked model.',
        'Each valid year passes the original balance-sheet, liquidity and roll-forward checks.',
        'Restored base inputs, all five statement rows, checks and valuations: EXACT MATCH.',
        'Comparison tolerance for base restoration: zero (unrounded Python values).',
        'Accounting-check tolerance: 0.000001 USD million.',
        'Original Lab 10 source SHA256 unchanged: ' + source_hash, '',
        '| Run | Maximum absolute balance gap ($m) | Minimum cash ($m) |', '|---|---:|---:|']
    for driver, cases in runs.items():
        for name, r in cases.items():
            if r['valid']:
                lines.append(f"| {DRIVERS[driver][0]} / {name} | {max(abs(c['balance_gap']) for c in r['checks']):.12f} | {min(c['cash'] for c in r['checks']):.3f} |")
    selected = runs['RD']['Higher']
    lines += ['', '## Selected trace: higher R&D versus base, FY2030', '',
        '| Line ($m) | Base | Higher R&D | Change |', '|---|---:|---:|---:|']
    for key in ['revenue', 'gross_profit', 'cost_of_sales', 'sga', 'rd', 'operating_income',
                'tax', 'net_income', 'inventory', 'payables', 'change_wc', 'depreciation',
                'amortization', 'cfo', 'capex', 'fcfe']:
        a, b = base['rows'][-1][key], selected['rows'][-1][key]
        lines.append(f'| {key} | {a:.3f} | {b:.3f} | {b-a:+.3f} |')
    output = '\n'.join(lines)+'\n'
    (ROOT / 'rocketlab_lab11_output.md').write_text(output, encoding='utf-8')
    print(output)


if __name__ == '__main__':
    main()
