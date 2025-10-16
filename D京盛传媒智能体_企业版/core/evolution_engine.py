import os, openai, json, datetime
openai.api_key = os.getenv("OPENAI_API_KEY")

LOG_PATH = "logs/runtime.log"
EVOLUTION_REPORT = "logs/evolution_suggestions.json"

def read_logs(n_chars=5000):
    if not os.path.exists(LOG_PATH):
        return "无日志"
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        return f.read()[-n_chars:]

def analyze_logs_with_gpt():
    logs = read_logs()
    prompt = f"""你是系统工程师。请阅读下面运行日志，给出：
1) 问题总结
2) 改进建议（按优先级）
3) 需要修改的文件与示例代码片段（不直接覆盖）
日志：
{logs}
请用中文输出。"""
    if not os.getenv("OPENAI_API_KEY"):
        raise Exception("OPENAI_API_KEY 未配置")
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        max_tokens=800
    )
    suggestions = resp["choices"][0]["message"]["content"]
    os.makedirs("logs", exist_ok=True)
    json.dump({"time":datetime.datetime.utcnow().isoformat(),"suggestions":suggestions}, open(EVOLUTION_REPORT,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    return suggestions
