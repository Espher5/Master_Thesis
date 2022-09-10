from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.callbacks import EarlyStopping
import pandas as pd
import numpy as np
from sklearn import metrics
import csv


from tabgan.sampler import GANGenerator
from sklearn.model_selection import train_test_split

with open('../tests.csv') as csv_file:
    columns = []
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        columns.append(row)
        break
    columns = columns[0]

df = pd.read_csv('../tests.csv')
print(df)
# Split into training and test sets
x = df.loc[:, 'x0': 'y49']
y = df.loc[:, 'fitness']
print(x.head())
print(y.head())

df_x_train, df_x_test, df_y_train, df_y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# Create dataframe versions for tabular GAN
df_x_test, df_y_test = df_x_test.reset_index(drop=True), df_y_test.reset_index(drop=True)
df_y_train = pd.DataFrame(df_y_train)
df_y_test = pd.DataFrame(df_y_test)

# Pandas to Numpy
x_train = df_x_train.values
x_test = df_x_test.values
y_train = df_y_train.values
y_test = df_y_test.values


# Build the neural network discriminator
model = Sequential()
# Hidden 1
model.add(Dense(50, input_dim=x_train.shape[1], activation='relu'))
model.add(Dense(25, activation='relu'))     # Hidden 2
model.add(Dense(12, activation='relu'))     # Hidden 2
model.add(Dense(1))                         # Output
model.compile(loss='mean_squared_error', optimizer='adam')

monitor = EarlyStopping(monitor='val_loss', min_delta=1e-3,
                        patience=5, verbose=1, mode='auto',
                        restore_best_weights=True)
model.fit(x_train, y_train, validation_data=(x_test, y_test), callbacks=[monitor], verbose=2, epochs=1000)

# Generator definition
gen_x, gen_y = GANGenerator(
    gen_x_times=1.1,
    cat_cols=None,
    bot_filter_quantile=0.001,
    top_filter_quantile=0.999,
    is_post_process=True,
    adversarial_model_params={
        "metrics": "rmse",
        "max_depth": 2,
        "max_bin": 100,
        "learning_rate": 0.02,
        "random_state": 42,
        "n_estimators": 500,
    },
    pregeneration_frac=2,
    only_generated_data=False,
    gan_params={
        "batch_size": 500,
        "patience": 25,
        "epochs": 500,
    }).generate_data_pipe(df_x_train, df_y_train, df_x_test,
                          deep_copy=True,
                          only_adversarial=False,
                          use_adversarial=True)


print('Generated cases', gen_x)
gen_x.to_csv('generated_cases.csv')

print('Starting prediction...')
pred = model.predict(gen_x.values)
score = np.sqrt(metrics.mean_squared_error(pred,gen_y.values))
print("Final score (RMSE): {}".format(score))