"""Pruebas sin red ni credenciales para el adaptador DeepSeek."""
import contextlib
import importlib.util
import io
import json
import pathlib
import unittest

PATH = pathlib.Path(__file__).resolve().parents[1] / "integrations" / "deepseek_adapter.py"
spec = importlib.util.spec_from_file_location("deepseek_adapter", PATH)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)

class FakeResponse(io.BytesIO):
    status = 200
    def __enter__(self):
        return self
    def __exit__(self, *args):
        self.close()

class AdapterTests(unittest.TestCase):
    def test_dry_run_without_key(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(adapter.main(["--prompt", "8 de 10"]), 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["mode"], "dry-run")
        self.assertEqual(result["model"], "deepseek-chat")
        self.assertEqual(result["max_tokens"], 256)
        self.assertEqual(result["prompt_length"], 7)
        self.assertEqual(len(result["prompt_sha256"]), 64)
        self.assertNotIn("8 de 10", output.getvalue())
        self.assertNotIn("messages", result)

    def test_invalid_prompts(self):
        for prompt in ("", "   ", "a" * 8001):
            with self.subTest(length=len(prompt)), self.assertRaises(ValueError):
                adapter.build_request(prompt)

    def test_missing_key(self):
        with self.assertRaises(ValueError):
            adapter.send(adapter.build_request("test"), "")

    def test_mocked_response(self):
        calls = []
        def fake_opener(request, timeout):
            calls.append((request, timeout))
            return FakeResponse(b'{"choices":[{"message":{"content":"80%"}}]}')
        answer = adapter.send(adapter.build_request("8 de 10"), "TEST_ONLY", fake_opener)
        self.assertEqual(answer, "80%")
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][0].full_url, adapter.ENDPOINT)
        self.assertEqual(calls[0][1], 25)
        self.assertEqual(calls[0][0].get_method(), "POST")

    def test_bad_response(self):
        for payload in ({}, {"choices": []}, {"choices": [{"message": {"content": ""}}]}):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                adapter.extract_answer(payload)

if __name__ == "__main__":
    unittest.main()
