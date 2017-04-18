#!/usr/bin/env python
# -*- coding: utf-8 -*-

from keras.applications import ResNet50, VGG16, InceptionV3, Xception
from keras.layers import Flatten, Dense, Dropout, Input
from keras.models import Sequential, Model

# map model names to classes
MODELS = {
    "vgg16": VGG16,
    "inception": InceptionV3,
    "xception": Xception,
    "resnet": ResNet50
}


def create_model(model, model_weights_path=None, top_model=True):
    """Create custom model for transfer learning

    Steps:
    (i) load pre-trained NN architecture
    (ii) (optional) add custom classification block of two fully connected layers
    (iii) load pre-trained model weights, if available

    Parameters
    ----------
    model: str
        choose which pre-trained Keras deep learning model to use for the 'bottom' layers of the custom model
    model_weights_path: str
        path to pre-trained weights, if available
    top_model: bool
        whether to include custom classification block, or to load model 'without top' to extract features

    Returns
    -------
    my_model: keras.model
        Model utilised for prediction or training
    """

    # ensure a valid model name was supplied
    if model not in MODELS.keys():
        raise AssertionError("The model parameter must be a key in the `MODELS` dictionary")

    # Create pre-trained model without classification block
    print("[INFO] loading %s..." % (model,))
    model = MODELS[model](include_top=False,
                          input_tensor=Input(shape=(224, 224, 3)))
    if top_model:
        # Create classification block
        top_model = Sequential()
        top_model.add(Flatten(input_shape=model.output_shape[1:]))
        top_model.add(Dense(256, activation='relu'))
        top_model.add(Dropout(0.5))
        top_model.add(Dense(26, activation='softmax'))

        # Join model + classification block
        print("[INFO] creating model.")
        my_model = Model(inputs=model.input,
                         outputs=top_model(model.output))

    if model_weights_path is not None:
        # Load pre-trained model weights
        print("[INFO] loading model weights.")
        my_model.load_weights(model_weights_path)

    return my_model
