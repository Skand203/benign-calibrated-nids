# An Empirical Evaluation of Threshold Sensitivity and Calibration Transfer in Benign-Trained Network Anomaly Detection

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3119/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.9.1-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Official research repository containing the complete experimental codebase, statistical auditing pipelines, diagnostic analyses, and evaluation outputs for the study:

> **"An Empirical Evaluation of Threshold Sensitivity and Calibration Transfer in Benign-Trained Network Anomaly Detection"**  
> *Preprint / Research Paper under review.*

---

## 1. Project Overview

Anomaly-based network intrusion detection systems (NIDS) are conventionally framed around an appealing operational premise: by modelling normative behaviour strictly on benign network traffic, an intrusion detector can identify novel, zero-day attacks without requiring exhaustive historical attack signatures. In high-throughput network monitoring, however, the practical viability of such detectors is governed by their **false-positive rate (FPR)**. As demonstrated by Axelsson (2000) through the base-rate fallacy, even a 1% false alarm rate can overwhelm security operations centres (SOCs) with thousands of unmanageable daily alerts.

Consequently, practitioners must establish a decision threshold on historical benign validation traffic to cap false alarms at a sustainable operational budget $\alpha$ (e.g., 1%, 3%, or 5%). Despite this requirement, machine learning literature predominantly evaluates anomaly detectors using threshold-independent summary metrics (e.g., ROC-AUC) or assumes an "oracle" setting where thresholds are tuned directly on labelled test traffic.

This research investigates **calibration transfer divergence**: the empirical phenomenon whereby operating thresholds calibrated on historical benign traffic fail to maintain their target false-positive rates when transferred to an independent evaluation environment. Furthermore, the study evaluates detection capability across heterogeneous attack families and uncovers how structural benchmark artefacts distort reported performance.

---

## 2. Central Research Questions

1. **Detection Efficacy Across Threat Heterogeneity:** To what extent can benign-trained anomaly detection algorithms identify diverse network attack categories when evaluated on the official UNSW-NB15 test partition?
2. **Reliability of Calibration Transfer:** How reliably can operating thresholds calibrated on benign validation observations maintain target false-positive rates on an independent test partition, and what governs the magnitude of calibration transfer loss?
3. **Influence of Benchmark Artefacts:** How do structural dataset properties—specifically categorical vocabulary mismatch (unseen transport protocols) and extensive feature-vector duplication—influence observed anomaly detection performance?

---

## 3. Evaluated Algorithms & Configurations

Three foundational one-class anomaly detection algorithms are evaluated under controlled, label-blind configurations:

- **Isolation Forest (Tree-Based Partitioning):**
  - Number of estimators: $n_{\text{estimators}} = 200$
  - Subsample per tree: `max_samples="auto"` (scikit-learn default, evaluating to $\min(256, n) = 256$ for $n = 5,000$)
  - Sampling: Tree subsampling without replacement
  - Scoring: Negated `score_samples()` (higher score monotonically denotes higher anomaly severity)
  - Random state: Seed-pinned (`[0, 21, 42, 123, 2025]`)
- **Local Outlier Factor (LOF) (Density-Based Neighbourhoods):**
  - Mode: Novelty detection (`novelty = True`)
  - Neighbourhood size: $k = 20$ neighbours (`n_neighbors = 20`)
  - Distance metric: Euclidean / Minkowski ($p = 2$)
  - Scoring: Negated `score_samples()` relative to the fitted benign neighbourhood graph
- **One-Class Support Vector Machine (Kernel Boundary Estimation):**
  - Kernel: Radial Basis Function (RBF Gaussian kernel)
  - Gamma: Auto-scaled (`gamma = 'scale'`, $\gamma = \frac{1}{d \cdot \text{Var}(X)}$)
  - Regularisation: $\nu = 0.05$ (`nu = 0.05`)
  - Memory cache: 2,000 MB (`cache_size = 2000`)
  - Scoring: Negated decision function

---

## 4. Dataset & Experimental Partitions

Evaluations are conducted on the widely cited **UNSW-NB15** network intrusion benchmark (Moustafa & Slay, 2015).

### Partitioning & Volume Ground Truth:
- **Official Training Partition ($N = 175,341$):**
  - **Benign records:** 56,000 (31.94%) — retained for model development.
  - **Attack records:** 119,341 (68.06%) — **strictly excluded** from benign model fitting and calibration.
- **Official Testing Partition ($N = 82,332$):**
  - **Benign records:** 37,000 (44.94%).
  - **Attack records:** 45,332 (55.06%) across 9 categories: Generic (18,871), Exploits (11,132), Fuzzers (6,062), DoS (4,089), Reconnaissance (3,496), Analysis (677), Backdoor (583), Shellcode (378), and Worms (44).
  - Preserved intact as an unseen evaluation partition. Test labels are strictly sequestered during all fitting and threshold selection stages.
- **Feature Space (42 Retained Features):**
  - 39 continuous numerical flow features (standardised via `StandardScaler`).
  - 3 categorical features: `proto`, `service`, `state` (encoded via `OneHotEncoder(handle_unknown='ignore')`).
  - Metadata columns excluded: `id`, `attack_cat`, and `label`.

### Multi-Seed Controlled Subsampling Protocol:
- **Preprocessing Fitting Partition ($N = 44,800$):** 80% split of benign training data used exclusively to fit the `ColumnTransformer`. (Ensures full training vocabulary is captured; produces 64 encoded columns).
- **Benign Calibration Partition ($N = 11,200$):** Held-out 20% split used strictly for empirical quantile threshold selection.
- **Detector Fitting Sample ($n = 5,000$):** Due to quadratic $\mathcal{O}(n^2)$ computational complexity of kernel and distance methods, each model is fitted on an identical 5,000-record sample drawn uniformly from the fitting partition via `np.random.default_rng(seed).choice(len(X_fit_full), size=5000, replace=False)`.
- **Five Experimental Seeds:** Evaluated across seeds `0, 21, 42, 123, 2025`. (These represent repeated stochastic draws and initialisations on a single benchmark dataset, not five independent network captures).

---

## 5. Main Empirical Findings

### A. Primary Experiment: Five-Seed Threshold-Independent Ranking
Evaluated across the 82,332 official test records using the primary NumPy choice sampling protocol (`notebooks/UNSW_NB15_Final_Experiments.ipynb`, Cell 62; exported in [`results/main/controlled_comparison_summary.csv`](results/main/controlled_comparison_summary.csv)):

| Algorithm | ROC-AUC (mean ± std) | Average Precision (mean ± std) | Primary Result File |
| :--- | :---: | :---: | :--- |
| **Isolation Forest** | $0.7847 \pm 0.0060$ | $0.8152 \pm 0.0056$ | [`results/main/controlled_comparison_summary.csv`](results/main/controlled_comparison_summary.csv) |
| **Local Outlier Factor (LOF)** | $\mathbf{0.8551 \pm 0.0082}$ | $\mathbf{0.8404 \pm 0.0129}$ | [`results/main/controlled_comparison_summary.csv`](results/main/controlled_comparison_summary.csv) |
| **One-Class SVM** | $0.6384 \pm 0.0089$ | $0.7116 \pm 0.0030$ | [`results/main/controlled_comparison_summary.csv`](results/main/controlled_comparison_summary.csv) |

*LOF achieves superior global ranking due to its density-ratio formulation, which accommodates multi-modal benign clusters without creating artificial global hulls.*

### B. Primary Experiment: Threshold Calibration Transfer Divergence
Thresholds calibrated to enforce target FPRs on the 11,200 benign calibration set systematically diverge when transferred to the 82,332 test set ([`results/main/controlled_comparison_summary.csv`](results/main/controlled_comparison_summary.csv)):

| Algorithm | Target FPR | Calibration FPR | Achieved Test FPR | Detection Rate | Alert Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Isolation Forest** | 1.0% | 1.00% | $0.83\% \pm 0.12\%$ | $18.74\% \pm 2.18\%$ | $10.69\% \pm 1.24\%$ |
| **Isolation Forest** | 3.0% | 3.00% | $3.30\% \pm 0.43\%$ | $24.96\% \pm 0.58\%$ | $15.22\% \pm 0.49\%$ |
| **Isolation Forest** | 5.0% | 5.00% | $6.45\% \pm 0.49\%$ | $30.29\% \pm 1.70\%$ | $19.58\% \pm 1.11\%$ |
| **Isolation Forest** | 10.0% | 10.00% | $15.74\% \pm 0.56\%$ | $50.75\% \pm 2.27\%$ | $35.01\% \pm 1.48\%$ |
| **LOF** | 1.0% | 1.02% | $1.04\% \pm 0.28\%$ | **$1.30\% \pm 0.85\%$** | $1.19\% \pm 0.57\%$ |
| **LOF** | 3.0% | 3.00% | $3.81\% \pm 0.38\%$ | $31.45\% \pm 10.62\%$ | $19.03\% \pm 5.97\%$ |
| **LOF** | 5.0% | 5.00% | $7.16\% \pm 0.42\%$ | $55.27\% \pm 3.87\%$ | $33.65\% \pm 2.18\%$ |
| **LOF** | 10.0% | 10.00% | $15.04\% \pm 0.72\%$ | $71.94\% \pm 1.22\%$ | $46.37\% \pm 0.72\%$ |
| **One-Class SVM** | 1.0% | 1.00% | $1.97\% \pm 0.24\%$ | $20.59\% \pm 2.14\%$ | $12.22\% \pm 1.20\%$ |
| **One-Class SVM** | 3.0% | 3.00% | $5.78\% \pm 0.20\%$ | $28.83\% \pm 0.63\%$ | $18.47\% \pm 0.37\%$ |
| **One-Class SVM** | 5.0% | 5.00% | $8.71\% \pm 0.29\%$ | $31.50\% \pm 0.36\%$ | $21.26\% \pm 0.25\%$ |
| **One-Class SVM** | 10.0% | 10.01% | $12.37\% \pm 0.21\%$ | $32.43\% \pm 0.44\%$ | $23.41\% \pm 0.29\%$ |

- **Critical Operational Trade-off:** While LOF achieves the highest overall ROC-AUC, its detection rate collapses to just **1.30%** at the conservative 1.0% calibration target.
- **Benign Score Distribution Shift:** A two-sample Kolmogorov-Smirnov test comparing benign calibration scores against benign test scores across all 5 seeds confirms a statistically significant shift (mean $D = 0.1028$, $p < 10^{-65}$; [`results/diagnostics/ks_distribution_comparison.csv`](results/diagnostics/ks_distribution_comparison.csv)). Test benign traffic exhibits heavier anomaly score tails, causing empirical test FPRs to overshoot targets by 1.4 to 5.7 percentage points.

### C. Supplementary Experiment: Attack Category Heterogeneity (5% Target)
Evaluated across all 9 attack categories ([`results/categories/attack_category_detection_summary.csv`](results/categories/attack_category_detection_summary.csv)):
- **Generic Attacks Dominate Metrics:** Generic attacks comprise 41.6% of attack traffic and are detected with high recall ($60.3\%$ to $83.8\%$), heavily inflating aggregate detection metrics.
- **Stealthy Attacks are Missed:** Stealthy threats are virtually undetected: Reconnaissance detection is under 8.3% across all models (0.59% for Isolation Forest), and Shellcode detection is strictly 0.00% for Isolation Forest and under 5.2% for LOF.
- **Multi-Vector Threat Separation:** LOF decisively outperforms Isolation Forest and One-Class SVM on Analysis ($62.63\%$ vs. $3.49\%$ and $7.59\%$), Backdoor ($63.84\%$ vs. $4.91\%$ and $9.61\%$), and DoS ($43.55\%$ vs. $5.03\%$ and $10.90\%$).

### D. Supplementary Experiment: Benchmark Duplication & Sensitivity
- Row-hash auditing reveals that **28,386 test records (34.48%) are exact duplicates** ([`results/duplicates/duplicate_audit_results.csv`](results/duplicates/duplicate_audit_results.csv)). Duplication is heavily concentrated in attacks (56.44% duplicate) versus benign traffic (7.57% duplicate).
- Exactly **6 feature-vector hash groups (14 records total)** carry conflicting labels (Normal vs. Fuzzers).
- In a deduplicated evaluation of **53,940 unique non-conflicting feature representatives**, detection rates drop by more than half across all algorithms (IF: $30.29\% \to 14.02\%$; LOF: $55.27\% \to 33.61\%$; OCSVM: $31.50\% \to 17.15\%$).

### E. Supplementary Experiment: Protocol Familiarity & LOF Resilience
*Methodological Note on Sampling:* The protocol group analysis is a supplementary investigation executed in Cell 51 using pandas dataframe `.sample(n=5000, random_state=seed)` on the benign training dataframe (whereas the primary benchmark in Cell 62 uses NumPy choice index sampling on preprocessed feature matrices). Both methods draw valid, reproducible 5,000-record samples; results are exported in [`results/protocols/protocol_group_detection_summary.csv`](results/protocols/protocol_group_detection_summary.csv) and [`results/protocols/protocol_group_per_seed_runs.csv`](results/protocols/protocol_group_per_seed_runs.csv):

| Algorithm | Seen Protocols (37,206 attacks) | Unseen Protocols (8,126 attacks) | Disparity (Unseen − Seen) | Export File |
| :--- | :---: | :---: | :---: | :--- |
| **Isolation Forest** | $36.17\% \pm 2.94\%$ | $3.25\% \pm 3.10\%$ | $-32.92\%$ | [`results/protocols/protocol_group_detection_summary.csv`](results/protocols/protocol_group_detection_summary.csv) |
| **Local Outlier Factor (LOF)** | $\mathbf{53.27\% \pm 5.17\%}$ | $\mathbf{51.45\% \pm 3.38\%}$ | $\mathbf{-1.82\%}$ | [`results/protocols/protocol_group_detection_summary.csv`](results/protocols/protocol_group_detection_summary.csv) |
| **One-Class SVM** | $36.39\% \pm 0.44\%$ | $7.02\% \pm 0.76\%$ | $-29.37\%$ | [`results/protocols/protocol_group_detection_summary.csv`](results/protocols/protocol_group_detection_summary.csv) |

While tree and kernel models experience sharp drops on unseen protocols (partially confounded with difficult DoS and Exploit types), LOF maintains steady detection ($53.27\%$ vs. $51.45\%$), demonstrating density resilience on continuous numerical dimensions even when categorical dimensions default to zeros.

### F. Supplementary Diagnostic: LOF Score Magnitudes on Seed 42
Detailed diagnostic inspection (Cells 12–28) on Seed 42 revealed that extreme LOF calibration scores ($\sim 10^6$, peaking at 917,870.04) were driven by sparse ARP protocol transactions occurring in tight local clusters where training neighbours had near-zero distance to other training points, resulting in massive neighbour local reachability densities ($LRD$). Deduplicating training observations reduced peak scores by orders of magnitude while preserving overall ranking ROC-AUC ($0.8645 \to 0.8672$). This demonstrates that local density anomalies in network traffic are sensitive to discrete transactional replication.

### G. Supplementary Analysis: Oracle Matched-FPR Upper Bound
To isolate calibration transfer error from inherent scoring separation limits, an oracle test-label-informed threshold selection was executed ([`results/oracle/oracle_matched_fpr_summary.csv`](results/oracle/oracle_matched_fpr_summary.csv)):
- At 5.0% matched FPR, oracle detection rates are: IF = 27.38%, LOF = 43.47%, One-Class SVM = 27.58%.
- *Non-deployable:* This analysis requires ground-truth test labels and serves solely as an upper-bound diagnostic.

---

## 6. Repository Structure

```text
benign-calibrated-nids/
├── README.md                           # Comprehensive empirical overview, methodology & results
├── LICENSE                             # Open-source MIT License
├── CITATION.cff                        # Machine-readable citation metadata
├── requirements.txt                    # Verified Python dependencies (Python 3.11.9 stack)
├── .gitignore                          # Clean exclusions (data CSVs, .venv, caches, drafts)
│
├── notebooks/
│   └── UNSW_NB15_Final_Experiments.ipynb  # Primary executed experimental notebook
│
├── src/                                # Modular, reusable pipeline code
│   ├── preprocessing/
│   │   └── pipeline.py                 # ColumnTransformer (StandardScaler + OneHotEncoder)
│   ├── models/
│   │   └── detectors.py                # Isolation Forest (auto/256), LOF (novelty), One-Class SVM
│   ├── evaluation/
│   │   └── calibration.py              # Batched scoring & empirical quantile calibration
│   └── utils/
│
├── results/                            # Audited, consistent final experimental outputs
│   ├── main/                           # Primary multi-seed transfer & ranking results
│   │   ├── controlled_comparison_results.csv   # Per-seed main ranking & transfer runs
│   │   ├── controlled_comparison_summary.csv   # 5-seed mean/std ranking & transfer metrics
│   │   ├── calibration_validation_all_runs.csv # Calibration validation per-seed runs
│   │   └── calibration_validation_summary.csv  # Calibration validation summary
│   ├── categories/                     # Granular 9-category detection outputs
│   │   ├── attack_category_detection_results.csv # Per-seed 9-category detection rates
│   │   ├── attack_category_detection_summary.csv # 5-seed mean/std 9-category metrics
│   │   ├── attack_category_all_seeds.csv         # Preliminary per-seed category metrics
│   │   └── attack_category_summary.csv           # Category summary table
│   ├── duplicates/                     # Feature-vector duplication audit
│   │   └── duplicate_audit_results.csv           # 42-feature row-hash duplicate audit
│   ├── protocols/                      # Seen vs. unseen protocol group outputs
│   │   ├── protocol_group_detection_summary.csv  # Overall protocol group summary
│   │   ├── protocol_group_per_seed_runs.csv      # Per-seed protocol group runs
│   │   └── protocol_group_by_category_summary.csv# Category-stratified protocol breakdown
│   ├── oracle/                         # Upper-bound matched-actual-FPR analysis
│   │   └── oracle_matched_fpr_summary.csv        # Upper-bound matched-actual-FPR comparison
│   └── diagnostics/                    # Statistical shift & distribution tests
│       └── ks_distribution_comparison.csv        # Kolmogorov-Smirnov score shift statistics
│
├── figures/                            # Publication-ready 300 DPI visualizations
│   ├── fig1_threshold_transfer.png
│   ├── fig2_attack_category_comparison.png
│   ├── fig3_protocol_group_detection.png
│   ├── fig4_duplicate_sensitivity.png
│   ├── contamination_robustness.png
│   └── ranking_metrics_robustness.png
│
├── docs/                               # In-depth technical documentation
│   ├── methodology.md                  # Comprehensive scientific audit & evidence map
│   ├── experiment_reproduction.md      # Detailed step-by-step reproduction instructions
│   └── references.md                   # Verified academic literature registry
│
├── archive/                            # Historical exploratory notebooks & preliminary sweeps
│   ├── experiment.ipynb                # Initial single-detector exploratory notebook
│   ├── comparative_experiments.ipynb   # Intermediate comparative sweeps
│   ├── master_experimental_results.csv # Contamination sweep summary
│   ├── robustness_all_runs.csv         # Contamination sweep runs
│   ├── robustness_summary.csv          # Contamination summary statistics
│   ├── threshold_transfer_all_runs.csv # Preliminary threshold transfer runs
│   ├── threshold_transfer_summary.csv  # Preliminary threshold transfer summary
│   ├── isolation_forest_results.csv    # Early IF preliminary results
│   └── ranking_metrics.csv             # Early ranking metrics
│
└── data/
    └── README.md                       # Download & placement instructions for UNSW-NB15
```

---

## 7. Installation & Reproduction

### Prerequisites
- Python 3.11 (tested on Python 3.11.9, 64-bit)
- Standard scientific stack (`scikit-learn==1.9.1`, `pandas==3.1.1`, `numpy==2.4.6`, `scipy==1.17.1`)

### Quick Start
```bash
# 1. Clone repository
git clone https://github.com/Skand203/benign-calibrated-nids.git
cd benign-calibrated-nids

# 2. Set up virtual environment
python -m venv .venv

# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Place official UNSW-NB15 CSV files in root directory
# (See data/README.md for download instructions)

# 5. Launch Jupyter and execute notebook
jupyter lab notebooks/UNSW_NB15_Final_Experiments.ipynb
```

For detailed guidance, see [`docs/experiment_reproduction.md`](docs/experiment_reproduction.md).

---

## 8. Reproducibility & Limitations

1. **Benchmark Realism:** UNSW-NB15 was generated in a cyber range testbed using IXIA traffic engines; synthetic flow generation introduces structural regularities absent from production enterprise backbones.
2. **Subsampling Invariant:** Detectors were fitted on 5,000-record benign samples (11.16% of the fitting split) to facilitate kernel and nearest-neighbour distance scaling. Multi-seed replication demonstrates narrow variance.
3. **Partition Nature:** The official train/test partition does not represent longitudinal operational concept drift over months of real traffic; calibration transfer gaps reflect partition differences rather than validated live concept drift.
4. **Statistical Independence:** Wilson confidence intervals represent approximate record-level bounds due to duplicate feature vectors violating sample independence.

---

## 9. Citation

If you use this codebase, empirical methodology, or evaluation data in your academic work, please cite:

```bibtex
@misc{shukla2026benigncalibratednids,
  author       = {Skand Shukla and Kapil Verma and Yash Vardhan Singh and Vyom Shanker Tewari and Varchas Kumar Pandey},
  title        = {An Empirical Evaluation of Threshold Sensitivity and Calibration Transfer in Benign-Trained Network Anomaly Detection},
  year         = {2026},
  howpublished = {Preprint / GitHub Repository},
  url          = {https://github.com/Skand203/benign-calibrated-nids}
}
```

---

## 10. License

This repository is licensed under the [MIT License](LICENSE).
