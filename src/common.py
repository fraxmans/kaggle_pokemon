from sklearn.preprocessing import LabelEncoder

def target_encoding(combats, col):
    replace_dict = {}

    res = combats.groupby([col])["Winner"].sum() / combats.groupby([col]).size()
    for idx, val in res.items():
        replace_dict[idx] = val

    combats[col].replace(replace_dict, inplace=True)
    return replace_dict

def label_encoding(pokemon, col):
    le = LabelEncoder()
    pokemon[col] = le.fit_transform(pokemon[col])

    return le
