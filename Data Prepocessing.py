import json
from PIL import Image 
from itertools import chain
from sklearn.model_selection import train_test_split


f = open("output.manifest", "r")
file=f.read()
lis=file.split('\n')

image_name=[]
properties=[]

for i in lis[:-1]:
    js = json.loads(i)
    image_name.append(js['source-ref'].split('/')[-1])
    annot=[]
    for j in js['zegar-labeling-test']['annotations']:
        label_index = [*j.values()][0]

        '''xmin = [*j.values()][1] #Top 
        ymin = [*j.values()][2] #left
        h = [*j.values()][3] #height Right
        w = [*j.values()][4] #width Bottom 

        w_img = [*js['zegar-labeling-test']['image_size'][0].values()][0] # image width
        h_img = [*js['zegar-labeling-test']['image_size'][0].values()][1]  #image height
 
        xcenter = (xmin + w/2) / w_img
        ycenter = (ymin + h/2) / h_img
        w = w / w_img
        h = h / h_img
        annot.append([label_index, xcenter, ycenter, w, h])'''
        
        
        t = [*j.values()][1] # top
        l = [*j.values()][2] # left
        h = [*j.values()][3] #height
        w = [*j.values()][4]  #width
        
        #image height and image width
        img_w, img_h = [*js['zegar-labeling-test']['image_size'][0].values()][0], [*js['zegar-labeling-test']['image_size'][0].values()][1]
        
        
        x1 = l
        y1 = t
        x2 = (l+w)
        y2 = (t+h)

        b_center_x = (x1 + x2) / 2 
        b_center_y = (y1 + y2) / 2
        b_width    = (x2 - x1)
        b_height   = (y2 - y1)
        
        # Normalise the co-ordinates by the dimensions of the image
        b_center_x /= img_w 
        b_center_y /= img_h 
        b_width    /= img_w 
        b_height   /= img_h 

        #annot.append([label_index,x1, y1, x2, y2])
        annot.append([label_index,b_center_x, b_center_y, b_width, b_height])

    properties.append(annot)
    

images_train, images_test, labels_train, labels_test = train_test_split(image_name, properties, test_size=0.2, random_state=42)


for i , j in zip(images_train, labels_train):
    if(len(j)>0):
        im1 = Image.open(i) 

        im1.save('train_data/train/images/'+i)
        with open('train_data/train/labels/'+i.split('.')[0]+".txt", "w") as outfile:
            
            for line in j:
                for inline in line:
                    outfile.write(f" {inline}")
                outfile.write(f"\n")
    else:
        print(f"{i} has no annotation")

        
        
        
        
        
for i , j in zip(images_test, labels_test):
    if(len(j)>0): # if annotation list of an image is not empty it mean it has annotations
        im1 = Image.open(i) 

        im1.save('train_data/val/images/'+i)
        with open('train_data/val/labels/'+i.split('.')[0]+".txt", "w") as outfile:
            for line in j:
                for inline in line:
                    outfile.write(f" {inline}")
                outfile.write(f"\n")
    else:
        print(f"{i} has no annotation")
                              
                              