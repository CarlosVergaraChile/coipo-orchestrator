"""Additional offline regression checks for multi-IA dispatch. Run: python -m unittest discover -s tests -v."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("dispatch_ai", Path(__file__).resolve().parents[1] / "integrations" / "dispatch_ai.py")
dispatch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dispatch)

class ProviderContractTests(unittest.TestCase):
    def test_each_supported_provider(self):
        for provider in ("claude", "gemini", "deepseek", "perplexity", "manus"):
            with self.subTest(provider=provider):
                p = dispatch.payload(provider, "7", "CarlosVergaraChile/coipo-orchestrator", "Synthetic QA only")
                self.assertEqual(p["provider"], provider)
                self.assertEqual(p["issue_number"], 7)
                self.assertEqual(p["task_id"], f"CarlosVergaraChile/coipo-orchestrator#7:{provider}")
                self.assertEqual(p["schema"], "idg.ai-task.v1")
                self.assertEqual(set(p["requires_human_approval_for"]), {"deploy", "merge", "delete", "outbound_contact"})
    def test_blank_prompt_rejected(self):
        with self.assertRaises(ValueError):
            dispatch.payload("gemini", "7", "CarlosVergaraChile/coipo-orchestrator", " \n ")
    def test_zero_issue_rejected(self):
        with self.assertRaises(ValueError):
            dispatch.payload("gemini", "0", "CarlosVergaraChile/coipo-orchestrator", "QA")
    def test_negative_issue_rejected(self):
        with self.assertRaises(ValueError):
            dispatch.payload("gemini", "-1", "CarlosVergaraChile/coipo-orchestrator", "QA")
    def test_case_sensitive_provider(self):
        with self.assertRaises(ValueError):
            dispatch.payload("Gemini", "7", "CarlosVergaraChile/coipo-orchestrator", "QA")
if __name__ == "__main__":
    unittest.main()
