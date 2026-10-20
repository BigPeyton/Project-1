import hashlib
import json
import sys
import unittest
import threading
from http.server import ThreadingHTTPServer
from urllib.request import urlopen
from urllib.error import HTTPError
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from app import calculate, controls, response_for, ROOT, Handler
from three_statements import FundingGap


class ApplicationTests(unittest.TestCase):
    def test_reference_matches_saved_financial_engine(self):
        saved=json.loads((ROOT/'outputs/equity-bridge.json').read_text())
        for case in ('base','upside'):
            r=calculate(dict(case=case))
            self.assertEqual(r['bridge'],saved['cases'][case]['if_converted'])

    def test_change_then_reset_no_file_mutation(self):
        files=list((ROOT/'data').glob('*.json'))
        before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
        base=calculate({}); changed=calculate(dict(wacc='18'))
        self.assertLess(changed['bridge']['price'],base['bridge']['price'])
        self.assertEqual(calculate({}),base)
        self.assertEqual(before,{p:hashlib.sha256(p.read_bytes()).hexdigest() for p in files})

    def test_boundary_failure_then_recovery(self):
        code,_,body=response_for('/?wacc=3&growth=3')
        self.assertEqual(code,422)
        self.assertIn('Terminal growth must be below WACC',body)
        self.assertNotIn('Conditional value / share',body)
        self.assertEqual(response_for('/')[0],200)

    def test_downside_funding_not_hidden(self):
        with self.assertRaises(FundingGap): calculate(dict(case='downside'))
        code,_,body=response_for('/?case=downside')
        self.assertEqual(code,422)
        self.assertIn('314.688',body)
        self.assertNotIn('Conditional value / share',body)

    def test_invalid_and_duplicate_parameters(self):
        for query in ('wacc=NaN','growth=inf','margin=0','roic=5&growth=6',
                      'wacc=','case=unknown','wacc=16&wacc=20','surprise=1'):
            with self.subTest(query=query): self.assertEqual(response_for('/?'+query)[0],422)

    def test_export_uses_same_inputs_and_escapes_reflected_text(self):
        code,kind,body=response_for('/result.json?wacc=18')
        self.assertEqual(code,200); self.assertIn('application/json',kind)
        self.assertEqual(json.loads(body),calculate(dict(wacc='18')))
        html=response_for('/?wacc=%22%3E%3Cscript%3E')[2]
        self.assertNotIn('<script>',html); self.assertIn('&lt;script&gt;',html)

    def test_only_allowlisted_evidence_is_served(self):
        self.assertEqual(response_for('/evidence/decision')[0],200)
        for path in ('/evidence/../../session_index.jsonl','/session_index.jsonl','/data/capitalization.json'):
            self.assertEqual(response_for(path)[0],404)

    def test_page_exposes_statement_and_scope_evidence(self):
        code,_,body=response_for('/')
        self.assertEqual(code,200)
        for label in ('Five-year income statement','Five-year balance sheet','Five-year cash flow',
                      'pending Iridium','note conversion','Reset to base','No new equity required'):
            self.assertIn(label,body)


class LiveHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class QuietHandler(Handler):
            def log_message(self,*args): pass
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),QuietHandler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start(); cls.url=f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join(timeout=5)

    def test_live_export_and_headers(self):
        with urlopen(self.url+'/result.json?wacc=18',timeout=5) as response:
            self.assertEqual(response.status,200)
            self.assertEqual(response.headers['Cache-Control'],'no-store')
            self.assertIn('attachment',response.headers['Content-Disposition'])
            self.assertEqual(json.load(response)['controls']['wacc'],18)

    def test_live_failure_then_success(self):
        with self.assertRaises(HTTPError) as context:
            urlopen(self.url+'/?growth=3&wacc=3',timeout=5)
        self.assertEqual(context.exception.code,422)
        self.assertIn('No result is displayed',context.exception.read().decode())
        context.exception.close()
        with urlopen(self.url+'/',timeout=5) as response:
            self.assertEqual(response.status,200)
            self.assertIn('Conditional value / share',response.read().decode())


if __name__=='__main__': unittest.main()
