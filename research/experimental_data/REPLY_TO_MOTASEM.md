# 💬 Proposed Reply to Motasem

Salam Motasem,

Thank you for the detailed feedback. These are exactly the points we need to tighten to ensure a smooth peer-review process. Here is how I am addressing your concerns in the paper draft:

1. **Redundancy (Sec 1 & 2):** I agree. I have refactored the **Introduction** to be a "Lean" high-level "Problem-Gap-Solution" narrative (approx. 3 paragraphs). All specific technical histories of CV and static analysis are being moved to **Section 2 (Related Work)** to avoid repetitive content.
2. **The "Golden Set" & Sample Size:** The 'Golden Set' refers to a **Curated Benchmark of Ground-Truth Extremes**. While it is currently 4 videos, these aren't random samples; they represent the 4 critical failure modes of current AI proctoring (Honest, Sudden Logic/Paste, Paradigm Tampering, and High-Speed Gaze Micro-aversions). I have explicitly defined this in Section 4 as our "Expert-weighted proof-of-concept testbed" so reviewers understand its purpose.
3. **Comparison of Contributions:** In the **Discussion (Section 5)**, I added a 'Detection Capability Matrix.' This table explicitly contrasts Exam-Flow against baseline Unimodal (Visual-only) and Static (Code-only) systems, showing exactly where they fail and we succeed (e.g., False Positives vs. Triangulated Verification).
4. **Reproducibility:** I added a specific "Reproducibility" subsection to Section 4. It clarifies that our pipeline, local evaluation scripts (`evaluate_system.py`), and standardized `.zip` demo packages are bundled to independently verify the 1.00 F1-score metric.
5. **References:** I agree the list is long. We will prune this down to only the most "load-bearing" citations that directly support our multimodal triangulation claims, making the bibliography much more focused.

I have updated the drafts for the Introduction, Methodology, and Discussion to reflect this tighter scientific structure!

Best regards,
Muhammad
