import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
import lightgbm as lgb

from common import label_encoding

def run_cv_lgb(x, y):
    params = {
            "objective": "binary",
            "num_leaves": 31,
            "bagging_freq": 1,
            "bagging_fraction": 0.1,
            "feature_fraction": 0.1
            }
    train_data = lgb.Dataset(x, label=y)
    eval_hist = lgb.cv(params=params, train_set=train_data, metrics="auc")
    print("Lightgbm best accuracy: %f" % max(eval_hist["auc-mean"]))

def run_cv_lr(x, y):
    n_splits = 5
    skf = StratifiedKFold(n_splits=n_splits)
    mean = 0.0

    for train_idx, test_idx in skf.split(x, y):
        x_train, x_test = x.iloc[train_idx], x.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        lr = LogisticRegression()
        lr.fit(x_train, y_train)

        score = lr.score(x_test, y_test)
        mean += score
        print(score)

    print("Logistic Regression mean accuracy: %f" % (mean / n_splits))

def run_cv_dtc(x, y):
    n_splits = 5
    skf = StratifiedKFold(n_splits=n_splits)
    mean = 0.0

    for train_idx, test_idx in skf.split(x, y):
        x_train, x_test = x.iloc[train_idx], x.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        dtc = DecisionTreeClassifier()
        dtc.fit(x_train, y_train)

        score = dtc.score(x_test, y_test)
        mean += score
        print(score)

    print("Decision Tree mean accuracy: %f" % (mean / n_splits))

def feature_engineering(pokemon, combats):
    pokemon["mix_type"] = pokemon["Type_1"] + "-" + pokemon["Type_2"]
    combats["Winner"] = (combats["Winner"] == combats["First_pokemon"])
    pokemon.drop(columns=["Name"], axis=1, inplace=True)

    label_encoding(pokemon, "Type_1")
    label_encoding(pokemon, "Type_2")
    label_encoding(pokemon, "mix_type")

def load_data(fname):
    data = pd.read_csv(fname)
    columns = data.columns
    rename_dict = {}

    for col in columns:
        rep = col
        rep = rep.replace(" ", "_")
        rep = rep.replace(".", "")
        rename_dict[col] = rep

    data.rename(columns=rename_dict, inplace=True)

    return data

def main():
    pokemon = load_data("data/pokemon.csv")
    combats = load_data("data/combats.csv")
    pokemon.fillna("nan", inplace=True)
    feature_engineering(pokemon, combats)

    m1 = combats.merge(pokemon, left_on="First_pokemon", right_on="#", how="left")
    m2 = m1.merge(pokemon, left_on="Second_pokemon", right_on="#", how="left", suffixes=("_f", "_s"))
    m2["Speed_diff"] = m2["Speed_f"] - m2["Speed_s"]

    y = m2["Winner"]
    m2.drop(columns=["Winner","#_f", "#_s"], inplace=True, axis=1)

    run_cv_lr(m2, y)
    run_cv_dtc(m2, y)
    run_cv_lgb(m2, y)

main()
