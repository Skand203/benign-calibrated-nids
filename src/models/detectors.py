from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM

def get_models(seed=42):
    """
    Returns the three evaluated models configured identically to the final experiments.
    """
    models = {
        "Isolation Forest": IsolationForest(
            n_estimators=200,
            max_samples=256,
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
