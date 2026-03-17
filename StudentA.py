# -*- coding: utf-8 -*-


from email import generator

import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import numpy as np
import time
import os
import mlflow
import mlflow.tensorflow

def load_data():
    (x_train, _), (_, _) = tf.keras.datasets.fashion_mnist.load_data()
    x_train = x_train.astype("float32")
    x_train = (x_train - 127.5) / 127.5
    x_train = x_train.reshape(x_train.shape[0], 784)
    return x_train


def build_generator():
    return tf.keras.Sequential([
        layers.Dense(256, input_shape=(100,)),
        layers.LeakyReLU(0.2),
        layers.BatchNormalization(),
        layers.Dense(512),
        layers.LeakyReLU(0.2),
        layers.BatchNormalization(),
        layers.Dense(1024),
        layers.LeakyReLU(0.2),
        layers.BatchNormalization(),
        layers.Dense(784, activation='tanh')
    ])


def build_discriminator():
    return tf.keras.Sequential([
        layers.Dense(512, input_shape=(784,)),
        layers.LeakyReLU(0.2),
        layers.Dropout(0.3),
        layers.Dense(256),
        layers.LeakyReLU(0.2),
        layers.Dropout(0.3),
        layers.Dense(1, activation='sigmoid')
    ])


def save_generated_images(model, epoch):
    noise = tf.random.normal([16, 100])
    predictions = model(noise, training=False)
    predictions = (predictions + 1.0) / 2.0

    fig = plt.figure(figsize=(4, 4))

    for i in range(predictions.shape[0]):
        plt.subplot(4, 4, i+1)
        image = tf.reshape(predictions[i], [28, 28])
        plt.imshow(image, cmap='gray')
        plt.axis('off')

    if not os.path.exists("generated"):
        os.makedirs("generated")

    plt.savefig(f"generated/epoch_{epoch}.png")
    plt.close()


def train():

    # Define hyperparameters
    batch_size = 256
    learning_rate = 0.0002
    epochs = 5

    # Set MLflow experiment
    mlflow.set_experiment("Assignment3_Abdelaziz")

    with mlflow.start_run():

        # Log parameters
        mlflow.log_param("batch_size", batch_size)
        mlflow.log_param("learning_rate", learning_rate)
        mlflow.log_param("epochs", epochs)

        # Add tag
        mlflow.set_tag("Abdelaziz", "ElHelaly")

        # Load dataset
        x_train = load_data()
        dataset = tf.data.Dataset.from_tensor_slices(x_train).shuffle(60000).batch(batch_size)

        # Build models
        generator = build_generator()
        discriminator = build_discriminator()

        # Loss and optimizers
        loss_fn = tf.keras.losses.BinaryCrossentropy(label_smoothing=0.1)
        opt_G = tf.keras.optimizers.Adam(learning_rate)
        opt_D = tf.keras.optimizers.Adam(learning_rate)

        @tf.function
        def train_step(real_images):

            batch = tf.shape(real_images)[0]
            noise = tf.random.normal([batch, 100])

            with tf.GradientTape() as tape_D, tf.GradientTape() as tape_G:

                fake_images = generator(noise, training=True)

                real_output = discriminator(real_images, training=True)
                fake_output = discriminator(fake_images, training=True)

                loss_D = loss_fn(tf.ones_like(real_output), real_output) + \
                         loss_fn(tf.zeros_like(fake_output), fake_output)

                loss_G = loss_fn(tf.ones_like(fake_output), fake_output)

                real_acc = tf.reduce_mean(tf.cast(real_output >= 0.5, tf.float32))
                fake_acc = tf.reduce_mean(tf.cast(fake_output < 0.5, tf.float32))
                acc_D = (real_acc + fake_acc) / 2

            grads_D = tape_D.gradient(loss_D, discriminator.trainable_variables)
            grads_G = tape_G.gradient(loss_G, generator.trainable_variables)

            opt_D.apply_gradients(zip(grads_D, discriminator.trainable_variables))
            opt_G.apply_gradients(zip(grads_G, generator.trainable_variables))

            return loss_D, loss_G, acc_D

        # Training loop
        for epoch in range(1, epochs + 1):

            start = time.time()
            acc_list = []

            for batch in dataset:
                _, _, acc = train_step(batch)
                acc_list.append(acc)

            epoch_acc = tf.reduce_mean(acc_list).numpy()

            # Log metric to MLflow
            mlflow.log_metric("discriminator_accuracy", epoch_acc, step=epoch)

            print(f"Epoch {epoch} | Time: {round(time.time()-start,2)}s | D_acc: {epoch_acc:.4f}")

        mlflow.tensorflow.log_model(
        model=generator,
        artifact_path="model"
        )

if __name__ == "__main__":
    train()