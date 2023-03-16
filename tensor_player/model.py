import json
import random
from typing import List

import numpy
import tensorflow

from game.enums import Directions


class Model:
    def __init__(self, filepath: str | None = None) -> None:
        inputs = tensorflow.keras.Input(shape=(900,), name="digits")
        x = tensorflow.keras.layers.Dense(100, name="dense_1")(inputs)
        x = tensorflow.keras.layers.Dense(100, name="dense_2")(x)
        outputs = tensorflow.keras.layers.Dense(1, name="predictions")(x)

        self._model = tensorflow.keras.Model(inputs=inputs, outputs=outputs)
        if filepath is not None:
            with open(filepath, 'r') as fd:
                weights = json.load(fd)
            self.set_weights(weights)
        else:
            # self.set_random_weights()
            self.set_random_weights

    def get_weights(self) -> List[float]:
        weights = []
        for weight in self._model.weights:
            if len(weight.shape) == 1:
                weights += numpy.array(weight).tolist()
            elif len(weight.shape) == 2:
                weights += numpy.array(weight).reshape((weight.shape[0]*weight.shape[1],)).tolist()
            else:
                raise Exception('Invalid shape')

        return weights

    def set_weights(self, weights: List[float]):
        final_weights = []
        for weight in self._model.weights:
            if len(weight.shape) == 1:
                final_weights.append(numpy.array(weights[:weight.shape[0]]))
                weights = weights[weight.shape[0]:]
            elif len(weight.shape) == 2:
                ws = numpy.array(weights[:weight.shape[0]*weight.shape[1]])
                final_weights.append(ws.reshape(weight.shape))
                weights = weights[weight.shape[0]*weight.shape[1]:]
            else:
                raise Exception('Invalid shape')

        self._model.set_weights(final_weights)

    def set_random_weights(self) -> None:
        self._model.compile(tensorflow.keras.optimizers.Adam(0.1), loss='mean_squared_error')
        x_train = []
        y_train = []
        for _ in range(1000):
            a = numpy.zeros((30, 30))
            a[random.randint(0, 29)][random.randint(0, 29)] = 1
            a[random.randint(0, 29)][random.randint(0, 29)] = 3
            x_train.append(a.reshape((900,)))
            y_train.append(random.randint(0, 359))

        self._model.fit(numpy.array(x_train), numpy.array(y_train), epochs=100, verbose=False)

    def predict(self, data: numpy.ndarray) -> Directions:
        result = self._model.predict(data.reshape((1, 900)), verbose=False)[0]

        if result < 0 or result > 360:
            return None

        if result >= 315 or result <= 45:
            return Directions.East
        elif abs(result-90) <= 45:
            return Directions.North
        elif abs(result-180) <= 45:
            return Directions.West
        elif abs(result-270) <= 45:
            return Directions.South

    def save(self, filename) -> None:
        with open(filename, 'w') as fd:
            json.dump(self.get_weights(), fd)

    def __del__(self):
        del self._model
