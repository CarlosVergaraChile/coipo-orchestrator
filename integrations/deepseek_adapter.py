"""Adaptador DeepSeek de prueba: sin red por defecto y sin registrar secretos.

Uso:
  python integrations/deepseek_adapter.py --prompt 'Responde OK'
  DEEPSEEK_API_KEY=... python integrations/deepseek_adapter.py --prompt 'Responde OK' --send
La llamada real requiere autorización explícita y puede generar costos.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

ENDPOINT = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"
MAX_PROMPT = 8000

def build_request(prompt):
    if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > MAX_PROMPT:
        raise ValueError("Prompt vacío o excesivamente largo")
    return {"model": MODEL, "messages": [{"role": "user", "content": prompt}],
            "stream": False, "max_tokens": 256, "temperature": 0}

def extract_answer(data):
    try:
        answer = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("Respuesta DeepSeek sin contenido") from exc
    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("Respuesta DeepSeek vacía")
    return answer

def send(request_data, key, opener=urllib.request.urlopen):
    if not key:
        raise ValueError("Falta DEEPSEEK_API_KEY")
    request = urllib.request.Request(
        ENDPOINT, data=json.dumps(request_data).encode("utf-8"),
        headers={"Authorization": "Bearer " + key,
                 "Content-Type": "application/json"},
        method="POST")
    with opener(request, timeout=25) as response:
        if response.status != 200:
            raise RuntimeError("DeepSeek respondió con estado HTTP no exitoso")
        return extract_answer(json.load(response))

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--send", action="store_true")
    args = parser.parse_args(argv)
    try:
        data = build_request(args.prompt)
        if not args.send:
            print(json.dumps({"mode": "dry-run", "endpoint": ENDPOINT,
                              "request": data}, ensure_ascii=False))
            return 0
        answer = send(data, os.getenv("DEEPSEEK_API_KEY", ""))
        print(json.dumps({"mode": "live", "answer": answer}, ensure_ascii=False))
        return 0
    except (ValueError, RuntimeError, urllib.error.URLError) as exc:
        print("Error del adaptador DeepSeek: " + type(exc).__name__, file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
