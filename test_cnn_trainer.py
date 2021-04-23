# Ressource : https://arnavparuthi.medium.com/playing-ultimate-tic-tac-toe-using-reinforcement-learning-892f084f7def

from keras import layers
from keras.models import Model
from keras.optimizers import Adam


def neural_network():
    # Couche d'entrée : la shape est 3,3 (board 3x3)
    input_layer = layers.Input(shape=(3, 3), name="BoardInput")
    reshape = layers.core.Reshape((3, 3, 1))(input_layer)

    # 1 couche convolutionnelle
    conv_1 = layers.Conv2D(128, (3, 3), padding='valid', activation='relu', name='conv1')(reshape)
    conv_1_flat = layers.Flatten()(conv_1)

    # 2 couches Dense
    dense_1 = layers.Dense(512, activation='relu', name='dense1')(conv_1_flat)
    dense_2 = layers.Dense(256, activation='relu', name='dense2')(dense_1)

    # Value & policy
    # La policy fournit un vecteur de probabilités pour effectuer une certaine action
    # La value fournit une valeur entre 1 et -1, indiquant l'estimation de savoir si le joueur actuel gagnera ou non à partir de l'état actuel
    pi = layers.Dense(9, activation="softmax", name='pi')(dense_2)
    v = layers.Dense(1, activation="tanh", name='value')(dense_2)

    model = Model(inputs=input_layer, outputs=[pi, v])
    model.compile(loss=['categorical_crossentropy'], optimizer=Adam())

    model.summary()
    return model


def train():
    cnn = neural_network()

    # Lancer n simulations de parties
    # Puis transmetter au cnn les boards ?

    # board_state?
    # [policy, value]?
    history = nn.fit(
        board_state,
        [policy, value],
        batch_size=32,
        verbose=1
    )