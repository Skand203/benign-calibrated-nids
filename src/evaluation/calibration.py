import numpy as np

def score_samples_batched(model, X, batch_size=2000):
    """
    Computes negated anomaly scores in batches. Higher score = more anomalous.
    """
    n_samples = X.shape[0] if hasattr(X, "shape") else len(X)
    scores = []
    for start in range(0, n_samples, batch_size):
        end = min(start + batch_size, n_samples)
        batch = X[start:end]
        batch_scores = -model.score_samples(batch)
        scores.append(batch_scores)
    return np.concatenate(scores)

def calibrate_quantile_threshold(calibration_scores, target_fpr):
    """
    Computes the (1 - target_fpr) empirical quantile threshold from benign calibration scores.
    """
    return np.quantile(calibration_scores, 1.0 - target_fpr)
