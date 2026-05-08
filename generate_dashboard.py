import requests, json, datetime, hashlib, html as html_module
from xml.etree import ElementTree as ET

tz = datetime.timezone(datetime.timedelta(hours=8))
now = datetime.datetime.now(tz)
today = now.strftime("%Y-%m-%d")
today_time = now.strftime("%Y-%m-%d %H:%M")
days = ["一","二","三","四","五","六","日"]
day_cn = days[now.weekday()]

biz_items = []
try:
    r = requests.get("https://feeds.bbci.co.uk/news/business/rss.xml", timeout=15)
    root = ET.fromstring(r.content)
    for item in root.findall(".//item")[:5]:
        title = item.findtext("title", "")
        desc = html_module.unescape(item.findtext("description", ""))
        if len(desc) > 200: desc = desc[:200] + "..."
        biz_items.append({"title": title, "desc": desc})
except Exception as e:
    print(f"BIZ error: {e}")

ai_items = []
try:
    r = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
    ids = r.json()[:40]
    keywords = ["ai","llm","gpt","claude","gemini","openai","anthropic","neural","agent","mistral","transformer","model"]
    for sid in ids:
        if len(ai_items) >= 3: break
        try:
            s = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=5).json()
            if any(k in s.get("title","").lower() for k in keywords):
                ai_items.append({"title": s.get("title"), "url": s.get("url","https://news.ycombinator.com")})
        except:
            continue
except Exception as e:
    print(f"HN error: {e}")

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

biz_html = "".join(
    f'<div class="news-item"><div class="news-title">{i["title"]}</div><div class="news-desc">{i["desc"]}</div></div>'
    for i in biz_items
) or '<p style="color:#94a3b8">今日財經新聞暫時無法取得。</p>'

ai_html = "".join(
    f'<div class="news-item"><div class="news-title"><a href="{i["url"]}" class="news-link" target="_blank">{i["title"]}</a></div></div>'
    for i in ai_items
) or '<p style="color:#94a3b8">今日 AI 動態暫時無法取得。</p>'

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
.news-title{{font-weight:600;color:#1e293b;margin-bottom:6px;font-size:0.95rem}}
.news-desc{{color:#64748b;font-size:0.875rem;line-height:1.6}}
.news-link{{color:#4F46E5;text-decoration:none}}
.study-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.study-item{{background:#f8faff;border-radius:10px;padding:14px}}
.study-label{{font-size:0.75rem;color:#94a3b8;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px}}
.study-value{{font-weight:600;color:#1e293b;font-size:0.95rem}}
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
