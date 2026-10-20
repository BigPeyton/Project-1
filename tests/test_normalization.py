import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from normalize_history import load_inputs, normalize


class NormalizationTests(unittest.TestCase):
    def setUp(self):
        self.reported, self.policy = load_inputs()

    def test_reconciliation_and_reported_data_preserved(self):
        original = copy.deepcopy(self.reported)
        values = normalize(self.reported, self.policy)
        self.assertEqual(values['fy2025']['normalized_ebit'], -228838)
        self.assertEqual(values['h1_2026']['normalized_ebit'], -102303)
        self.assertEqual(values['h1_2026']['normalized_sga'], 100430)
        self.assertEqual(self.reported, original)

    def test_noncash_removal_cannot_create_cash(self):
        values = normalize(self.reported, self.policy)['h1_2026']
        self.assertEqual(values['remaining_sbc'], 36497)
        self.assertEqual(values['illustrative_cfo_unchanged'], -134407)
        self.policy['adjustments'][0]['treatment'] = 'retain'
        retained = normalize(self.reported, self.policy)['h1_2026']
        self.assertEqual(retained['normalized_ebit'], -113483)
        self.assertEqual(retained['illustrative_cfo_unchanged'], values['illustrative_cfo_unchanged'])

    def test_duplicate_and_post_cutoff_evidence_rejected(self):
        bad = copy.deepcopy(self.policy)
        bad['adjustments'].append(copy.deepcopy(bad['adjustments'][0]))
        with self.assertRaises(ValueError):
            normalize(self.reported, bad)
        bad = copy.deepcopy(self.policy)
        bad['sources']['Q26']['published'] = '2026-09-11'
        with self.assertRaises(ValueError):
            normalize(self.reported, bad)

    def test_wrong_da_scope_fails(self):
        self.policy['h1_2026_release_crosscheck']['depreciation'] = 16144
        with self.assertRaises(ValueError):
            normalize(self.reported, self.policy)


if __name__ == '__main__':
    unittest.main()
