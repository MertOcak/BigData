# -*- coding: utf-8 -*-
"""
Yapay zeka destekli veri özeti - veri seti hakkında Türkçe insight üretir.
OPENAI_API_KEY ortam değişkeni tanımlıysa kullanılır; yoksa atlanır.
"""

import os
import json


def _get_openai_client():
    """OpenAI istemcisini döndürür; yoksa None."""
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
    Veri özetine göre Türkçe kısa yorum ve öneri üretir.
    
    Args:
        summary: analyzer.summary() çıktısı
        describe_text: sayısal describe metni
        correlation_text: korelasyon matrisi metni (opsiyonel)
    
    Returns:
        Türkçe insight metni veya None (API yok/hatada)
    """
    client = _get_openai_client()
    if not client:
        return None

    prompt = f"""Aşağıda bir veri setinin istatistik özeti var. Bu veriye dayanarak:
1) 2-3 cümleyle veriyi özetle,
2) Dikkat çeken noktaları (uç değerler, dağılım, eksik veri) kısaca belirt,
3) İş zekası veya analiz için 1-2 pratik öneri ver.

Yanıtı sadece Türkçe, net ve kısa tut (en fazla 6-7 cümle). Başlık ekleme, sadece paragraf yaz.

VERİ ÖZETİ:
- Satır sayısı: {summary.get('satır_sayısı', '?')}
- Sütun sayısı: {summary.get('sütun_sayısı', '?')}
- Sayısal sütunlar: {summary.get('sayısal_sütunlar', [])}
- Kategorik sütunlar: {summary.get('kategorik_sütunlar', [])}
- Eksik değerler: {summary.get('eksik_değerler', {})}

Sayısal istatistikler:
{describe_text[:1500]}
"""
    if correlation_text:
        prompt += f"\nKorelasyon (özet):\n{correlation_text[:500]}\n"

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
