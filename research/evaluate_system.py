import requests
import json
import time

BACKEND_URL = "http://localhost:8000" # Use localhost since running from host

# Ground Truth for our Curated Research Trials (The "Golden Dataset")
GROUND_TRUTH_CURATED = {
    "trial1_honest.zip": {"expected_integrity": "PASS", "label": "True Negative"},
    "trial2_sudden_logic.zip": {"expected_integrity": "FAIL", "label": "True Positive (Paste)"},
    "trial3_paradigm_mismatch.zip": {"expected_integrity": "FAIL", "label": "True Positive (Tamper)"},
    "trial4_gaze_aversion.zip": {"expected_integrity": "FAIL", "label": "True Positive (Gaze)"}
}

# Legacy Synthetic Cases (Phase 1 Baseline)
GROUND_TRUTH_SYNTHETIC = {
    "case1_standard_success.zip": {"expected_integrity": "PASS"},
    "case2_semantic_variation.zip": {"expected_integrity": "PASS"},
    "case3_sudden_logic.zip": {"expected_integrity": "FAIL"},
    "case4_gaze_deviation.zip": {"expected_integrity": "FAIL"}
}


def run_evaluation():
    print("🚀 Starting Scientific Evaluation: Phase 2 (Agentic AI)")
    print("📋 Evaluation Mode: CURATED RESEARCH TRIALS")
    results = []
    
    for filename, truth in GROUND_TRUTH_CURATED.items():
        print(f"\n📊 Processing: {filename}")
        
        # Handle both running from project root and from research/ directory
        import os
        if os.path.exists(f"cases/{filename}"):
            file_path = f"cases/{filename}"
        else:
            file_path = f"research/cases/{filename}"
        
        with open(file_path, "rb") as f:
            files = {"file": (filename, f, "application/zip")}
            params = {
                "assessment_type": "General",
                "enable_proctoring": True
            }
            
            print(f"⏳ Sending to backend (this takes ~60s per case)...")
            start_time = time.time()
            
            try:
                # Timeout set to 180s to account for model fallback cycling (6 models × 2s + 4 agents × 10s + buffer)
                response = requests.post(
                    f"{BACKEND_URL}/analyze-package", 
                    params=params, 
                    files=files,
                    timeout=300
                )
                duration = time.time() - start_time
                print(f"✅ Response received in {duration:.1f}s")
                
                if response.status_code == 200:
                    data = response.json()
                    report = data.get("report", "")
                    
                    # Simple extraction of verdict from report markdown
                    verdict = "FAIL" if "FAIL" in report or "SUSPICIOUS" in report else "PASS"
                    
                    results.append({
                        "case": filename,
                        "actual_verdict": verdict,
                        "expected_verdict": truth["expected_integrity"],
                        "latency": f"{duration:.2f}s",
                        "report_preview": report[:100] + "...",
                        "is_cached": data.get("source") == "Cached Research Result"
                    })
                    print(f"✅ Completed in {duration:.2f}s. Verdict: {verdict}")
                else:
                    print(f"❌ Backend Error {response.status_code}: {response.text[:200]}")
                    
            except requests.exceptions.Timeout:
                print(f"⏰ Timeout after 300s - Agentic analysis is taking longer than expected.")

            except requests.exceptions.ConnectionError as e:
                print(f"🔌 Connection Error: {str(e)[:100]}")
            except Exception as e:
                print(f"❌ Unexpected Error: {str(e)[:100]}")
        
        # Only cool down if we actually hit the AI API (not a cache hit)
        if results and results[-1].get("is_cached"):
            print("🚀 Cache Hit - Skipping cooldown.")
        else:
            print("⏳ Cooling down before next case (30s)...")
            time.sleep(30)

    # Calculate Metrics
    tp = sum(1 for r in results if r["actual_verdict"] == "FAIL" and r["expected_verdict"] == "FAIL")
    fp = sum(1 for r in results if r["actual_verdict"] == "FAIL" and r["expected_verdict"] == "PASS")
    tn = sum(1 for r in results if r["actual_verdict"] == "PASS" and r["expected_verdict"] == "PASS")
    fn = sum(1 for r in results if r["actual_verdict"] == "PASS" and r["expected_verdict"] == "FAIL")

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    print("\n" + "="*40)
    print("📈 FINAL RESEARCH METRICS (Phase 2)")
    print("="*40)
    print(f"Precision: {precision:.2f} (How accurate are cheater flags?)")
    print(f"Recall:    {recall:.2f} (How many cheaters did we catch?)")
    print(f"F1-Score:  {f1:.2f} (Balanced accuracy)")
    print("="*40)

    # Export to a Research Table (Markdown)
    print("\n📑 RESEARCH PAPER TABLE (Copy for Motasem):")
    print("| Case Study | Expected | Actual | Validated | Latency |")
    print("|---|---|---|---|---|")
    for r in results:
        status = "✅" if r["actual_verdict"] == r["expected_verdict"] else "❌"
        print(f"| {r['case']} | {r['expected_verdict']} | {r['actual_verdict']} | {status} | {r['latency']} |")


if __name__ == "__main__":
    run_evaluation()
