"""Entrainement du modele baseline M0 : Regression Lineaire sur 3 features neutres.
Ce modele volontairement simple sert de reference de depart dans le Brief 1.
"""

from pathlib import Path
import joblib
import pandas as pd
from loguru import logger
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

DATA_PATH = Path(__file__).resolve().parent / "credit_risk_dataset.csv"
MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_OUTPUT_PATH = MODEL_DIR / "credit_linear_model.joblib"

FEATURES = ["montant_demande", "duree_mois", "revenu_mensuel"]
TARGET = "score_credit"


def train_baseline():
    logger.info("Chargement du dataset depuis {path}", path=DATA_PATH)
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Fichier dataset introuvable : {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    logger.info("Dataset charge : {n} lignes, {p} colonnes", n=len(df), p=len(df.columns))

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    logger.info("Separation train/test : {tr} train, {te} test", tr=len(X_train), te=len(X_test))

    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluation
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5

    logger.success("Entrainement termine avec succes !")
    logger.info("Coefficients : {c}", c=dict(zip(FEATURES, model.coef_.round(4))))
    logger.info("Intercept : {i:.2f}", i=model.intercept_)
    logger.info("Metriques Test : R2 = {r2:.3f} | MAE = {mae:.2f} pts | RMSE = {rmse:.2f} pts", r2=r2, mae=mae, rmse=rmse)

    # Sauvegarde
    bundle = {
        "model": model,
        "features": FEATURES,
        "metrics": {"r2": r2, "mae": mae, "rmse": rmse},
    }
    joblib.dump(bundle, MODEL_OUTPUT_PATH)
    logger.success("Modele baseline sauvegarde dans : {path}", path=MODEL_OUTPUT_PATH)
    return bundle


if __name__ == "__main__":
    train_baseline()
