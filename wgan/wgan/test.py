from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
import pandas as pd
import io
import os
import requests
import numpy as np
from sklearn import metrics


from tabgan.sampler import GANGenerator
from sklearn.model_selection import train_test_split

#df = pd.read_csv('https://data.heatonresearch.com/data/t81-558/auto-mpg.csv', na_values=['NA', '?'])
#COLS_USED = ['cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'year', 'origin', 'mpg']
#COLS_TRAIN = ['cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'year', 'origin']

df = pd.read_csv('', na_values=['NA', '?'])
COLS_USED = ['cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'year', 'origin', 'mpg']
COLS_TRAIN = ['cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'year', 'origin']

df = df[COLS_USED]

# Handle missing value
df['horsepower'] = df['horsepower'].fillna(df['horsepower'].median())

# Split into training and test sets
df_x_train, df_x_test, df_y_train, df_y_test = train_test_split(
    df.drop("mpg", axis=1),
    df["mpg"],
    test_size=0.20,
    #shuffle=False,
    random_state=42,
)

# Create dataframe versions for tabular GAN
df_x_test, df_y_test = df_x_test.reset_index(drop=True), \
  df_y_test.reset_index(drop=True)
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
model.add(Dense(25, activation='relu')) # Hidden 2
model.add(Dense(12, activation='relu')) # Hidden 2
model.add(Dense(1)) # Output
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
    gan_params = {
        "batch_size": 500,
        "patience": 25,
        "epochs" : 500,
    }).generate_data_pipe(df_x_train, df_y_train, df_x_test,
                          deep_copy=True,
                          only_adversarial=False,
                          use_adversarial=True)
print(gen_x)

print('Starting prediction...')
pred = model.predict(gen_x.values)
score = np.sqrt(metrics.mean_squared_error(pred,gen_y.values))
print("Final score (RMSE): {}".format(score))