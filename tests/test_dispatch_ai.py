"""Offline contract tests for AI dispatch payload. No network calls."""
import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location("dispatch_ai",Path(__file__).resolve().parents[1]/"integrations"/"dispatch_ai.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
class DispatchTests(unittest.TestCase):
    def test_payload(self):
        p=mod.payload("gemini","3","CarlosVergaraChile/coipo-orchestrator","Audit")
        self.assertEqual(p["schema"],"idg.ai-task.v1")
        self.assertEqual(p["task_id"],"CarlosVergaraChile/coipo-orchestrator#3:gemini")
        self.assertIn("deploy",p["requires_human_approval_for"])
    def test_provider_rejected(self):
        with self.assertRaises(ValueError):mod.payload("unknown","3","CarlosVergaraChile/coipo-orchestrator","Audit")
    def test_invalid_issue(self):
        with self.assertRaises(ValueError):mod.payload("manus","abc","CarlosVergaraChile/coipo-orchestrator","Audit")
    def test_repo_scope(self):
        with self.assertRaises(ValueError):mod.payload("manus","3","someone/else","Audit")
if __name__=="__main__":unittest.main()
