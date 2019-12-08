# mlFinalVape

Requirements

Python 3
Keras 
OpenCV
imgaug
tqdm
h5py

try installing them with PIP




You have to edit the config file to control most of the behavior

#Step1 do config.json
OPen it up and change the architecture to "Tiny Yolo", this is the backend weights for the network that 
we have trained with. 
Our parameters were the following: 2 training iterations, 10 epochs, 3 warmups

You need to unzip our raccon dataset folder. 
Inside of the folder you will see a folder named images and a folder named annotations
The annotations are POC XML format for defining the correct boundary boxes

Once you set up the folders, make sure to have the paths set in train_image_folder and train_annot_folder 

Leave the pretrained_weights section blank unless you want to add training to a set of weights

the Saved_weights string will be the name of the weights you will produce and use for perdicting

the anchors section is important for setting up the grid examination Yolo does to pass into the CNN part of the code

#Step 2 set up anchor
Anchors are initial sizes (width, height) some of which (the closest to the object size) will be resized to the object size 
using some outputs from the neural network (final feature map):
We already have anchors set up for the Raccoon image set but if you want to regenerate them you have to put in the following
: python gen_anchors.py -c config.json

#Step 3 Training 

python train.py -c config.json

#Step 4 Prediction

After you are done training it will produce a weight file that is

python predict.py -c config.json -w /path/to/best_weights.h5 -i /path/to/image/or/video

Check the folder where the image is and a square will be created (if fate allows)
with a image with the extension -Detected on the end of it

#NOTES
We trained on a data set that was a mistake. 
YOLO was created for images that are consitent in sizing for grid space learning 
It recognizes objects relative to a set size. Since we have images smaller than this 
set size, it causes distortion and errors in training. 

Keep in mind this is an Object Detection Algorithm designed for Live Video Streams 

So still images of various sizes were not the ideal situation to train in 
