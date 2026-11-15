"""No-network regression tests for issue parser and stable deduplication key."""
import importlib.util
import pathlib
import unittest

SOURCE = pathlib.Path(__file__).resolve().parents[1] / "integrations" / "issue_task.py"
spec = importlib.util.spec_from_file_location("issue_task", SOURCE)
module = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = module
spec.loader.exec_module(module)

class IssueTaskTests(unittest.TestCase):
    def test_valid_issue(self):
        t = module.parse_issue("[AI-TASK] Caso sintético", "provider: gemini\ninstructions:\nCalcular 8/10")
        self.assertEqual((t.provider, t.instructions, t.title), ("gemini", "Calcular 8/10", "Caso sintético"))

    def test_all_providers(self):
        for p in sorted(module.PROVIDERS):
            with self.subTest(provider=p):
                self.assertEqual(module.parse_issue("[AI-TASK] Demo", f"provider: {p}\ninstructions:\nHola").provider, p)

    def test_reject_non_task_and_ambiguous_fields(self):
        invalid = [
            ("[QA Orquesta] Prueba", "provider: gemini\ninstructions:\nHola"),
            ("[AI-TASK] ", "provider: gemini\ninstructions:\nHola"),
            ("[AI-TASK] Demo", "provider: gemini\nprovider: deepseek\ninstructions:\nHola"),
            ("[AI-TASK] Demo", "provider: openai\ninstructions:\nHola"),
            ("[AI-TASK] Demo", "provider: gemini\ninstructions:\n"),
            ("[AI-TASK] Demo", "provider: gemini\nsecret: x\ninstructions:\nHola"),
            ("[AI-TASK] Demo", "provider: gemini\ninstructions:\nHola\ninstructions:\nOtro"),
            ("[AI-TASK] Demo", "provider: gemini\ninstructions:\n" + "x" * 8001),
        ]
        for title, body in invalid:
            with self.subTest(body=body[:60], title=title), self.assertRaises(ValueError):
                module.parse_issue(title, body)

    def test_stable_key(self):
        key = module.task_key("CarlosVergaraChile/coipo-orchestrator", 15, "deepseek")
        self.assertEqual(key, "CarlosVergaraChile/coipo-orchestrator#15:deepseek")
        self.assertEqual(key, module.task_key("CarlosVergaraChile/coipo-orchestrator", 15, "deepseek"))

    def test_reject_unauthorized_key(self):
        for repo, number, provider in [
            ("other/repo", 15, "gemini"),
            ("CarlosVergaraChile/repo", 0, "gemini"),
            ("CarlosVergaraChile/repo", True, "gemini"),
            ("CarlosVergaraChile/repo", 15, "openai"),
        ]:
            with self.subTest(repo=repo, number=number, provider=provider), self.assertRaises(ValueError):
                module.task_key(repo, number, provider)

if __name__ == "__main__":
    unittest.main()
