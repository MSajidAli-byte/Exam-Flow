# 📝 Revised Section 1: Introduction (Lean & Focused)

The global transition toward remote digital assessment has democratized access to technical education while exposing critical vulnerabilities in academic integrity frameworks. As generative AI tools become increasingly sophisticated, traditional proctoring systems are proving inadequate, creating what researchers term a "critical integrity gap" in digital credentialing.

Current integrity solutions operate within two siloed paradigms: **visual behavioral monitoring** and **static code analysis**. Visual proctoring systems suffer from high false positive rates, misinterpreting benign behaviors (such as thinking pauses) as cheating, while raising significant privacy concerns. Static code analysis tools operate exclusively on final artifacts and cannot distinguish organic development from instantaneous code insertion. The emergence of LLM-generated code has further exposed these limitations.

The fundamental gap is the absence of **forensic triangulation**—the explicit cross-referencing of behavioral patterns against content creation dynamics. A gaze aversion of 0.5 seconds may be benign in isolation, but when it coincides with the instantaneous appearance of complex code, it becomes a high-probability fraud indicator. Current systems lack this cross-modal reasoning capability.

In this paper, we introduce **Exam-Flow**, a multi-agentic framework that synchronizes behavioral monitoring with semantic code analysis through four specialized LLM agents. Our primary contributions are:

1. **Agentic Orchestration Architecture:** A sequentially coordinated multi-agent pipeline enabling specialized AI agents to share multimodal context.
2. **Multimodal Forensic Triangulation:** A methodology correlating behavioral data with code evolution through "Sudden Logic" detection, addressing temporal blindness.
3. **Empirical Validation:** On a curated testbed of diverse fraud scenarios, Exam-Flow achieves an **F1-score of 1.00**, with cached evaluation latency under 0.8 seconds.

The remainder of this paper is organized as follows: Section 2 reviews related work; Section 3 details the architecture; Section 4 describes experimental methodology; Section 5 presents results and comparisons; and Section 6 concludes with limitations and future directions.
