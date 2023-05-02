from typing import Dict

from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
import requests


def download_data(url: str, data_csv: str) -> None:
    if Path(data_csv).exists():
        return
    
    response = requests.get(url)
    with Path(data_csv).open("wb") as f:
        f.write(response.content)


def load_data(data_csv: str) -> pd.DataFrame:
    col_names = ["buying", "maint", "doors", "persons", "lug_boot", "safety", "class"]
    dtype = {col: "category" for col in col_names}
    df = pd.read_csv(data_csv, dtype=dtype, header=None, names=col_names)
    return df


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    df = (
        df.astype("category")
        .assign(**{
            "maint": lambda df: df["maint"].cat.set_categories(["low", "med", "high", "vhigh"], ordered=True),
            "doors": lambda df: df["doors"].cat.set_categories(["2", "3", "4", "5more"], ordered=True),
            "persons": lambda df: df["persons"].cat.set_categories(["2", "4", "more"], ordered=True),
            "lug_boot": lambda df: df["lug_boot"].cat.set_categories(["small", "med", "big"], ordered=True),
            "safety": lambda df: df["safety"].cat.set_categories(["low", "med", "high"], ordered=True),
            "class": lambda df: df["class"].cat.set_categories(["unacc", "acc", "good", "vgood"], ordered=True),
        })
    )
    return df
  

def process_labels(labels: pd.Series) -> pd.Series:
    labels = (
        labels.cat.reorder_categories(["low", "med", "high", "vhigh"], ordered=True)
        .cat.codes
    )
    return labels


def prepare_dataset(df: pd.DataFrame, **kwargs) -> lgb.Dataset:
    label_name = "buying"
    exclude_col_names = []
    excluded = exclude_col_names + [label_name]

    features = df.drop(columns=excluded)
    labels = process_labels(df[label_name])

    params = {"feature_pre_filter": False}
    dataset = lgb.Dataset(features, labels, params=params, **kwargs)
    return dataset


def model_train(df: pd.DataFrame, model_path="model.lgb") -> lgb.Booster:
    train = prepare_dataset(df)
    num_class = len(df["class"].unique())
    params = {
        "objective": "multiclass",
        "num_class": num_class,
        "metrics": ["multi_logloss"],
        "boosting": "gbdt",
        "force_row_wise": True,
        "first_metric_only": True,
        "is_unbalanced": True,
    }
    model = lgb.train(
        params, 
        train,
        num_boost_round=1000,
    )
    model.save_model(model_path)
    return model


def process_scores(scores: np.ndarray) -> str:
    buying_classes = ["low", "med", "high", "vhigh"]
    return np.array(buying_classes)[scores.argmax(axis=1)]


def model_predict(model_path, data: Dict[str, str]) -> str:
    model = lgb.Booster(model_file=model_path)
    feature_name = model.feature_name()

    data = {name: data.get(name) for name in feature_name}
    df = process_data(pd.DataFrame([data], columns=feature_name))

    scores = model.predict(df)
    return process_scores(scores)[0]


if __name__ == "__main__":
    data_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/car/car.data"
    data_csv = "car.data"

    download_data(data_url, data_csv)

    df = load_data(data_csv)
    df = process_data(df)

    model_path = "model.lgb"
    model = model_train(df, model_path)

    predict_data = {"maint": "high", "doors": '4', "lug_boot": "big", "safety": "high", "class": "good"}
    buying_pred = model_predict(model_path, predict_data)
    
    print(f"for the following input: {predict_data}.")
    print(f"the predicted buying price is: {buying_pred}.")
