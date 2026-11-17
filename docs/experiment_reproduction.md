# Experiment Reproduction Guide

This guide provides step-by-step instructions for reproducing the entire empirical evaluation of benign-trained network anomaly detection on the UNSW-NB15 dataset.

---

## 1. Environment Setup

### Prerequisites
- Python 3.11 (tested on Python 3.11.9, 64-bit).
- Git.
- Recommended: Windows 10/11 or Linux x86_64 with at least 8 GB RAM.

### Step 1: Clone the Repository
```bash
git clone https://github.com/Skand203/benign-calibrated-nids.git
cd benign-calibrated-nids
```

### Step 2: Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 2. Obtain and Position Dataset

1. Download the official CSV files from the Australian Centre for Cyber Security (ACCS):
   - `UNSW_NB15_training-set.csv`
   - `UNSW_NB15_testing-set.csv`
2. Place both files in the root directory of this repository:
   ```text
   benign-calibrated-nids/
   ├── UNSW_NB15_training-set.csv
   ├── UNSW_NB15_testing-set.csv
   ```

---

## 3. Execution Pipeline

### Running via Jupyter Notebook
Launch your preferred Jupyter environment (VS Code, JupyterLab, or Jupyter Notebook):
```bash
jupyter lab
```
Open `notebooks/UNSW_NB15_Final_Experiments.ipynb`.

### Execution Order & Structure
1. **Cells 0–1:** Load raw dataset, verify partition shapes (175,341 train, 82,332 test), filter the 56,000 benign records, and define numerical and categorical feature lists.
2. **Cells 2–11:** Preliminary benchmark setup and metric calculation functions.
3. **Cells 12–30:** In-depth diagnostic investigation of LOF score behavior and ARP protocol density dynamics on Seed 42.
4. **Cells 50–52:** Controlled multi-seed protocol group evaluation across 5 random seeds (`[0, 21, 42, 123, 2025]`).
5. **Cells 57–65:** Row-hash audit, duplicate feature vector analysis, conflicting label resolution, and generation of the 53,940 unique non-conflicting test subset.
6. **Cell 62:** Execution of the controlled 5-seed comparative evaluation across Isolation Forest, LOF, and One-Class SVM on both original (82,332) and deduplicated (53,940) test sets using the exact `np.random.default_rng(seed).choice()` subsampling.
7. **Cell 72:** Upper-bound oracle matched-actual-FPR analysis across all 5 seeds.
8. **Cells 76–89:** Generation of final summary tables and category detection rates.

---

## 4. Key Methodological Invariants

When reproducing or extending these experiments, the following experimental invariants must be strictly maintained to preserve parity with published findings:
- **Seed Set:** Exact seeds used: `0, 21, 42, 123, 2025`.
- **Sampling Routine:** Must use `np.random.default_rng(seed).choice(len(X_fit_full), size=5000, replace=False)`.
- **Preprocessor Fitting:** `ColumnTransformer(StandardScaler, OneHotEncoder)` must be fitted exclusively on the full 44,800-record benign fitting partition, never on the 5,000 subsample or test data.
- **Label Sequestering:** Ground-truth labels from the official test partition are never accessed during model fitting, preprocessor fitting, or threshold selection.
