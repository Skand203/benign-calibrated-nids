from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM

def get_models(seed=42):
    """
    Returns the three evaluated models configured identically to the primary experiments.
    
    Notes on Isolation Forest:
    - In scikit-learn, max_samples defaults to 'auto', which sets max_samples = min(256, n_samples).
    - For the primary experiment's training subsample of n = 5,000 observations, max_samples='auto'
      evaluates to exactly 256. Specifying max_samples='auto' ensures full fidelity to the primary
      experimental notebook (UNSW_NB15_Final_Experiments.ipynb, Cell 62).
    """
    models = {
        "Isolation Forest": IsolationForest(
            n_estimators=200,
            max_samples="auto",
            bootstrap=False,
            random_state=seed,
            n_jobs=-1,
        ),
        "Local Outlier Factor": LocalOutlierFactor(
            n_neighbors=20,
            novelty=True,
            n_jobs=-1,
        ),
        "One-Class SVM": OneClassSVM(
            kernel="rbf",
            gamma="scale",
            nu=0.05,
            cache_size=2000,
        ),
    }
    return models
