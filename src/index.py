#!/usr/bin/env python3
"""
paper-explainer — arXiv / DOI / PDF → plain-English summary
Produces: lay summary, key findings, methodology, limitations, related work, jargon glossary
"""
import anthropic
import base64
import json
import re
import sys
import urllib.request
import urllib.parse
from pathlib import Path


SYSTEM = """You are a science communicator who makes complex research accessible.
Explain this academic paper as if talking to a smart person who isn't in the field.

Return ONLY valid JSON — no markdown, no explanation.

Format:
{
  "title": "paper title",
  "authors": ["list of authors"],
  "published": "year or YYYY-MM or YYYY-MM-DD or null",
  "venue": "journal/conference name or null",
  "tldr": "One sentence. What did they do and what did they find?",
  "lay_summary": "3-4 sentences. Explain to a non-expert what this paper is about and why it matters.",
  "problem_statement": "What problem were they trying to solve?",
  "approach": "How did they try to solve it? What methods did they use?",
  "key_findings": [
    "Specific finding 1 — include numbers if mentioned",
    "Specific finding 2",
    "..."
  ],
  "limitations": [
    "Limitation 1 — things the paper itself admits or clear gaps",
    "..."
  ],
  "real_world_impact": "What could change in the real world if this research is applied?",
  "related_work": ["2-3 important related papers or research areas mentioned"],
  "jargon_glossary": {
    "technical term": "plain English definition"
  },
  "difficulty_level": "undergraduate|graduate|expert",
  "fields": ["machine learning", "biology", ...],
  "open_source_code": "URL or null",
  "dataset": "dataset name or null",
  "read_time_minutes": number,
  "confidence": 0.0
}"""


def fetch_arxiv(arxiv_id: str) -> str:
    """Fetch abstract and metadata from arXiv API."""
    clean_id = arxiv_id.replace("https://arxiv.org/abs/", "").replace("arxiv:", "").strip()
    url = f"https://export.arxiv.org/abs/{clean_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "paper-explainer/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="replace")
    # Strip HTML
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)
    return text[:20000]


def fetch_pdf(url: str) -> tuple[str, bytes]:
    """Download a PDF from a URL."""
    req = urllib.request.Request(url, headers={"User-Agent": "paper-explainer/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.headers.get("Content-Type", "application/pdf"), resp.read()


def explain(source: str) -> dict:
    """
    Explain a paper from:
    - arXiv ID: "2301.07041" or "https://arxiv.org/abs/2301.07041"
    - PDF URL: "https://..."
    - Local PDF file path
    - Plain text (pasted abstract or full text)
    """
    client = anthropic.Anthropic()

    # Determine source type
    if source.startswith("http") and ".pdf" in source:
        # PDF URL
        _, pdf_bytes = fetch_pdf(source)
        data = base64.standard_b64encode(pdf_bytes).decode("ascii")
        messages = [{
            "role": "user",
            "content": [
                {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": data}},
                {"type": "text", "text": "Explain this academic paper."}
            ]
        }]

    elif "arxiv.org" in source or re.match(r'^\d{4}\.\d{4,5}$', source):
        # arXiv
        text = fetch_arxiv(source)
        messages = [{"role": "user", "content": f"Explain this academic paper:\n\n{text}"}]

    elif Path(source).exists() and source.endswith(".pdf"):
        # Local PDF
        data = base64.standard_b64encode(Path(source).read_bytes()).decode("ascii")
        messages = [{
            "role": "user",
            "content": [
                {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": data}},
                {"type": "text", "text": "Explain this academic paper."}
            ]
        }]

    else:
        # Plain text (abstract pasted in)
        if len(source) > 50000:
            source = source[:50000]
        messages = [{"role": "user", "content": f"Explain this academic paper:\n\n{source}"}]

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=3000,
        system=SYSTEM,
        messages=messages
    )

    raw = response.content[0].text.strip()
    raw = re.sub(r'^```(?:json)?\s*', '', raw, flags=re.MULTILINE)
    raw = re.sub(r'\s*```$', '', raw, flags=re.MULTILINE)
    return json.loads(raw)


def print_explanation(result: dict):
    print(f"\n{'═'*60}")
    print(f"  {result.get('title', 'Paper')}")
    if result.get("authors"):
        print(f"  {', '.join(result['authors'][:3])}{'...' if len(result.get('authors',[])) > 3 else ''}")
    if result.get("venue"):
        print(f"  {result.get('venue')} {result.get('published','')}")
    print(f"{'═'*60}")

    print(f"\n  TL;DR: {result.get('tldr','')}")
    print(f"\n  {result.get('lay_summary','')}")

    print(f"\n  Problem: {result.get('problem_statement','')}")
    print(f"\n  Approach: {result.get('approach','')}")

    findings = result.get("key_findings", [])
    if findings:
        print(f"\n  Key findings:")
        for f in findings:
            print(f"    • {f}")

    limits = result.get("limitations", [])
    if limits:
        print(f"\n  Limitations:")
        for l in limits:
            print(f"    ⚠ {l}")

    impact = result.get("real_world_impact", "")
    if impact:
        print(f"\n  Real-world impact: {impact}")

    glossary = result.get("jargon_glossary", {})
    if glossary:
        print(f"\n  Jargon explained:")
        for term, defn in list(glossary.items())[:6]:
            print(f"    {term}: {defn}")

    print(f"\n  Fields: {', '.join(result.get('fields', []))}")
    print(f"  Level: {result.get('difficulty_level', '?')}")
    print(f"  Read time: ~{result.get('read_time_minutes', '?')} min")
    if result.get("open_source_code"):
        print(f"  Code: {result['open_source_code']}")
    print(f"{'═'*60}\n")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: python -m paper_explainer <arxiv-id|url|file.pdf|text>")
        print("Examples:")
        print("  python -m paper_explainer 2301.07041")
        print("  python -m paper_explainer https://arxiv.org/abs/2301.07041")
        print("  python -m paper_explainer paper.pdf")
        sys.exit(0)

    source = args[0]
    # If it looks like an arXiv ID passed directly
    if re.match(r'^\d{4}\.\d{4,5}(v\d+)?$', source):
        pass  # already in right format

    result = explain(source)

    if "--json" in args:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_explanation(result)
