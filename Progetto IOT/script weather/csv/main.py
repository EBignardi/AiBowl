import os
import glob2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, Normalizer, OneHotEncoder

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def change_directory(directory):
    os.chdir(directory)
    return


def match_pattern():
    file_extension = '.csv'
    all_filenames = [i for i in glob2.glob(f"*{file_extension}")]
    # print(f"These are all of the filenames ending in .csv {all_filenames}.")
    return all_filenames


def get_col_names(files):
    transposed_csv_data = pd.read_csv(files, header=None).T
    #
    names = []
    for i in range(10):
        names.append(transposed_csv_data[i][0])
    print(names)
    return names


def merge_csv(files, cols):
    combined_csv_data = pd.concat([pd.read_csv(f, header=None) for f in files], axis=1).T
    print(combined_csv_data.shape)
    # cambiare con il nome del file
    combined_csv_data.to_csv("C:\\Users\\39342\\Desktop\\Progetto IOT\\script weather\\csv\\wow.csv")
    return


def save_final():
    df = pd.read_csv("C:\\Users\\39342\\Desktop\\Progetto IOT\\script weather\\csv\\wow.csv", header=1,
                     skiprows=lambda x: x % 2 != 0, usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    df.to_csv("C:\\Users\\39342\\Desktop\\Progetto IOT\\script weather\\csv\\wow.csv", header=col_names)
    print(df.head())
    return


def plot(dataFrame):
    # bar plot del numero di classi
    # dataFrame.value_counts().plot.bar()

    # istogramma delle features
    dataFrame.hist(figsize=(10, 12))
    plt.show()
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # directory contenente tutti i csv da unire
    # C:\\Users\\39342\\Desktop\\Progetto IOT\\script weather\\csv
    dir = "C:\\Users\\39342\\Desktop\\Progetto IOT\\script weather\\csv"
    change_directory(dir)
    files = match_pattern()
    # print(len(files))

    col_names = get_col_names(files[0])

    #change the number of file to merge
    merge_csv(files[0:-1], col_names)

    save_final()

    df = pd.read_csv("C:\\Users\\39342\\Desktop\\Progetto IOT\\script weather\\csv\\wow.csv")
    print(df.head())

    plot(df)



    print('Finish')
