################################################################################################################################
# This function implements the image search/retrieval .
# inputs: Input location of uploaded image, extracted vectors
# 
################################################################################################################################
import random
# import tensorflow.compat.v1 as tf
import tensorflow._api.v2.compat.v1 as tf
import numpy as np
import imageio
import os
import scipy.io
import time
from datetime import datetime
from scipy import ndimage
#from scipy.misc import imsave
imsave = imageio.imsave
imread = imageio.imread
from scipy.spatial.distance import cosine
#import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
import pickle 
from PIL import Image
import gc
import os
from tempfile import TemporaryFile
import json
from tensorflow.python.platform import gfile
BOTTLENECK_TENSOR_NAME = 'pool_3/_reshape:0'
BOTTLENECK_TENSOR_SIZE = 2048
MODEL_INPUT_WIDTH = 299
MODEL_INPUT_HEIGHT = 299
MODEL_INPUT_DEPTH = 3
JPEG_DATA_TENSOR_NAME = 'DecodeJpeg/contents:0'
RESIZED_INPUT_TENSOR_NAME = 'ResizeBilinear:0'
MAX_NUM_IMAGES_PER_CLASS = 2 ** 27 - 1  # ~134M

#show_neighbors(random.randint(0, len(extracted_features)), indices, neighbor_list)

def get_top_k_similar(image_data, pred, pred_final, tags, k):
      sim = []
      print("total data",len(pred))
      print(image_data.shape)
      #for i in pred:
      #print(i.shape)
              #break
      os.mkdir('static/result')
      
  # cosine calculates the cosine distance, not similiarity. Hence no need to reverse list
      top_k_ind = np.argsort([cosine(image_data, pred_row) \
                          for ith_row, pred_row in enumerate(pred)])[:]
      
      
      # 遍历top_k_ind，如果匹配到的图片在dislike.txt中，就跳过，如果不在，就存入top_k_ind，直到找到k个为止
      # print(top_k_ind)
      
      for i, neighbor in enumerate(top_k_ind):
          if neighbor >= len(pred_final) or len(sim) >= k:
              continue
          
          # print("neighbor in range")
          image = imread(pred_final[neighbor])
          #timestr = datetime.now().strftime("%Y%m%d%H%M%S")
          #name= timestr+"."+str(i)
          name = pred_final[neighbor]
          tokens = name.split("\\")
          img_name = tokens[-1]
          # 如果img_name在dislike.txt中，就跳过
          if img_name in open('./dislike.txt').read():
              print(img_name+"in dislike.txt")
              continue
          # print(img_name)

          # 去掉img_name前面的im和后面的.jpg
          img_index = img_name[2:-4]

          # 读取pic_tags.json,并转成字典
          with open('./pic_tags.json', 'r') as f:
              pic_tags = json.load(f)

          ok = False
          # 遍历tags
          for tag in tags:
              # 如果tag在pic_tags中，就检查img_index是否在pic_tags[tag]中，如果在，就结束循环
              if tag in pic_tags:
                  if img_index in pic_tags[tag]:
                      ok = True
                      break
                  
          if ok==False:
              continue

          # 计算原图和推荐图的cosine距离，并输出
          similarity_percentage = (1 - cosine(image_data, pred[neighbor])) * 100
          # 取三位小数
          similarity_percentage = round(similarity_percentage, 3)
          sim.append(similarity_percentage)

          name = 'static/result/'+img_name
          imsave(name, image) 
      
      
      return sim

                
def create_inception_graph():
  """"Creates a graph from saved GraphDef file and returns a Graph object.

  Returns:
    Graph holding the trained Inception network, and various tensors we'll be
    manipulating.
  """
  with tf.Session() as sess:
    model_filename = os.path.join(
        'imagenet', 'classify_image_graph_def.pb')
    with gfile.FastGFile(model_filename, 'rb') as f:
      graph_def = tf.GraphDef()
      graph_def.ParseFromString(f.read())
      bottleneck_tensor, jpeg_data_tensor, resized_input_tensor = (
          tf.import_graph_def(graph_def, name='', return_elements=[
              BOTTLENECK_TENSOR_NAME, JPEG_DATA_TENSOR_NAME,
              RESIZED_INPUT_TENSOR_NAME]))
  return sess.graph, bottleneck_tensor, jpeg_data_tensor, resized_input_tensor

def run_bottleneck_on_image(sess, image_data, image_data_tensor,
                            bottleneck_tensor):
 
    bottleneck_values = sess.run(
            bottleneck_tensor,
            {image_data_tensor: image_data})
    bottleneck_values = np.squeeze(bottleneck_values)
    return bottleneck_values

def recommend(imagePath, extracted_features, tags):
    
    tf.reset_default_graph()

    config = tf.ConfigProto(
        device_count = {'GPU': 0}
    )

    sess = tf.Session(config=config)
    graph, bottleneck_tensor, jpeg_data_tensor, resized_image_tensor = (create_inception_graph())
    image_data = gfile.FastGFile(imagePath, 'rb').read()
    features = run_bottleneck_on_image(sess, image_data, jpeg_data_tensor, bottleneck_tensor)	

    with open('neighbor_list_recom.pickle','rb') as f:
                neighbor_list = pickle.load(f)
    print("loaded images")
    sim = get_top_k_similar(features, extracted_features, neighbor_list, tags, k=12)
    print("sim",sim)
    return sim

