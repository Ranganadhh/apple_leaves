from flask import Flask, render_template,request, redirect, url_for
import os
import cv2
from tensorflow.keras.models import load_model
import numpy as np
app = Flask(__name__,template_folder="template")

ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg' }

def allowed_file(filename):
    if (filename.split('.')[1].lower()) in { 'png', 'jpg', 'jpeg' }:
        return True
    else:
        return False
@app.route('/')
def home():
   return '''
    <html>
    <head>
    <title>MODEL</title>
    </head>
    <body>
        <h1>Apple leaf disease detection using convolutional neural networks</h1>
        <form action="http://127.0.0.1:5000/home1" method="POST"  enctype="multipart/form-data">
        <label>upload image:</label>
        <input type="file" name="file"   size="30"><br><br><br>
        <input type="submit" value="submit">
        </form>
    </body>
    </html>  '''
@app.route('/home1', methods = ['GET', 'POST'])
def about():
   if request.method == 'POST':
      x = request.files["file"]
      file = x.filename
      if file=='':
          return redirect(url_for('home'))
      if allowed_file(file)!=True:
          return '''
              <h1>Enter image only</h1>
              '''
      #redirect(url_for('home'))
      if file and allowed_file(file):
          f=''
          file=os.path.join(r'C:\Users\ADMIN\Pictures\Screenshots', file)
          model = load_model('apple_model.h5')
          model.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['accuracy'])
          img = cv2.imread(file)
          img = cv2.resize(img,(128,128))
          img = np.reshape(img,[1,128,128,3])
          img=np.float32(img)
          classes = model.predict_classes(img)
          if classes[0]==0:
              f="Type of Apple leaf Disease is : Apple_scab"
          elif classes[0]==1:
              f="Type of Apple leaf Disease is  : Black_rot"
          elif classes[0]==2:
              f="Type of Apple leaf Disease is : Cedar_apple_rust"
          else:
              f="No disease found : Leaf is Healthy"
          return render_template('home1.html',name=f)
if __name__ == '__main__':
   app.run()