"""Timed development audit. Never labels itself a student cold run or locked test."""
import hashlib
import io
import json
import platform
import sys
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path
from three_statements import load_inputs, project, FundingGap
import valuation
import equity_bridge
import downside_exit
import comparables
import reverse_dcf
import proforma_sensitivity

ROOT=Path(__file__).resolve().parents[1]


class AuditResult(unittest.TextTestResult):
    """Preserve failure/error discovery order for an honest first-failure record."""
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs); self.ordered_issues=[]

    def addFailure(self,test,error):
        super().addFailure(test,error); self.ordered_issues.append(self.failures[-1])

    def addError(self,test,error):
        super().addError(test,error); self.ordered_issues.append(self.errors[-1])


def audit():
    started=datetime.now(timezone.utc).isoformat(); timer=time.perf_counter()
    files=sorted(p for folder in ('src','data','tests') for p in (ROOT/folder).rglob('*') if p.suffix in ('.py','.json'))
    hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    fingerprint=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'))
    stream=io.StringIO(); test_result=unittest.TextTestRunner(stream=stream,verbosity=2,resultclass=AuditResult).run(suite)
    failures=[dict(test=str(test),detail=detail) for test,detail in test_result.ordered_issues]
    checks=[]
    for name,module,fn in [('valuation-transition',valuation,valuation.build_report),
                            ('equity-bridge',equity_bridge,equity_bridge.report),
                            ('downside-exit',downside_exit,downside_exit.evaluate),
                            ('comparables',comparables,comparables.report),
                            ('reverse-dcf',reverse_dcf,reverse_dcf.report),
                            ('proforma-sensitivity',proforma_sensitivity,proforma_sensitivity.report)]:
        try:
            current=fn()
            if current!=json.loads((ROOT/f'outputs/{name}.json').read_text(encoding='utf-8')):
                raise ValueError('Saved JSON differs from recomputation.')
            if module.render(current)!=(ROOT/f'outputs/{name}.md').read_text(encoding='utf-8'):
                raise ValueError('Saved Markdown differs from recomputation.')
            checks.append(dict(check=name,status='PASS',detail='JSON and Markdown exactly reproduce.'))
        except Exception as error:
            checks.append(dict(check=name,status='FAIL',detail=str(error)))
    try:
        project(*load_inputs(),case='downside')
        highest=dict(status='FAIL',detail='Expected unfunded downside to stop, but it completed.')
    except FundingGap as error:
        highest=dict(status='PASS: expected funding failure observed',period=error.period,
                     required_net_funding_m=error.gap,detail=str(error),
                     decision_effect='Continuing downside cannot be underwritten without committed funding; WATCH can become DO NOT INITIATE. Separate exit remains conditional.')
    errors=failures+[c for c in checks if c['status']=='FAIL']
    if highest['status']=='FAIL': errors.append(highest)
    return dict(run_started_utc=started,elapsed_seconds=round(time.perf_counter()-timer,6),
                environment=dict(python=sys.version,platform=platform.platform()),
                classification='AI-assisted development audit; NOT a recorded fresh-environment cold run or human AI-off exercise.',
                source_fingerprint_sha256=fingerprint,file_hashes=hashes,
                tests_run=test_result.testsRun,tests_successful=test_result.wasSuccessful(),test_log=stream.getvalue(),
                failures=failures,first_unexpected_failure_this_run=errors[0] if errors else None,
                reproducibility=checks,highest_risk_development_probe=highest,
                overall_pass=not errors,
                must_fix_before_submission=['Student AI-off locked prediction AND execution, with precommit evidence',
                    'Recorded README-only fresh-environment cold run with first failure and elapsed time',
                    'Final PDFs, three real videos and corrected timestamped transcripts',
                    'Manifest, source/access review, version freeze and submission receipt'])


def render(r):
    lines=['# Development validation run','',r['classification'],'',
           f'- Started (UTC): {r["run_started_utc"]}',f'- Elapsed: {r["elapsed_seconds"]:.6f} seconds',
           f'- Python: {r["environment"]["python"]}',f'- Platform: {r["environment"]["platform"]}',
           f'- Source/data/tests SHA256 fingerprint: `{r["source_fingerprint_sha256"]}`',
           f'- Tests: {r["tests_run"]}; successful: {r["tests_successful"]}',
           f'- Overall pass: {r["overall_pass"]}',
           f'- First unexpected failure in this run: {r["first_unexpected_failure_this_run"] or "none"}', '',
           '## Saved-output reproduction','']
    lines += [f'- {c["check"]}: {c["status"]}. {c["detail"]}' for c in r['reproducibility']]
    probe=r['highest_risk_development_probe']
    lines += ['', '## Highest-risk development probe','',probe['status']+'. '+probe['detail'],
              probe.get('decision_effect',''), '',
              'This probes funding failure; it does not prove terminal assumptions, transaction scope or recovery values. '
              'Prior development failures remain recorded in docs/reverse-dcf-validation.md and the other validation notes. '
              'No first failure or elapsed time from a separate cold run is inferred here.', '',
              '## Must fix before submission','']
    lines += ['- '+s for s in r['must_fix_before_submission']]
    lines += ['', '## Executed tests','', '```text',r['test_log'].rstrip(),'```']
    return '\n'.join(lines)+'\n'


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(); p.add_argument('--save',action='store_true'); args=p.parse_args(); r=audit()
    if args.save:
        (ROOT/'outputs/development-validation.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
        (ROOT/'outputs/development-validation.md').write_text(render(r),encoding='utf-8')
        print(f'Saved audit: {r["tests_run"]} tests, overall pass {r["overall_pass"]}.')
    else: print(render(r),end='')
    sys.exit(0 if r['overall_pass'] else 1)
