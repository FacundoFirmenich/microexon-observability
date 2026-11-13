import json
import unittest
from audit_transitions import audit, unique_object


class Transitions(unittest.TestCase):
    def test_equal_totals_can_hide_turnover(self):
        r = audit({'a': True, 'b': False}, {'a': False, 'b': True})
        self.assertEqual((r['net_change'], r['turnover']), (0, 2))
        self.assertEqual(r['transitions']['10'], ['a'])

    def test_abstention_preserves_identity(self):
        r = audit({'a': None, 'b': True}, {'a': False, 'b': True})
        self.assertEqual((r['identity_count'], r['paired_denominator']), (2, 1))
        self.assertEqual(r['not_evaluable'][0]['fragment'], 'a')

    def test_different_universes_rejected(self):
        with self.assertRaises(ValueError):
            audit({'a': True}, {'b': True})

    def test_numeric_not_boolean(self):
        with self.assertRaises(ValueError):
            audit({'a': 1}, {'a': True})

    def test_duplicate_json_rejected(self):
        with self.assertRaises(ValueError):
            json.loads('{"a":true,"a":false}', object_pairs_hook=unique_object)

    def test_empty_denominator_not_invented(self):
        self.assertEqual(audit({}, {})['paired_denominator'], 0)
