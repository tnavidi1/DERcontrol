from keras.models import Sequential
from keras.layers import Dense
import numpy
# fix random seed for reproducibility
numpy.random.seed(7)


def nn_train(X, Y, loss, activation_1, activation_2, activation_3, epochs, batch_size):
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.20)
    # create model
    model = Sequential()
    model.add(Dense(200, input_dim=246, activation=activation_1))
    model.add(Dense(50, activation=activation_2))
    model.add(Dense(123, activation=activation_3))

    # Compile model
    model.compile(loss=loss, optimizer='adam', metrics=['accuracy'])

    # Fit the model
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)

    # evaluate the model
    scores = model.evaluate(X_test, y_test)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))