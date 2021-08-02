
import csv
import tensorflow as tf
import numpy as np
import urllib
]
def windowed_dataset(series, window_size, batch_size, shuffle_buffer):
    series = tf.expand_dims(series, axis=-1)
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size + 1, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size + 1))
    ds = ds.shuffle(shuffle_buffer)
    ds = ds.map(lambda w: (w[:-1], w[1:]))
    return ds.batch(batch_size).prefetch(1)


def solution_model():

    time_step = []
    stocks = []

    with open('stocks.csv') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      next(reader)
      for row in reader:
        stocks.append(float(row[2])) 
        time_step.append(float(row[0]))

    series = np.array(stocks) 
    
    min = np.min(series)
    max = np.max(series)
    series -= min
    series /= max
    time = np.array(time_step)


    split_time = 3000


    time_train = time[:split_time] 
    x_train = series[:split_time] 
    time_valid = time[split_time:] 
    x_valid = series[split_time:]

    # DO NOT CHANGE THIS CODE
    window_size = 30
    batch_size = 32
    shuffle_buffer_size = 1000


    train_set = windowed_dataset(x_train, window_size=window_size, batch_size=batch_size,
                                 shuffle_buffer=shuffle_buffer_size)
    validation_set = windowed_dataset(x_valid, window_size=window_size, batch_size=batch_size,
                                 shuffle_buffer=shuffle_buffer_size)

    model = tf.keras.models.Sequential([
        # YOUR CODE HERE. Whatever your first layer is, the input shape will be [None,1] when using the Windowed_dataset above, depending on the layer type chosen
        tf.keras.layers.Conv1D(64, kernel_size=5, padding='same', activation='relu',
                               input_shape=[None, 1]),
        tf.keras.layers.LSTM(64, return_sequences=True),
        tf.keras.layers.LSTM(64, return_sequences=True), #아니면 return_sequences 를 지우던가.
        # Flatten 안해줘?
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    # PLEASE NOTE IF YOU SEE THIS TEXT WHILE TRAINING -- IT IS SAFE TO IGNORE
    # BaseCollectiveExecutor::StartAbort Out of range: End of sequence
    # 	 [[{{node IteratorGetNext}}]]
    #

    # YOUR CODE HERE TO COMPILE AND TRAIN THE MODEL

    model.compile(loss='mae', optimizer='adam', metrics=['mae'])

    model.fit(train_set, validation_data=validation_set, epochs=200)

    return model


# Note that you'll need to save your model as a .h5 like this.
# When you press the Submit and Test button, your saved .h5 model will
# be sent to the testing infrastructure for scoring
# and the score will be returned to you.
if __name__ == '__main__':
    model = solution_model()
    # model.save("mymodel.h5")



# THIS CODE IS USED IN THE TESTER FOR FORECASTING. IF YOU WANT TO TEST YOUR MODEL
# BEFORE UPLOADING YOU CAN DO IT WITH THIS
#def model_forecast(model, series, window_size):
#    ds = tf.data.Dataset.from_tensor_slices(series)
#    ds = ds.window(window_size, shift=1, drop_remainder=True)
#    ds = ds.flat_map(lambda w: w.batch(window_size))
#    ds = ds.batch(32).prefetch(1)
#    forecast = model.predict(ds)
#    return forecast


#window_size = # YOUR CODE HERE
#rnn_forecast = model_forecast(model, series[..., np.newaxis], window_size)
#rnn_forecast = rnn_forecast[split_time - window_size:-1, -1, 0]

#result = tf.keras.metrics.mean_absolute_error(x_valid, rnn_forecast).numpy()

## To get the maximum score, your model must have an MAE OF .12 or less.
## When you Submit and Test your model, the grading infrastructure
## converts the MAE of your model to a score from 0 to 5 as follows:

#test_val = 100 * result
#score = math.ceil(17 - test_val)
#if score > 5:
#    score = 5

#print(score)