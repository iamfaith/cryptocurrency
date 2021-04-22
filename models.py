import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, BatchNormalization
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.callbacks import ModelCheckpoint, ModelCheckpoint
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier

NUM_UNITS = 128
VERBOSE = False

def _create_model(input_shape,dropout_01,dropout_02):

    model = Sequential()
    model.add(LSTM(NUM_UNITS, input_shape=input_shape, return_sequences=True))
    model.add(Dropout(dropout_01))
    model.add(BatchNormalization())

    model.add(LSTM(NUM_UNITS, return_sequences=True))
    model.add(Dropout(dropout_02))
    model.add(BatchNormalization())

    model.add(LSTM(NUM_UNITS))
    model.add(Dropout(dropout_01))
    model.add(BatchNormalization())

    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.1))

    model.add(Dense(3, activation='softmax'))

    if VERBOSE:
        model.summary()

    opt = tf.keras.optimizers.Adam(lr=0.001, decay=1e-6)  # lr=0.001, decay=1e-6

    model.compile(loss='sparse_categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

    return model


def create_model(input_shape,dropout_01,dropout_02):
    gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
    tf.config.experimental.set_visible_devices(devices=gpus[0], device_type='GPU')
    tf.config.experimental.set_memory_growth(device=gpus[0], enable=True)
    model = KerasClassifier(build_fn=_create_model, input_shape=input_shape, dropout_01=dropout_01, dropout_02=dropout_02, epochs=100, batch_size=128, verbose=1)
    return model