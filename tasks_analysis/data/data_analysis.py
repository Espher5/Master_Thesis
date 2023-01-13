import matplotlib.pyplot as plt
import pandas as pd


def get_mean(df, column):
    return df[column].mean()


def main():
    df = pd.read_excel('Data.xlsx')
    p1_df = df.loc[df['Period'] == 'P1']
    p2_df = df.loc[df['Period'] == 'P2']
    p1_tdd_df = p1_df.loc[p1_df['Condition'] == 'TDD']
    p1_no_tdd_df = p1_df.loc[p1_df['Condition'] == 'NO-TDD']
    p2_tdd_df = p2_df.loc[p2_df['Condition'] == 'TDD']
    p2_no_tdd_df = p2_df.loc[p2_df['Condition'] == 'NO-TDD']

    p1_qlty_mean = p1_df['QLTY'].mean()
    p1_qlty_tdd_mean = p1_tdd_df['QLTY'].mean()
    p1_qlt_no_tdd_mean = p1_no_tdd_df['QLTY'].mean()
    p2_qlty_mean = 0
    p2_qlty_tdd_mean = p2_tdd_df['QLTY'].mean()
    p2_qlt_no_tdd_mean = p2_no_tdd_df['QLTY'].mean()

    p1_prod_mean = 0
    p1_prod_tdd_mean = 0
    p1_prod_no_tdd_mean = 0
    p2_prod_mean = 0
    p2_prod_tdd_mean = 0
    p2_prod_no_tdd_mean = 0

    p1_test_mean = p1_df['TEST'].mean()
    p1_test_tdd_mean = p1_tdd_df['TEST'].mean()
    p1_test_no_tdd_mean = p1_no_tdd_df['TEST'].mean()
    p2_test_mean = 0
    p2_test_tdd_mean = 0
    p2_test_no_tdd_mean = 0

    means = [p1_qlty_tdd_mean, p1_qlt_no_tdd_mean]

    qlty_boxplot = df.boxplot(by='Period', column=['TEST'], grid=False)
    qlty_boxplot.plot()
    plt.show()


if __name__ == '__main__':
    df = pd.DataFrame([
        ['Abhishek', '13/6/1995',  100, 90],
        ['Anurag',   '13/6/1995',  101, 95],
        ['Bavya',    '19/5/1995',  102, 92],
        ['Bavana',   '23/10/2003', 103, 90],
        ['Chetan',   '23/10/2003', 104, 89],
        ['Chirag',   '19/5/1995',  105, 100]],
        columns=['Name', 'DOB', 'Roll No', 'Marks'])
    print(df)
    print(df['Marks'].quantile([0.25, 0.5, 0.75]))

    boxplot = df.boxplot(column=['Marks'], by='DOB')
    boxplot.plot()
    plt.show()