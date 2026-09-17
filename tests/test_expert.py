import unittest

from src.expert import ExpertSystem, validate_rules


class ExpertSystemTests(unittest.TestCase):
    def test_rule_validation_rejects_unknown_sources(self):
        rules = [{
            "id": "R-1", "description": "test", "priority": 1,
            "when": {"all": [{"fact": "x", "equals": True}]},
            "then": [{"fact": "y", "value": True}], "source_ids": ["missing"]
        }]
        self.assertIn(
            "rule R-1 references unknown source missing",
            validate_rules(rules, set()),
        )

    def test_rule_fires_and_explains_itself(self):
        rules = [{
            "id": "R-1", "description": "control plus authority", "priority": 10,
            "when": {"all": [
                {"fact": "control", "equals": True},
                {"fact": "authority", "equals": True},
            ]},
            "then": [{"fact": "ready", "value": True}], "source_ids": ["S-1"]
        }]
        result = ExpertSystem(rules).infer({"control": True, "authority": True})
        self.assertEqual(result["facts"]["ready"][0]["value"], True)
        self.assertEqual(result["trace"][0]["rule_id"], "R-1")
        self.assertEqual(result["trace"][0]["sources"], ["S-1"])

    def test_unknown_is_not_false(self):
        rules = [{
            "id": "R-1", "description": "explicit negative only", "priority": 1,
            "when": {"all": [{"fact": "authority", "equals": False}]},
            "then": [{"fact": "gap", "value": True}]
        }]
        result = ExpertSystem(rules).infer({})
        self.assertNotIn("gap", result["facts"])
        self.assertEqual(result["trace"], [])

    def test_why_not_lists_missing_prerequisite(self):
        rules = [{
            "id": "R-1", "description": "needs authority", "priority": 1,
            "when": {"all": [{"fact": "authority", "equals": True}]},
            "then": [{"fact": "ready", "value": True}], "source_ids": ["S-1"]
        }]
        result = ExpertSystem(rules).infer({}, targets=["ready"])
        unmet = result["why_not"][0]["candidate_rules"][0]["unmet"][0]
        self.assertEqual(unmet["required"]["fact"], "authority")
        self.assertEqual(unmet["actual"], "unknown")

    def test_conflicting_conclusions_are_reported(self):
        rules = [
            {"id": "R-A", "description": "yes", "priority": 1,
             "when": {"all": [{"fact": "trigger", "equals": True}]},
             "then": [{"fact": "decision", "value": True}]},
            {"id": "R-B", "description": "no", "priority": 1,
             "when": {"all": [{"fact": "trigger", "equals": True}]},
             "then": [{"fact": "decision", "value": False}]},
        ]
        result = ExpertSystem(rules).infer({"trigger": True})
        self.assertEqual(result["status"], "conflict")
        self.assertEqual(result["conflicts"][0]["fact"], "decision")

    def test_priority_then_identifier_is_deterministic(self):
        rules = [
            {"id": "R-B", "description": "later", "priority": 1,
             "when": {"all": [{"fact": "x", "equals": True}]},
             "then": [{"fact": "b", "value": True}]},
            {"id": "R-A", "description": "first", "priority": 2,
             "when": {"all": [{"fact": "x", "equals": True}]},
             "then": [{"fact": "a", "value": True}]},
        ]
        result = ExpertSystem(rules).infer({"x": True})
        self.assertEqual([step["rule_id"] for step in result["trace"]], ["R-A", "R-B"])


if __name__ == "__main__":
    unittest.main()
