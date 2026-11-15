"""Pruebas del contrato de despacho. Sin red ni secretos; Python stdlib."""
import importlib.util
import pathlib
import unittest

SOURCE = pathlib.Path(__file__).resolve().parents[1] / "integrations" / "dispatch_ai.py"
spec = importlib.util.spec_from_file_location("dispatch_ai", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class DispatchContractTests(unittest.TestCase):
    def test_allowed_providers_have_stable_key(self):
        for provider in ("gemini", "deepseek", "manus", "claude", "perplexity"):
            with self.subTest(provider=provider):
                p = module.payload(provider, "15", "CarlosVergaraChile/coipo-orchestrator", "Prueba sintética")
                self.assertEqual(p["task_id"], f"CarlosVergaraChile/coipo-orchestrator#15:{provider}")
                self.assertEqual(p["schema"], "idg.ai-task.v1")
                self.assertIn("merge", p["requires_human_approval_for"])
                self.assertIn("deploy", p["requires_human_approval_for"])

    def test_invalid_provider(self):
        for provider in ("openai", "Gemini", "", "../gemini"):
            with self.subTest(provider=provider):
                with self.assertRaises(ValueError):
                    module.payload(provider, "15", "CarlosVergaraChile/coipo-orchestrator", "Prueba")

    def test_invalid_issue(self):
        for issue in ("0", "-1", "1.5", "abc", ""):
            with self.subTest(issue=issue):
                with self.assertRaises(ValueError):
                    module.payload("gemini", issue, "CarlosVergaraChile/coipo-orchestrator", "Prueba")

    def test_unauthorized_repository(self):
        with self.assertRaises(ValueError):
            module.payload("gemini", "1", "OtroUsuario/repo", "Prueba")

    def test_empty_prompt(self):
        with self.assertRaises(ValueError):
            module.payload("gemini", "1", "CarlosVergaraChile/coipo-orchestrator", "  ")

    def test_no_secrets_in_payload(self):
        p = module.payload("gemini", "1", "CarlosVergaraChile/coipo-orchestrator", "8 de 10")
        for key in ("token", "api_key", "password", "webhook"):
            self.assertNotIn(key, p)

if __name__ == "__main__":
    unittest.main()
