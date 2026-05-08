import requests, datetime, hashlib, html as html_module
from xml.etree import ElementTree as ET

tz = datetime.timezone(datetime.timedelta(hours=8))
now = datetime.datetime.now(tz)
today = now.strftime("%Y-%m-%d")
today_time = now.strftime("%Y-%m-%d %H:%M")
days = ["一","二","三","四","五","六","日"]
day_cn = days[now.weekday()]

def fetch_rss(url, max_items=5):
    items = []
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        root = ET.fromstring(r.content)
        for item in root.findall(".//item")[:max_items]:
            title = item.findtext("title", "").strip()
            desc = html_module.unescape(item.findtext("description", "")).strip()
            link = item.findtext("link", "#").strip()
            # 清除 HTML 標籤
            import re
            desc = re.sub(r"<[^>]+>", "", desc)
            if len(desc) > 120:
                desc = desc[:120] + "..."
            if title:
                items.append({"title": title, "desc": desc, "link": link})
    except Exception as e:
        print(f"RSS error ({url}): {e}")
    return items

# 財經新聞：多個來源輪流嘗試
print("抓取財經新聞...")
biz_sources = [
    "https://www.cna.com.tw/rssfeed/wkss0004.xml",   # 中央社財經
    "https://ec.ltn.com.tw/rss/news.xml",              # 自由時報財經
    "https://money.udn.com/rssfeed/news/1001/5613",    # 聯合財經
]
biz_items = []
for src in biz_sources:
    biz_items = fetch_rss(src, 5)
    if biz_items:
        print(f"  來源：{src}")
        break
print(f"財經新聞：{len(biz_items)} 則")

# AI 科技新聞：科技新報
print("抓取科技新聞...")
ai_items = fetch_rss("https://technews.tw/feed/", 8)
# 過濾 AI 相關
ai_keywords = ["ai", "人工智慧", "大模型", "chatgpt", "claude", "gemini", "openai", "llm", "機器學習", "深度學習", "生成式", "gpt", "語言模型"]
ai_filtered = [i for i in ai_items if any(k in i["title"].lower() or k in i["desc"].lower() for k in ai_keywords)]
if len(ai_filtered) < 2:
    ai_filtered = ai_items[:5]  # 若沒有 AI 相關就顯示全部科技新聞
else:
    ai_filtered = ai_filtered[:5]
print(f"科技新聞：{len(ai_filtered)} 則")

# 學習計畫
start = datetime.date(2026, 1, 1)
week_num = (datetime.date.today() - start).days // 7 + 1
if week_num <= 4:
    topic, goal, resource = "Python 基礎與資料處理", "完成 Python 基礎語法練習，學習 list、dict、函式", "Python 官方教學 或 CS50P"
elif week_num <= 8:
    topic, goal, resource = "機器學習基礎概念", "了解監督式學習、損失函數、梯度下降原理", "fast.ai 或 Kaggle Learn"
elif week_num <= 12:
    topic, goal, resource = "神經網路與深度學習", "實作一個簡單的神經網路，理解反向傳播", "fast.ai Part 1 或 3Blue1Brown"
elif week_num <= 16:
    topic, goal, resource = "Transformer 架構與 LLM 原理", "閱讀 Attention Is All You Need 摘要，理解 Self-Attention", "Illustrated Transformer 部落格"
elif week_num <= 20:
    topic, goal, resource = "實作：用 API 串接 Claude/OpenAI", "寫一個呼叫 Claude API 的 Python 腳本，完成一個小工具", "Anthropic 官方文件"
else:
    topic, goal, resource = "進階：微調模型與 Agent 設計", "研究 LoRA 微調或設計一個多步驟 Agent", "HuggingFace 文件、LangChain"

motivations = [
    "每一行程式碼，都是你替未來的自己鋪的路。今天也加油！",
    "學習不是衝刺，是長跑。穩穩地走，終點就在前方。",
    "昨天的你不懂的事，今天的你正在弄懂。這就是成長。",
    "困惑是理解的前一秒。別放棄，答案就快來了。",
    "你不需要完美，你只需要今天比昨天多懂一點。",
]
motivation = motivations[int(hashlib.md5(today.encode()).hexdigest(), 16) % len(motivations)]

def news_cards(items, empty_msg):
    if not items:
        return f'<p style="color:#94a3b8">{empty_msg}</p>'
    cards = []
    for i in items:
        cards.append(f'''<div class="news-item">
      <a class="news-title" href="{i["link"]}" target="_blank">{i["title"]}</a>
      <div class="news-desc">{i["desc"]}</div>
    </div>''')
    return "\n".join(cards)

biz_html = news_cards(biz_items, "今日財經新聞暫時無法取得。")
ai_html = news_cards(ai_filtered, "今日科技新聞暫時無法取得。")

html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>宗聖的每日儀表板 {today}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;background:linear-gradient(135deg,#f0f4f8,#e8edf2);min-height:100vh;padding:20px;color:#1a202c}}
.container{{max-width:860px;margin:0 auto}}
header{{text-align:center;padding:40px 20px 30px}}
header h1{{font-size:2.4rem;color:#4F46E5;font-weight:700}}
header p{{color:#64748b;margin-top:8px;font-size:1.05rem}}
.card{{background:white;border-radius:16px;box-shadow:0 2px 12px rgba(0,0,0,0.08);padding:24px;margin-bottom:20px}}
.card-title{{font-size:1.1rem;font-weight:700;color:#4F46E5;border-left:4px solid #4F46E5;padding-left:12px;margin-bottom:16px}}
.news-item{{padding:14px 0;border-bottom:1px solid #f1f5f9}}
.news-item:last-child{{border-bottom:none}}
a.news-title{{display:block;font-weight:600;color:#1e293b;margin-bottom:6px;font-size:0.95rem;text-decoration:none;line-height:1.5}}
a.news-title:hover{{color:#4F46E5}}
.news-desc{{color:#64748b;font-size:0.875rem;line-height:1.6}}
.study-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.study-item{{background:#f8faff;border-radius:10px;padding:14px}}
.study-label{{font-size:0.75rem;color:#94a3b8;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px}}
.study-value{{font-weight:600;color:#1e293b;font-size:0.95rem;line-height:1.5}}
.motivation{{background:linear-gradient(135deg,#4F46E5,#7C3AED);color:white;border-radius:16px;padding:28px;text-align:center;font-size:1.1rem;line-height:1.8;font-weight:500;margin-bottom:20px}}
footer{{text-align:center;color:#94a3b8;font-size:0.8rem;padding:16px}}
@media(max-width:600px){{.study-grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>早安，宗聖！</h1>
    <p>{today} &nbsp;|&nbsp; 星期{day_cn}</p>
  </header>

  <div class="card">
    <div class="card-title">📈 今日財經新聞</div>
    {biz_html}
  </div>

  <div class="card">
    <div class="card-title">🤖 AI 產業動態</div>
    {ai_html}
  </div>

  <div class="card">
    <div class="card-title">📚 今日學習計畫</div>
    <div class="study-grid">
      <div class="study-item"><div class="study-label">本週主題</div><div class="study-value">{topic}</div></div>
      <div class="study-item"><div class="study-label">第幾週</div><div class="study-value">第 {week_num} 週</div></div>
      <div class="study-item"><div class="study-label">建議時段</div><div class="study-value">上午 10:00–12:00<br>下午 2:00–4:00</div></div>
      <div class="study-item"><div class="study-label">今日目標</div><div class="study-value">{goal}</div></div>
    </div>
    <div style="margin-top:14px;padding:12px;background:#f8faff;border-radius:10px">
      <span style="color:#64748b;font-size:0.875rem">📖 推薦資源：{resource}</span>
    </div>
  </div>

  <div class="motivation">✨ {motivation}</div>
  <footer>由 管家 自動生成 · {today_time}</footer>
</div>
</body>
</html>"""

with open(f"{today}.html", "w", encoding="utf-8") as f:
    f.write(html)
print(f"✅ 生成：{today}.html")
