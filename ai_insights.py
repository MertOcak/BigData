# -*- coding: utf-8 -*-
"""
AI-powered data summary — generates a short English insight from the dataset.
Uses OPENAI_API_KEY if set; otherwise skipped.
"""

import os


def _get_openai_client():
    """Return OpenAI client if available; otherwise None."""
    try:
        from openai import OpenAI
        api_key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not api_key:
            return None
        return OpenAI(api_key=api_key)
    except ImportError:
        return None


def generate_insights(summary: dict, describe_text: str, correlation_text: str = "") -> str | None:
    """
    Generate a short English summary and recommendations from the data overview.

    Args:
        summary: Output of analyzer.summary() (keys: row_count, column_count, etc.)
        describe_text: Numeric describe output as string
        correlation_text: Correlation matrix as string (optional)

    Returns:
        English insight text or None if API unavailable or error
    """
    client = _get_openai_client()
    if not client:
        return None

    prompt = f"""Below is a statistical summary of a dataset. Based on it:
1) Summarize the data in 2–3 sentences.
2) Briefly note anything notable (outliers, distribution, missing data).
3) Give 1–2 practical recommendations for analysis or business intelligence.

Respond in English only, concisely (at most 6–7 sentences). No headings, just a short paragraph.

DATA SUMMARY:
- Row count: {summary.get('row_count', '?')}
- Column count: {summary.get('column_count', '?')}
- Numeric columns: {summary.get('numeric_columns', [])}
- Categorical columns: {summary.get('categorical_columns', [])}
- Missing values: {summary.get('missing_values', {})}

Numeric statistics:
{describe_text[:1500]}
"""
    if correlation_text:
        prompt += f"\nCorrelation (summary):\n{correlation_text[:500]}\n"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.5,
        )
        text = response.choices[0].message.content
        return text.strip() if text else None
    except Exception:
        return None
