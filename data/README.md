# Data Directory Instructions: UNSW-NB15 Dataset

This research project evaluates anomaly detection algorithms on the **UNSW-NB15** network intrusion detection benchmark dataset.

In accordance with academic redistribution best practices and file size limits, the raw dataset CSV files are **not tracked in this Git repository**.

---

## 1. Obtaining the Dataset

The official UNSW-NB15 dataset is publicly provided by the Australian Centre for Cyber Security (ACCS):

- **Official ACCS Repository:** [https://research.unsw.edu.au/projects/unsw-nb15-dataset](https://research.unsw.edu.au/projects/unsw-nb15-dataset)
- **Primary Citation:**  
  Nour Moustafa and Jill Slay, *"UNSW-NB15: A comprehensive data set for network intrusion detection systems (UNSW-NB15 network data set)"*, in 2015 Military Communications and Information Systems Conference (MilCIS), Canberra, ACT, Australia, 2015, pp. 1–6. DOI: [10.1109/MilCIS.2015.7348942](https://doi.org/10.1109/MilCIS.2015.7348942)

---

## 2. Expected Files and Placement

Download the pre-partitioned CSV files from the repository:

1. `UNSW_NB15_training-set.csv` (approx. 32.3 MB, 175,341 records)
2. `UNSW_NB15_testing-set.csv` (approx. 15.4 MB, 82,332 records)

Place these two CSV files in the project root directory or in this `data/` directory:

```text
benign-calibrated-nids/
├── UNSW_NB15_training-set.csv
├── UNSW_NB15_testing-set.csv
└── data/
    └── README.md
```

*(Note: The primary execution notebook `notebooks/UNSW_NB15_Final_Experiments.ipynb` accesses `UNSW_NB15_training-set.csv` and `UNSW_NB15_testing-set.csv` from the root directory by default).*

---

## 3. Dataset Ground Truth Specifications

| Partition | Total Records | Benign (Normal) | Attack Records | Attack Prevalence |
| :--- | :---: | :---: | :---: | :---: |
| **Official Training Set** | 175,341 | 56,000 | 119,341 (excluded) | 68.06% |
| **Official Testing Set** | 82,332 | 37,000 | 45,332 | 55.06% |

- **Benign-Trained Paradigm:** Only the 56,000 benign records from the training set are utilised for model development (partitioned 80/20 into 44,800 fitting and 11,200 calibration records). The 119,341 training attack records are completely excluded from benign model fitting.
- **Features Used:** 42 features total (39 numerical features and 3 categorical features: `proto`, `service`, `state`). Three metadata columns are excluded: `id`, `attack_cat`, and `label`.
