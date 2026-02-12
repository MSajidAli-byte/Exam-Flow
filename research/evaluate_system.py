import requests
import json
import time

BACKEND_URL = "http://localhost:8000" # Use localhost since running from host

# Ground Truth for our 4 generated cases
GROUND_TRUTH = {
    "case1_standard_success.zip": {"expected_integrity": "PASS", "expected_grade": "90+"},
    "case2_semantic_variation.zip": {"expected_integrity": "PASS", "expected_grade": "80+"},
    "case3_sudden_logic.zip": {"expected_integrity": "FAIL", "expected_grade": "Low"},
    "case4_gaze_deviation.zip": {"expected_integrity": "FAIL", "expected_grade": "Medium"},
    "case5_library_blind.zip": {"expected_integrity": "PASS", "expected_grade": "Pass"},
    "case6_keyboard_warrior.zip": {"expected_integrity": "PASS", "expected_grade": "Fail"}, # Low Integrity Risk (typing but garbage)
    "case7_thinking_pause.zip": {"expected_integrity": "PASS", "expected_grade": "Pass"}
}

def run_evaluation():
    print("🚀 Starting Scientific Evaluation: Phase 2 (Agentic AI)")
    results = []
    
    for filename, truth in GROUND_TRUTH.items():
        print(f"\n📊 Processing: {filename}")
        file_path = f"research/cases/{filename}"
        
        with open(file_path, "rb") as f:
            files = {"file": (filename, f, "application/zip")}
            params = {
                "assessment_type": "General",
                "enable_proctoring": True
            }
            
            start_time = time.time()
            response = requests.post(f"{BACKEND_URL}/analyze-package", params=params, files=files)
            duration = time.time() - start_time
            
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
                    "report_preview": report[:100] + "..."
                })
                print(f"✅ Completed in {duration:.2f}s. Verdict: {verdict}")
            else:
                print(f"❌ Error: {response.text}")

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

if __name__ == "__main__":
    run_evaluation()
