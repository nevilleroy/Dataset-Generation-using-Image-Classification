import tensorflow as tf
import tensorflow_hub as hub
# For saving 'feature vectors' into a txt file
import numpy as np
# Glob for reading file names in a folder
import glob
import os.path
import time
from annoy import AnnoyIndex
from scipy import spatial


def load_img(path):
# Reads the image file and returns data type of string
    img = tf.io.read_file(path)
    img = tf.io.decode_jpeg(img, channels=3)
    img = tf.image.resize_with_pad(img, 224, 224)
    img = tf.image.convert_image_dtype(img,tf.float32)[tf.newaxis, ...]

    return img
    

def get_image_feature_vectors(path):
    module_handle = "https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/feature_vector/4"
    module = hub.load(module_handle)
    img = load_img(path)
    features = module(img)
    feature_set = np.squeeze(features)
    outfile_name = os.path.basename(path) + ".npz"
    out_path = os.path.join('/Users/nevilleroy/Desktop/MainProject/Web-Scraping/feature-vectors/',
            outfile_name)
    np.savetxt(out_path, feature_set, delimiter=',')
    return out_path


def get_similarity_score(sample_img, image, sample_path):
    img_path = "/temp.jpg"
    sample_vec_path = get_image_feature_vectors(sample_path)
    img_vec_path = get_image_feature_vectors(img_path)
    sample_file_vector = np.loadtxt(sample_vec_path)
    image_file_vector = np.loadtxt(img_vec_path)
    similarity = 1 - spatial.distance.cosine(sample_file_vector, image_file_vector)
    rounded_similarity = int((similarity * 10000)) / 10000.0
    return rounded_similarity * 100

