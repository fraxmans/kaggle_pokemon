import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from common import target_encoding

def attribute_winner_scatterplot(combats):
    attribute = ["HP", "Attack", "Defense", "Sp_Atk", "Sp_Def", "Speed"]

    for col in attribute:
        x = col + "_f"
        y = col + "_s"

        ax = sns.scatterplot(x=x, y=y, hue="Winner", data=combats)
        ax.set_title("%s - Winner scatterplot" % col)
        plt.show()

def generation_winrate_distribution(pokemon, combats):
    index = pokemon["Generation"].unique()
    df = pd.DataFrame(0, index=index, columns=["win_count", "fight_count", "win_rate"])

    for idx, row in combats.iterrows():
        generation_f = row["Generation_f"]
        generation_s = row["Generation_s"]

        if(row["Winner"]):
            df.loc[generation_f, "win_count"] += 1
            df.loc[generation_f, "fight_count"] += 1
            df.loc[generation_s, "fight_count"] += 1
        else:
            df.loc[generation_s, "win_count"] += 1
            df.loc[generation_s, "fight_count"] += 1
            df.loc[generation_f, "fight_count"] += 1
    df["win_rate"] = 100.0 * df["win_count"] / df["fight_count"]
 
    ax = sns.barplot(x=df.index, y=df.win_rate)
    ax.set_title("Winrate of each category in Generation")
    plt.show()

def mix_type_winrate_distribution(pokemon, combats):
    index = pokemon["mix_type"].unique()
    df = pd.DataFrame(0, index=index, columns=["win_count", "fight_count", "win_rate"])

    for idx, row in combats.iterrows():
        mix_type_f = row["mix_type_f"]
        mix_type_s = row["mix_type_s"]

        if(row["Winner"]):
            df.loc[mix_type_f, "win_count"] += 1
            df.loc[mix_type_f, "fight_count"] += 1
            df.loc[mix_type_s, "fight_count"] += 1
        else:
            df.loc[mix_type_s, "win_count"] += 1
            df.loc[mix_type_s, "fight_count"] += 1
            df.loc[mix_type_f, "fight_count"] += 1
    df["win_rate"] = 100.0 * df["win_count"] / df["fight_count"]
 
    ax = sns.barplot(x=df.index, y=df.win_rate)
    ax.set_title("Winrate of each category in mix_type")
    plt.show()

def type2_winrate_distribution(pokemon, combats):
    index = pokemon["Type_2"].unique()
    df = pd.DataFrame(0, index=index, columns=["win_count", "fight_count", "win_rate"])

    for idx, row in combats.iterrows():
        type2_f = row["Type_2_f"]
        type2_s = row["Type_2_s"]

        if(row["Winner"]):
            df.loc[type2_f, "win_count"] += 1
            df.loc[type2_f, "fight_count"] += 1
            df.loc[type2_s, "fight_count"] += 1
        else:
            df.loc[type2_s, "win_count"] += 1
            df.loc[type2_s, "fight_count"] += 1
            df.loc[type2_f, "fight_count"] += 1
    df["win_rate"] = 100.0 * df["win_count"] / df["fight_count"]
 
    ax = sns.barplot(x=df.index, y=df.win_rate)
    ax.set_title("Winrate of each category in Type_2")
    plt.show()

def type1_winrate_distribution(pokemon, combats):
    index = pokemon["Type_1"].unique()
    df = pd.DataFrame(0, index=index, columns=["win_count", "fight_count", "win_rate"])

    for idx, row in combats.iterrows():
        type1_f = row["Type_1_f"]
        type1_s = row["Type_1_s"]

        if(row["Winner"]):
            df.loc[type1_f, "win_count"] += 1
            df.loc[type1_f, "fight_count"] += 1
            df.loc[type1_s, "fight_count"] += 1
        else:
            df.loc[type1_s, "win_count"] += 1
            df.loc[type1_s, "fight_count"] += 1
            df.loc[type1_f, "fight_count"] += 1
    df["win_rate"] = 100.0 * df["win_count"] / df["fight_count"]
 
    ax = sns.barplot(x=df.index, y=df.win_rate)
    ax.set_title("Winrate of each category in Type_1")
    plt.show()

def legendary_to_generation_distribution(data):

    sns.countplot(x="Generation", hue="Legendary", data=data)
    plt.show()

def attribute_to_generation_boxplot(data):
    attribute = ["HP", "Attack", "Defense", "Sp_Atk", "Sp_Def", "Speed"]

    for col in attribute:
        ax = sns.boxplot(x="Generation", y=col, data=data)
        ax.set_title("Boxplot for %s - Generation" % (col))
        plt.show()

def attribute_to_legendary_boxplot(data):
    attribute = ["HP", "Attack", "Defense", "Sp_Atk", "Sp_Def", "Speed"]

    for col in attribute:
        ax = sns.boxplot(x="Legendary", y=col, data=data)
        ax.set_title("Boxplot for %s - Legendary" % (col))
        plt.show()

def attribute_to_mix_type_boxplot(data):
    attribute = ["HP", "Attack", "Defense", "Sp_Atk", "Sp_Def", "Speed"]

    for col in attribute:
        ax = sns.boxplot(x="mix_type", y=col, data=data)
        ax.set_title("Boxplot for %s - (Type_1-Type_2)" %col)
        plt.setp(ax.get_xticklabels(), rotation=60, horizontalalignment="left")
        plt.show()

def attribute_to_type_boxplot(data):
    attribute = ["HP", "Attack", "Defense", "Sp_Atk", "Sp_Def", "Speed"]

    for i in [1, 2]:
        tp = "Type_" + str(i)
        for col in attribute:
            ax = sns.boxplot(x=tp, y=col, data=data)
            ax.set_title("Boxplot for %s - %s" % (col, tp))
            plt.show()

def check_null_value(data):
    length = data.shape[0] * 1.0

    print("Column\t null(%)")
    for col in data.columns:
        print("%s\t%6.3f" % (col, data[col].isnull().sum() / length))

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
    pokemon["mix_type"] = pokemon["Type_1"] + "-" + pokemon["Type_2"]

    combats = load_data("data/combats.csv")
    combats["Winner"] = (combats["Winner"] == combats["First_pokemon"])

    m1 = combats.merge(pokemon, left_on="First_pokemon", right_on="#", how="left")
    m2 = m1.merge(pokemon, left_on="Second_pokemon", right_on="#", how="left", suffixes=("_f", "_s"))

main()
