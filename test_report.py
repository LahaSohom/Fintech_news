# test_report.py
import time
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

RUNS_TO_TEST = 3
MIN_ARTICLES = 3
MIN_BRANDED_RATIO = 0.6

# ── Import your agent ───────────────────────────────
from agents import run_agent


def measure_llm_latency():
    """
    Measures Groq LLM response speed and availability.
    """
    from openai import OpenAI

    # Disable platform header collection to avoid Windows WMI errors
    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        default_headers={"X-Stainless-OS": "windows"}  # override problematic header
    )

    models = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"]
    results = {}

    print("\n🤖 Testing LLM Latency...")
    for model in models:
        start = time.time()
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Summarize: AI in fintech"}],
                temperature=0.4,
                max_tokens=50
            )
            elapsed = round(time.time() - start, 2)
            results[model] = {"latency_seconds": elapsed, "status": "✅ pass"}
            print(f"   {model}: {elapsed}s | ✅ pass")
        except Exception as e:
            elapsed = round(time.time() - start, 2)
            results[model] = {"latency_seconds": elapsed, "status": f"❌ error: {str(e)[:60]}"}
            print(f"   {model}: {elapsed}s | ❌ error")
    return results


def measure_end_to_end():
    """
    Runs the full agent pipeline and measures latency and article quality.
    """
    print(f"\n🔄 Running End-to-End Test ({RUNS_TO_TEST} runs)...")
    runs = []

    for i in range(RUNS_TO_TEST):
        start = time.time()
        try:
            articles = run_agent()
            elapsed = round(time.time() - start, 2)

            if not articles:
                runs.append({
                    "run": i + 1,
                    "latency_seconds": elapsed,
                    "articles_returned": 0,
                    "branded_ratio": 0,
                    "success": False,
                    "error": "No articles returned"
                })
                print(f"   Run {i+1}: ❌ failed ({elapsed}s)")
            else:
                branded = sum(1 for a in articles if any(
                    b.lower() in a.get("source", "").lower()
                    for b in ["techcrunch", "finextra", "pymnts", "bloomberg", "reuters"]
                ))
                runs.append({
                    "run": i + 1,
                    "latency_seconds": elapsed,
                    "articles_returned": len(articles),
                    "branded_ratio": round(branded / len(articles), 2),
                    "success": len(articles) >= MIN_ARTICLES
                })
                print(f"   Run {i+1}: ✅ {len(articles)} articles ({elapsed}s)")
        except Exception as e:
            elapsed = round(time.time() - start, 2)
            runs.append({
                "run": i + 1,
                "latency_seconds": elapsed,
                "articles_returned": 0,
                "branded_ratio": 0,
                "success": False,
                "error": str(e)[:80]
            })
            print(f"   Run {i+1}: ❌ exception ({elapsed}s)")
        time.sleep(2)  # small delay between runs
    return runs


def generate_report(llm_metrics, e2e_runs):
    """
    Generates a full observability report and prints it.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    successful = [r for r in e2e_runs if r["success"]]
    success_rate = round(len(successful) / len(e2e_runs) * 100, 1) if e2e_runs else 0
    avg_latency = round(sum(r["latency_seconds"] for r in e2e_runs) / len(e2e_runs), 2) if e2e_runs else 0

    print("\n" + "=" * 60)
    print("📊 OBSERVABILITY REPORT")
    print(f"   Generated: {now}")
    print("=" * 60)

    print("\n🎯 SUCCESS RATE")
    print(f"   {success_rate}%  ({len(successful)}/{len(e2e_runs)} runs passed)")
    print("   Status:", "🟢 GOOD" if success_rate >= 80 else "🟡 DEGRADED")

    print("\n⏱ LATENCY")
    print(f"   Average end-to-end: {avg_latency}s")
    for r in e2e_runs:
        icon = "✅" if r["success"] else "❌"
        print(f"   Run {r['run']}: {icon} {r['latency_seconds']}s")

    print("\n📰 ARTICLE QUALITY")
    if successful:
        avg_articles = round(sum(r["articles_returned"] for r in successful) / len(successful), 1)
        avg_branded = round(sum(r["branded_ratio"] for r in successful) / len(successful), 2)
        print(f"   Avg articles returned: {avg_articles}")
        print(f"   Avg branded ratio:     {int(avg_branded*100)}%")

    print("\n🤖 LLM PERFORMANCE")
    for model, m in llm_metrics.items():
        print(f"   {model}: {m['status']} | {m['latency_seconds']}s")

    print("\n💡 RECOMMENDATIONS")
    if success_rate >= 80:
        print("   ✅ System is healthy — no action needed")
    else:
        print("   ⚠ Investigate pipeline reliability")

    print("=" * 60)


if __name__ == "__main__":
    print("🚀 Starting observability check...\n")
    llm_metrics = measure_llm_latency()
    e2e_runs = measure_end_to_end()
    generate_report(llm_metrics, e2e_runs)
