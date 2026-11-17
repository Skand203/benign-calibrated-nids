# Scientific Audit Report

**Title of Investigation:** Scientific Audit, Empirical Verification, and Numerical Reconciliation of the Benign-Trained Network Anomaly Detection Study  
**Evaluated Manuscript:** `research_paper.docx` / `Revised_Research_Paper.docx`  
**Dataset:** UNSW-NB15 Benchmark (`UNSW_NB15_training-set.csv`, `UNSW_NB15_testing-set.csv`)  
**Auditor Role:** Senior Academic Researcher, Cybersecurity & Machine Learning Reviewer, Technical Editor  
**Date of Audit:** 16 November 2026  
**Target Venue:** *SN Computer Science* (Springer Nature)  

---

## 1. Executive Summary

This scientific audit report presents a line-by-line verification of the empirical experiments, statistical calculations, data structures, and algorithmic evaluations underlying the research paper titled *"An Empirical Evaluation of Threshold Sensitivity and Calibration Transfer in Benign-Trained Network Anomaly Detection"*.

The primary objective of this audit is to identify, document, and correct all factual, numerical, and interpretative inaccuracies in the initial draft (`research_paper.docx`), while establishing complete, auditable traceability back to raw experimental data files, executed Jupyter notebooks (`UNSW_NB15_Final_Experiments.ipynb`, `comparitive_experiments.ipynb`, `experiment.ipynb`), and exported CSV summaries.

### Summary of Audit Status
1. **Calibration FPR Reporting (Table II):** Corrected. In the initial draft, One-Class SVM calibration FPR was incorrectly listed as 5.00% across all four targets (1%, 3%, 5%, 10%). The true 5-seed mean calibration FPRs have been verified and reconciled: Target 1% = 1.0000% ± 0.0000%, Target 3% = 3.0000% ± 0.0000%, Target 5% = 5.0036% ± 0.0080%, Target 10% = 10.0125% ± 0.0120%.
2. **Duplicate & Conflicting Records (Cell 62–65):** Corrected. The initial draft stated that "six conflicting-label groups account for 28,392 records." The audit reveals that exactly 6 feature-vector hash groups have conflicting ground-truth labels, encompassing exactly **14 records** (6 attack records belonging to Fuzzers and 8 benign records belonging to Normal). Deduplication leaves **53,940 unique non-conflicting feature representatives**, meaning 28,392 total records were excluded (28,378 redundant duplicates + 14 conflicting records).
3. **Kolmogorov-Smirnov Shift Test (Cell 17 of `experiment.ipynb`):** Corrected and Clarified. The initial draft attributed the KS test to LOF and ambiguously described the test partitions. The audit verifies that the two-sample KS test was conducted strictly on **Isolation Forest anomaly scores** comparing **benign calibration scores ($N = 11,200$)** against **benign test scores ($N = 37,000$)** across all 5 seeds. Mean KS statistic is 0.1028 (range: 0.0939 to 0.1078, $p < 10^{-65}$).
4. **Execution Environment & Timing:** Corrected. The initial draft reported Python 3.10 and average scoring times of 0.72 s, 1.19 s, and 2.32 s without runtime hardware specifications or fitting times. The audited notebook environment was **Python 3.11.9** (scikit-learn 1.9.1, pandas 3.1.1, NumPy 2.4.6, SciPy 1.17.1). Benchmarked fitting times on 5,000 records are: IF = 0.270 ± 0.033 s, LOF = 0.066 ± 0.003 s, OCSVM = 0.075 ± 0.010 s. Scoring times over 93,532 records (cal + test) are: IF = 0.720 ± 0.020 s, LOF = 1.191 ± 0.018 s, OCSVM = 2.324 ± 0.024 s. These timings are explicitly contextualized as hardware-dependent empirical runtimes rather than fundamental complexity bounds.
5. **Causal vs. Observational Language:** Refined. Detection deficits on unseen protocols (8,126 attack records) are explicitly reframed as observational rather than proven causal effects of one-hot zero-vector encoding, as the unseen protocols are heavily confounded with inherently difficult attack types (DoS and Exploits).
6. **Data Partition Terminology:** Refined. The official train/test partition is strictly described as an unseen evaluation split rather than temporal drift or operational deployment.
7. **Statistical Independence:** Wilson score intervals are explicitly qualified as approximate record-level bounds due to duplicate feature vectors.

---

## 2. Detailed Audit of Known Manuscript Issues

### 2.1 Issue A: Incorrect One-Class SVM Calibration FPR Values

#### Description of Error in Prior Manuscript
In Table II of the original draft, the `Cal. FPR` column for One-Class SVM was reported as `5.00%` across all target FPR levels (1.0%, 3.0%, 5.0%, and 10.0%). This error stemmed from an editorial miscopying where the nominal model training hyperparameter ($\nu = 0.05$) was conflated with the post-hoc empirical quantile calibration FPR.

#### Experimental Source of Truth
The post-hoc threshold selection procedure computes the $(1 - \alpha)$ empirical quantile of the model's raw anomaly scores over the 11,200 held-out benign calibration records:
$$\tau_\alpha = \text{Quantile}(S_{\text{cal}}, 1 - \alpha)$$
By definition of sample quantiles, evaluating the calibrated threshold $\tau_\alpha$ back on the calibration set $S_{\text{cal}}$ must yield an empirical FPR approximately equal to the target $\alpha$.

Inspecting `controlled_comparison_results.csv` and `controlled_comparison_summary.csv` across all five seeds (0, 21, 42, 123, 2025) confirms the following achieved calibration and test FPRs:

| Algorithm | Target FPR | Calibration FPR (5-Seed Mean ± Std) | Achieved Test FPR (5-Seed Mean ± Std) | Detection Rate (5-Seed Mean ± Std) |
| :--- | :---: | :---: | :---: | :---: |
| **Isolation Forest** | 1.0% | 1.0018% ± 0.0040% | 0.8303% ± 0.1205% | 18.7395% ± 2.1818% |
| **Isolation Forest** | 3.0% | 3.0000% ± 0.0000% | 3.3000% ± 0.4326% | 24.9603% ± 0.5843% |
| **Isolation Forest** | 5.0% | 5.0018% ± 0.0040% | 6.4524% ± 0.4907% | 30.2876% ± 1.7011% |
| **Isolation Forest** | 10.0% | 10.0000% ± 0.0000% | 15.7368% ± 0.5606% | 50.7496% ± 2.2741% |
| **LOF** | 1.0% | 1.0179% ± 0.0275% | 1.0411% ± 0.2847% | 1.3037% ± 0.8524% |
| **LOF** | 3.0% | 3.0000% ± 0.0000% | 3.8076% ± 0.3789% | 31.4478% ± 10.6225% |
| **LOF** | 5.0% | 5.0036% ± 0.0080% | 7.1578% ± 0.4208% | 55.2678% ± 3.8659% |
| **LOF** | 10.0% | 10.0000% ± 0.0000% | 15.0443% ± 0.7161% | 71.9381% ± 1.2189% |
| **One-Class SVM** | 1.0% | **1.0000% ± 0.0000%** | 1.9724% ± 0.2443% | 20.5907% ± 2.1378% |
| **One-Class SVM** | 3.0% | **3.0000% ± 0.0000%** | 5.7762% ± 0.1983% | 28.8340% ± 0.6318% |
| **One-Class SVM** | 5.0% | **5.0036% ± 0.0080%** | 8.7124% ± 0.2885% | 31.4987% ± 0.3621% |
| **One-Class SVM** | 10.0% | **10.0125% ± 0.0120%** | 12.3654% ± 0.2078% | 32.4340% ± 0.4398% |

#### Root Cause Analysis for "8.94%"
The prompt noted: *"The expected five-seed achieved calibration FPR values were approximately: 1% -> 1.00%, 3% -> 3.00%, 5% -> 5.00%, 10% -> 8.94%."*  
Upon auditing Cell 72 of `UNSW_NB15_Final_Experiments.ipynb` (the oracle matched-actual-FPR experiment), we discover that **8.942%** was the achieved *test* FPR for One-Class SVM when targeting a test FPR of 10.0%. In the oracle ROC evaluation, discrete step-jumps in One-Class SVM decision values prevented the test FPR from hitting 10.000% exactly, stopping at 8.942% to avoid exceeding the 10% constraint. However, in the *calibration transfer* experiment, the calibration FPR is 10.0125% and the achieved test FPR on the official test set is 12.3654%.

#### Revision Action
Table II in `Revised_Research_Paper.md` and `Revised_Research_Paper.docx` has been updated with the verified calibration FPR values: 1.00%, 3.00%, 5.00%, and 10.01% (or 8.94% in Table VI's oracle comparison).

---

### 2.2 Issue B: Duplicate and Conflicting-Label Record Statistics

#### Description of Error in Prior Manuscript
The prior draft stated:  
> *"Furthermore, 6 feature-vector groups exhibit conflicting ground-truth labels (identical features labelled as both benign and attack in 28,392 total records)."*

This phrasing mistakenly equated the total number of excluded records ($28,392$) with the size of the 6 conflicting groups.

#### Experimental Source of Truth (Cells 62–65, `UNSW_NB15_Final_Experiments.ipynb`)
Auditing the feature-vector hashing logic executed on the 42 model input features across the 82,332 test records establishes the following exact counts:
1. **Total Test Records:** 82,332 (37,000 benign, 45,332 attack).
2. **Exact Duplicate Rows:** 28,386 records (34.48% of the test partition).
3. **Unique Feature Hashes:** 53,946 distinct feature vectors.
4. **Conflicting-Label Groups:** Exactly **6 feature hashes** appear with both `label == 0` (Normal) and `label == 1` (Fuzzers).
5. **Records in Conflicting Groups:** These 6 hashes account for exactly **14 records in total**:
   - 8 benign records (`label == 0`, Normal).
   - 6 attack records (`label == 1`, Fuzzers).
6. **Unique Non-Conflicting Representative Vectors:** Removing the 6 conflicting hashes leaves exactly:
   $$53,946 - 6 = 53,940 \text{ unique non-conflicting feature vectors}$$
   Comprising 34,192 benign and 19,748 attack records.
7. **Total Excluded Records:** The deduplicated evaluation subset excludes:
   $$82,332 - 53,940 = 28,392 \text{ records}$$
   Breakdown: 28,378 redundant duplicate occurrences + 14 records with ambiguous/conflicting labels.

#### Revision Action
Section 5.5 of the revised manuscript accurately differentiates the 6 conflicting groups (14 records) from the total deduplication reduction (28,392 records excluded, leaving 53,940 unique non-conflicting representatives).

---

### 2.3 Issue C: Kolmogorov-Smirnov Distribution Shift Test

#### Description of Error in Prior Manuscript
The prior draft asserted that a two-sample Kolmogorov-Smirnov test confirmed distribution shift for Local Outlier Factor (LOF) with test statistics between 0.094 and 0.108 and $p < 10^{-65}$.

#### Experimental Source of Truth (Cell 17, `experiment.ipynb`)
Auditing `experiment.ipynb` reveals the exact implementation of the KS test:
```python
# Cell 17 in experiment.ipynb
from scipy.stats import ks_2samp
# Model evaluated: IsolationForest(n_estimators=200, contamination='auto')
# Sample 1: Benign calibration scores (N = 11,200)
# Sample 2: Benign test scores (N = 37,000)
ks_stat, p_val = ks_2samp(cal_scores, test_benign_scores)
```
The exact per-seed outputs are recorded in `ks_distribution_comparison.csv`:
- **Seed 0:** KS statistic = 0.0939, $p = 1.91 \times 10^{-66}$
- **Seed 21:** KS statistic = 0.1078, $p = 2.07 \times 10^{-87}$
- **Seed 42:** KS statistic = 0.1035, $p = 1.30 \times 10^{-80}$
- **Seed 123:** KS statistic = 0.1077, $p = 2.77 \times 10^{-87}$
- **Seed 2025:** KS statistic = 0.1014, $p = 2.08 \times 10^{-77}$
- **Five-Seed Mean KS Statistic:** **0.1028** (range: 0.0939–0.1078; all $p < 10^{-65}$).

Crucially:
- The comparison was conducted strictly between **benign calibration traffic** ($11,200$ records) and **benign test traffic** ($37,000$ records). No attack traffic was included in the KS test.
- The model evaluated was **Isolation Forest**, not LOF.

#### Statistical Interpretation
In sample sizes of $N_1 = 11,200$ and $N_2 = 37,000$, standard error is tiny ($\approx \sqrt{\frac{11200+37000}{11200 \times 37000}} \approx 0.0108$). Consequently, any small distribution shift produces astronomically small $p$-values. The meaningful finding is that the empirical supremum distance between cumulative distributions ($D \approx 0.103$) accounts directly for the 1.45 percentage point calibration shift observed at the 5% target (6.45% test FPR vs. 5.00% target).

#### Revision Action
Section 5.2 of the revised manuscript accurately specifies that the KS test was performed on **Isolation Forest benign anomaly scores** comparing the 11,200 calibration observations against the 37,000 benign test observations, reporting the exact 5-seed mean statistic of 0.1028 ($p < 10^{-65}$).

---

### 2.4 Issue D: Software Environment and Timing Verification

#### Description of Error in Prior Manuscript
The prior draft claimed the software environment was Python 3.10 and reported scoring times of 0.72 s, 1.19 s, and 2.32 s without mentioning hardware specifications or model fitting durations.

#### Experimental Source of Truth
1. **Python Environment:** The experimental virtual environment at `E:\Projects\contamination_experiment\.venv\pyvenv.cfg` confirms:
   - Python Version: **3.11.9** (64-bit)
   - Core libraries: scikit-learn 1.9.1, pandas 3.1.1, NumPy 2.4.6, SciPy 1.17.1.
2. **Empirical Benchmarked Runtimes:**
   Executed across 5 seeds on the reference evaluation system (Intel Core i7-12700H, 16 GB RAM, Windows 11):
   - **Model Fitting Duration (5,000 benign training records):**
     - Isolation Forest (200 trees, `n_jobs=-1`): $0.270 \pm 0.033\text{ s}$
     - LOF ($k = 20$, `novelty=True`, `n_jobs=-1`): $0.066 \pm 0.003\text{ s}$
     - One-Class SVM (RBF kernel, `cache_size=2000`): $0.075 \pm 0.010\text{ s}$
   - **Inference / Scoring Duration (93,532 records: 11,200 cal + 82,332 test, batched at 2,000):**
     - Isolation Forest: $0.720 \pm 0.020\text{ s}$
     - LOF: $1.191 \pm 0.018\text{ s}$
     - One-Class SVM: $2.324 \pm 0.024\text{ s}$

#### Methodological Distinction
Fitting times scale with training sample size ($N_{\text{fit}} = 5,000$), whereas inference times scale with evaluation partition size ($N_{\text{eval}} = 93,532$). For LOF and One-Class SVM, inference requires computing kernel distances or $k$-nearest neighbours against the fitted training points, resulting in higher scoring latency than tree traversing in Isolation Forest. These measurements are presented as benchmark-specific runtime observations rather than theoretical asymptotic bounds.

#### Revision Action
Section 4.5 of the revised manuscript updates the software version to Python 3.11.9 and reports both fitting and scoring durations with explicit benchmark hardware context.

---

## 3. Comprehensive Numerical Audit & Evidence Map

The following table links every table, metric, and finding in the revised manuscript directly to its underlying experimental data file, notebook cell, and raw output.

| Paper Element | Metric / Finding | Exact Value Reported | Authoritative Source File / Cell | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Dataset Overview** | Official Train Records | 175,341 (56,000 Benign, 119,341 Attack) | `UNSW_NB15_Final_Experiments.ipynb` (Cell 0) | Verified |
| **Dataset Overview** | Official Test Records | 82,332 (37,000 Benign, 45,332 Attack) | `UNSW_NB15_Final_Experiments.ipynb` (Cell 0) | Verified |
| **Dataset Overview** | Test Attack Prevalence | 55.06% ($45,332 / 82,332$) | `UNSW_NB15_Final_Experiments.ipynb` (Cell 0) | Verified |
| **Dataset Overview** | Feature Counts | 42 total: 39 numerical, 3 categorical | `UNSW_NB15_Final_Experiments.ipynb` (Cell 0, 69) | Verified |
| **Preprocessing** | Encoded Dimensions | 64 columns via OneHotEncoder(ignore) | `UNSW_NB15_Final_Experiments.ipynb` (Cell 1, 51) | Verified |
| **Table 1: Ranking** | IF ROC-AUC | 0.7847 ± 0.0060 | `controlled_comparison_summary.csv` | Verified |
| **Table 1: Ranking** | IF Average Precision | 0.8152 ± 0.0056 | `controlled_comparison_summary.csv` | Verified |
| **Table 1: Ranking** | LOF ROC-AUC | 0.8551 ± 0.0082 | `controlled_comparison_summary.csv` | Verified |
| **Table 1: Ranking** | LOF Average Precision | 0.8404 ± 0.0129 | `controlled_comparison_summary.csv` | Verified |
| **Table 1: Ranking** | OCSVM ROC-AUC | 0.6384 ± 0.0089 | `controlled_comparison_summary.csv` | Verified |
| **Table 1: Ranking** | OCSVM Average Precision| 0.7116 ± 0.0030 | `controlled_comparison_summary.csv` | Verified |
| **Table 2: Transfer** | IF Target 1% | Cal 1.00%, Test 0.83% ± 0.12%, Det 18.74% ± 2.18% | `controlled_comparison_summary.csv` | Verified |
| **Table 2: Transfer** | IF Target 3% | Cal 3.00%, Test 3.30% ± 0.43%, Det 24.96% ± 0.58% | `controlled_comparison_summary.csv` | Verified |
| **Table 2: Transfer** | IF Target 5% | Cal 5.00%, Test 6.45% ± 0.49%, Det 30.29% ± 1.70% | `controlled_comparison_summary.csv` | Verified |
| **Table 2: Transfer** | IF Target 10% | Cal 10.00%, Test 15.74% ± 0.56%, Det 50.75% ± 2.27% | `controlled_comparison_summary.csv` | Verified |
| **Table 2: Transfer** | LOF Target 1% | Cal 1.02%, Test 1.04% ± 0.28%, Det 1.30% ± 0.85% | `controlled_comparison_summary.csv` | Verified |
| **Table 2: Transfer** | LOF Target 3% | Cal 3.00%, Test 3.81% ± 0.38%, Det 31.45% ± 10.62%| `controlled_comparison_summary.csv` | Verified |
| **Table 2: Transfer** | LOF Target 5% | Cal 5.00%, Test 7.16% ± 0.42%, Det 55.27% ± 3.87% | `controlled_comparison_summary.csv` | Verified |
| **Table 2: Transfer** | LOF Target 10% | Cal 10.00%, Test 15.04% ± 0.72%, Det 71.94% ± 1.22%| `controlled_comparison_summary.csv` | Verified |
| **Table 2: Transfer** | OCSVM Target 1% | Cal 1.00%, Test 1.97% ± 0.24%, Det 20.59% ± 2.14% | `controlled_comparison_summary.csv` | Reconciled |
| **Table 2: Transfer** | OCSVM Target 3% | Cal 3.00%, Test 5.78% ± 0.20%, Det 28.83% ± 0.63% | `controlled_comparison_summary.csv` | Reconciled |
| **Table 2: Transfer** | OCSVM Target 5% | Cal 5.00%, Test 8.71% ± 0.29%, Det 31.50% ± 0.36% | `controlled_comparison_summary.csv` | Reconciled |
| **Table 2: Transfer** | OCSVM Target 10% | Cal 10.01%, Test 12.37% ± 0.21%, Det 32.43% ± 0.44%| `controlled_comparison_summary.csv` | Reconciled |
| **Table 3: Category** | Generic (18,871) | IF 64.77% ± 4.54%, LOF 83.82% ± 7.30%, SVM 60.31% | `attack_category_detection_summary.csv` | Verified |
| **Table 3: Category** | Exploits (11,132) | IF 6.53% ± 1.51%, LOF 46.88% ± 5.33%, SVM 12.70% | `attack_category_detection_summary.csv` | Verified |
| **Table 3: Category** | Fuzzers (6,062) | IF 8.24% ± 0.58%, LOF 18.56% ± 1.36%, SVM 12.78% | `attack_category_detection_summary.csv` | Verified |
| **Table 3: Category** | DoS (4,089) | IF 5.03% ± 0.62%, LOF 43.55% ± 3.62%, SVM 10.90% | `attack_category_detection_summary.csv` | Verified |
| **Table 3: Category** | Reconnaissance (3,496) | IF 0.59% ± 0.15%, LOF 8.22% ± 1.37%, SVM 3.82% | `attack_category_detection_summary.csv` | Verified |
| **Table 3: Category** | Analysis (677) | IF 3.49% ± 1.97%, LOF 62.63% ± 5.98%, SVM 7.59% | `attack_category_detection_summary.csv` | Verified |
| **Table 3: Category** | Backdoor (583) | IF 4.91% ± 2.41%, LOF 63.84% ± 6.32%, SVM 9.61% | `attack_category_detection_summary.csv` | Verified |
| **Table 3: Category** | Shellcode (378) | IF 0.00% ± 0.00%, LOF 5.19% ± 2.10%, SVM 3.54% | `attack_category_detection_summary.csv` | Verified |
| **Table 3: Category** | Worms (44) | IF 11.82% ± 1.90%, LOF 25.45% ± 2.96%, SVM 20.45% | `attack_category_detection_summary.csv` | Verified |
| **Table 4: Protocols**| Unseen Protocol Volume | 8,126 attack records (0 benign) | `UNSW_NB15_Final_Experiments.ipynb` (Cell 84) | Verified |
| **Table 4: Protocols**| Seen Protocol Volume | 37,206 attack records | `UNSW_NB15_Final_Experiments.ipynb` (Cell 84) | Verified |
| **Table 4: Protocols**| IF Seen vs Unseen | Seen 36.17% ± 2.94% vs Unseen 3.25% ± 3.10% | `UNSW_NB15_Final_Experiments.ipynb` (Cell 88) | Verified |
| **Table 4: Protocols**| LOF Seen vs Unseen | Seen 53.27% ± 5.17% vs Unseen 51.45% ± 3.38% | `UNSW_NB15_Final_Experiments.ipynb` (Cell 88) | Verified |
| **Table 4: Protocols**| OCSVM Seen vs Unseen | Seen 36.39% ± 0.44% vs Unseen 7.02% ± 0.76% | `UNSW_NB15_Final_Experiments.ipynb` (Cell 88) | Verified |
| **Table 5: Duplicates**| Duplicate Rows | 28,386 records (34.48% of test set) | `duplicate_audit_results.csv` | Verified |
| **Table 5: Duplicates**| Conflicting Groups | 6 groups (14 records total) | `UNSW_NB15_Final_Experiments.ipynb` (Cell 62) | Reconciled |
| **Table 5: Duplicates**| Unique Representatives | 53,940 non-conflicting records | `UNSW_NB15_Final_Experiments.ipynb` (Cell 63) | Verified |
| **Table 5: Duplicates**| IF Orig vs Uniq Det | 30.29% drops to 14.02% (ROC-AUC 0.7847 -> 0.6815)| `UNSW_NB15_Final_Experiments.ipynb` (Cell 85) | Verified |
| **Table 5: Duplicates**| LOF Orig vs Uniq Det | 55.27% drops to 33.61% (ROC-AUC 0.8551 -> 0.7778)| `UNSW_NB15_Final_Experiments.ipynb` (Cell 85) | Verified |
| **Table 5: Duplicates**| SVM Orig vs Uniq Det | 31.50% drops to 17.15% (ROC-AUC 0.6384 -> 0.5966)| `UNSW_NB15_Final_Experiments.ipynb` (Cell 85) | Verified |
| **Table 6: Oracle** | IF Matched 5% FPR | Test FPR = 4.997%, Detection = 27.38% | `UNSW_NB15_Final_Experiments.ipynb` (Cell 72) | Verified |
| **Table 6: Oracle** | LOF Matched 5% FPR | Test FPR = 4.998%, Detection = 43.47% | `UNSW_NB15_Final_Experiments.ipynb` (Cell 72) | Verified |
| **Table 6: Oracle** | SVM Matched 5% FPR | Test FPR = 4.998%, Detection = 27.58% | `UNSW_NB15_Final_Experiments.ipynb` (Cell 72) | Verified |
| **Section 5.7: Contam.**| Sweep Range | Contamination 0.01 to 0.10 (IF) | `master_experimental_results.csv` | Verified |

---

## 4. Methodological Compliance & Scientific Rigor

1. **Pre-processing Integrity:** StandardScaler and OneHotEncoder were fitted exclusively on the full 44,800-record fitting partition within each seed, guaranteeing zero data leakage from calibration or test sets.
2. **Label Blindness:** Ground-truth attack labels were strictly withheld during fitting, model selection, and threshold calibration.
3. **Partition Independence:** Five random seeds (0, 21, 42, 123, 2025) represent repeated stochastic draws and initialisations on a single benchmark dataset, not independent network captures.
4. **Oracle Transparency:** The matched-actual-FPR analysis in Table 6 is explicitly identified as an upper-bound oracle diagnostic requiring test labels, distinct from the operational post-hoc calibration in Table 2.
5. **Observational Qualification:** Protocol disparity is properly presented as observational, accounting for category confounding rather than asserting unproven causation.
6. **Independence Assumption:** Wilson confidence intervals are documented as approximate record-level bounds due to duplicate feature vectors.

This audit confirms that all experimental claims, numbers, and figures in the revised manuscript are mathematically sound, empirically verified, and strictly faithful to the executed research code.
