import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.callbacks import EarlyStopping
import pickle
import os


def split_sequence(sequence, n_steps):
    X, y = list(), list()
    for i in range(len(sequence)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the sequence
        if end_ix > len(sequence)-1:
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)

def preprocessing(df):
    scaler = MinMaxScaler()
    train_len = int((len(df)-1)/10*9)
    val_len = len(df) - train_len -1

    X_test = scaler.transform(df[['close']][-30:].values)
    X_test, y_test = split_sequence(X_test, 12)
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], n_features))

    if os.path.exists("model.py"):
        model = pickle.load(model, open('model.py', 'rb'))
        
    else:

        X_train = scaler.fit_transform(df[['close']][0:train_len].values)
        X_val = scaler.transform(df[['close']][train_len:-1].values)
        # X_test = scaler.transform(df[['close']][-30:].values)

        X_train, y_train = split_sequence(X_train, 12)
        X_val, y_val = split_sequence(X_val, 12)
        # X_test, y_test = split_sequence(X_test, 12)

        n_features=1
        X_val = X_val.reshape((X_val.shape[0], X_val.shape[1], n_features))
        # X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], n_features))

        model = Sequential([
        LSTM(50, activation="relu", input_shape=X_train.shape[1:]), # or (X_train.shape[1], 1) or (n_steps, n_features)
        Dense(1)
    ])
        model.compile(optimizer='adam', loss='mse')

        early_stopping_cb = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True) 

        history = model.fit(X_train, y_train, epochs=100, validation_data=(X_val, y_val),batch_size = 32,callbacks=early_stopping_cb)

        mse_val = model.evaluate(X_val, y_val)
        rmse = np.sqrt(mse_val)
        print(rmse)

        pickle.dump(model, open('model.py', 'wb')) 

    predicted_close = model.predict(X_test)
    predicted_close = scaler.inverse_transform(predicted_close)

    prediction = pd.Series(predicted_close[-18:].reshape(-1), index = df4['close'].iloc[-18:].index)

    predict_stock = prediction[-1]
    last_stock = df.iloc[-2]['close']

    change_by_day = ((predict_stock) - last_stock)/last_stock

    return change_by_day

if __name__ == "__main__":

    symbol =  'GOOGL'
    get_stocks_by_mongo(symbol)