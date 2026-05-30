# paper-explainer

> **arXiv / DOI / PDF → plain-English explanation.** TL;DR, key findings, methodology, limitations, jargon glossary, real-world impact. For any academic paper in any field.

[![PyPI](https://img.shields.io/pypi/v/paper-explainer?style=flat)](https://pypi.org/project/paper-explainer/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Quickstart

```bash
pip install paper-explainer

# From arXiv ID
python -m paper_explainer 2301.07041

# From arXiv URL
python -m paper_explainer https://arxiv.org/abs/2301.07041

# From local PDF
python -m paper_explainer attention_is_all_you_need.pdf
```

## Example output

```
TL;DR: They propose a new neural architecture using only attention
mechanisms — no convolutions or recurrence — that outperforms
previous models on translation tasks with less compute.

Problem: RNNs are slow to train (sequential) and struggle with
long-range dependencies.

Approach: Replace recurrence with self-attention entirely,
allowing full parallelization and direct connections between
any two positions.

Key findings:
  • 28.4 BLEU on WMT English-to-German (new SOTA at time)
  • Trains 3× faster than previous best models
  • Scales better with data and model size

Jargon explained:
  attention: a mechanism that lets the model focus on relevant
             parts of the input when generating each output token
  BLEU: a score (0-100) measuring translation quality
```

## License
MIT © [Alper Nabil Gabra Zakher](https://github.com/AlperNab)
