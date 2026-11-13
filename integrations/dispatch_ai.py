#!/usr/bin/env python3
"""Dispatch a GitHub task to an authorized Zapier/n8n webhook.
No secrets in repository. Dry-run is default. Python standard library only.
"""
import argparse, json, os, sys, urllib.request, urllib.error, uuid
from datetime import datetime, timezone

ALLOWED = {"manus", "gemini", "deepseek", "perplexity", "claude"}
def payload(provider, issue, repo, prompt):
    if provider not in ALLOWED: raise ValueError("unsupported provider")
    if not issue.isdigit() or int(issue)<1: raise ValueError("invalid issue")
    if not repo.startswith("CarlosVergaraChile/"): raise ValueError("repository not authorized")
    if not prompt.strip(): raise ValueError("empty prompt")
    return {"schema":"idg.ai-task.v1","task_id":f"{repo}#{issue}:{provider}",
      "provider":provider,"issue_number":int(issue),"repository":repo,
      "instructions":prompt,"requested_at":datetime.now(timezone.utc).isoformat(),
      "requires_human_approval_for":["deploy","merge","delete","outbound_contact"]}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--provider",required=True,choices=sorted(ALLOWED))
    ap.add_argument("--issue",required=True)
    ap.add_argument("--repo",default="CarlosVergaraChile/coipo-orchestrator")
    ap.add_argument("--prompt",required=True)
    ap.add_argument("--send",action="store_true")
    args=ap.parse_args()
    data=payload(args.provider,args.issue,args.repo,args.prompt)
    if not args.send:
        print(json.dumps({"mode":"dry-run","payload":data},ensure_ascii=False,indent=2));return
    url=os.environ.get("IDG_AUTOMATION_WEBHOOK")
    token=os.environ.get("IDG_AUTOMATION_TOKEN")
    if not url or not token or not url.startswith("https://"):
        sys.exit("Missing secure IDG_AUTOMATION_WEBHOOK or IDG_AUTOMATION_TOKEN")
    req=urllib.request.Request(url,data=json.dumps(data).encode(),
      headers={"Content-Type":"application/json","Authorization":"Bearer "+token,
      "Idempotency-Key":data["task_id"]},method="POST")
    try:
        with urllib.request.urlopen(req,timeout=20) as response:
            print(json.dumps({"http_status":response.status,"task_id":data["task_id"]}))
    except urllib.error.URLError as e:sys.exit("Dispatch failed: "+str(e))
if __name__=="__main__":main()
