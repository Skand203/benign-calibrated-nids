from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

def build_preprocessor(numerical_features, categorical_features):
    """
    Constructs the standard scikit-learn ColumnTransformer.
    - StandardScaler applied to numerical features.
    - OneHotEncoder(handle_unknown='ignore') applied to categorical features.
    """
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )
