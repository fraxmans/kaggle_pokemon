def target_encoding(combats, col):
    replace_dict = {}

    res = combats.groupby([col])["Winner"].sum() / combats.groupby([col]).size()
    for idx, val in res.items():
        replace_dict[idx] = val

    combats[col].replace(replace_dict, inplace=True)
    return replace_dict
