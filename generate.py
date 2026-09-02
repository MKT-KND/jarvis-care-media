import os
import sys
import google.generativeai as genai

# --- 広告コードここから ---
AD_CODE = """
<a href="https://px.a8.net/svt/ejp?a8mat=4BC1MM+DFFZZM+54PG+601S1" rel="nofollow">
<img border="0" width="468" height="60" alt="" src="https://www20.a8.net/svt/bgt?aid=260902462812&wid=001&eno=01&mid=s00000023938001008000&mc=1"></a>
<img border="0" width="1" height="1" src="https://www17.a8.net/0.gif?a8mat=4BC1MM+DFFZZM+54PG+601S1" alt="">
"""
# --- 広告コードここまで ---

print("=== START GENERATE SCRIPT ===")

# 1. APIキーのチェック
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("FATAL ERROR: GEMINI_API_KEY is empty or not found in environment variables!")
    sys.exit(1)
else:
    print(f"API Key detected (length: {len(api_key)})")

# 2. Geminiの初期化
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = "医療・介護・福祉に役立つ簡単なケアアドバイスを1つ作成してください。HTMLのタグ（<h3>と<p>）を使って出力してください。"
    print("Sending prompt to Gemini API...")
    
    response = model.generate_content(prompt)
    ai_text = response.text
    print("Successfully received response from Gemini API!")

except Exception as e:
    print(f"CRITICAL API ERROR: {type(e).__name__} - {e}")
    ai_text = f"<h3>本日のケアガイド</h3><p>AI通信エラーが発生しました: {e}</p>"

# 3. HTMLファイルの書き出し
html_code = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>医療・介護・福祉の暮らし知恵袋</title>
    <style>
        body {{ font-family: sans-serif; background: #f0f4f8; margin: 0; padding: 15px; color: #333; line-height: 1.6; }}
        header {{ background: #2c7a7b; color: white; padding: 20px; text-align: center; border-radius: 10px; margin-bottom: 20px; }}
        h1 {{ margin: 0; font-size: 1.3rem; }}
        .card {{ background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; }}
        .card h3 {{ color: #2c7a7b; margin-top: 0; }}
        .ad-box {{ background: #edf2f7; border: 2px dashed #cbd5e0; padding: 15px; text-align: center; border-radius: 8px; font-size: 0.9rem; margin-top: 15px; overflow-x: auto; }}
    </style>
</head>
<body>
    <header>
        <h1>医療・介護・福祉の暮らし知恵袋</h1>
    </header>
    <div class="card">
        {ai_text}
    </div>
    <div class="card">
        <div style="font-weight:bold; margin-bottom:10px; text-align:center;">💡 おすすめ福祉・介護サービス</div>
        <div class="ad-box">
            {AD_CODE}
        </div>
    </div>
</body>
</html>"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("=== FINISHED GENERATE SCRIPT ===")
