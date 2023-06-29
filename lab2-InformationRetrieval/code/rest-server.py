#!flask/bin/python
################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------                                                                                                                             
# This file implements the REST layer. It uses flask micro framework for server implementation. Calls from front end reaches 
# here as json and being branched out to each projects. Basic level of validation is also being done in this file. #                                                                                                                                  	       
#-------------------------------------------------------------------------------------------------------------------------------                                                                                                                              
################################################################################################################################
from flask import Flask, jsonify, abort, request, make_response, url_for,redirect, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os
import json
import shutil 
import numpy as np
from search import recommend
import tarfile
from datetime import datetime
from scipy import ndimage
#from scipy.misc import imsave

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
from tensorflow.python.platform import gfile
app = Flask(__name__, static_url_path = "")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()

#==============================================================================================================================
#                                                                                                                              
#    Loading the extracted feature vectors for image retrieval                                                                 
#                                                                          						        
#                                                                                                                              
#==============================================================================================================================
extracted_features=np.zeros((2955,2048),dtype=np.float32)
with open('saved_features_recom.txt') as f:
    		for i,line in enumerate(f):
        		extracted_features[i,:]=line.split()
print("loaded extracted_features") 


#==============================================================================================================================
#                                                                                                                              
#  This function is used to do the image search/image retrieval
#                                                                                                                              
#==============================================================================================================================
@app.route('/dislike', methods=['GET', 'POST'])
#   //将不喜欢图片的路径传给后端
#     var xhr = new XMLHttpRequest();
#     xhr.open("POST", "/dislike", true);
#     xhr.setRequestHeader("Content-Type", "application/json");
#     xhr.send(JSON.stringify({ "dislike": image.src }));

def dislike():
    print("dislike")
    if not request.json or not 'dislike' in request.json:
        abort(400)
    dislike = request.json['dislike']
    print(dislike)
    # 将dislike的图片路径存入dislike.txt
    with open('dislike.txt', 'a') as f:
        f.write(dislike + '\n')

    return jsonify({'dislike': dislike}), 201

# @app.route('/chooseTag', methods=['GET', 'POST'])
# def chooseTag():
#     print("chooseTag")
#     if not request.json or not 'tag' in request.json:
#         abort(400)
#     tag = request.json['tag']
#     print(tag)

#     return jsonify({'tag': tag}), 201

@app.route('/imgUpload', methods=['GET', 'POST'])
#def allowed_file(filename):
#    return '.' in filename and \
#           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_img():
    print("image upload")
    result = 'static/result'
    if not gfile.Exists(result):
          os.mkdir(result)
    shutil.rmtree(result)

    # print('result',result)
 
    if request.method == 'POST' or request.method == 'GET':
        print(request.method)
        # check if the post request has the file part
        

        list_str = request.form['list']
        list_data = json.loads(list_str)
        print(list_data)

        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url) # 导致重定向过多error
        
        file = request.files['file']
        print(file.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
           
            print('No selected file')
            return redirect(request.url)
        if file:# and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            inputloc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            sim_list = recommend(inputloc, extracted_features, list_data)
            print(sim_list)
            os.remove(inputloc)
            image_path = "/result"
            
            image_list =[os.path.join(image_path, file) for file in os.listdir(result)
                              if not file.startswith('.')]
            images = {
			'image0':image_list[0],
            'image1':image_list[1],	
			'image2':image_list[2],	
			'image3':image_list[3],	
			'image4':image_list[4],	
			'image5':image_list[5],	
			'image6':image_list[6],	
			'image7':image_list[7],	
			'image8':image_list[8],
            'image9':image_list[9],
            'image10':image_list[10],
            'image11':image_list[11],
            'sim0':sim_list[0],
            'sim1':sim_list[1],
            'sim2':sim_list[2],
            'sim3':sim_list[3],
            'sim4':sim_list[4],
            'sim5':sim_list[5],
            'sim6':sim_list[6],
            'sim7':sim_list[7],
            'sim8':sim_list[8],
            'sim9':sim_list[9],
            'sim10':sim_list[10],
            'sim11':sim_list[11]

		      }				# 最多返回12张图片
            
            return jsonify(images)

#==============================================================================================================================
#                                                                                                                              
#                                           Main function                                                        	            #						     									       
#  				                                                                                                
#==============================================================================================================================
@app.route("/")
def main():
    
    return render_template("main.html")   
if __name__ == '__main__':
    app.run(debug = True, host= '0.0.0.0')
