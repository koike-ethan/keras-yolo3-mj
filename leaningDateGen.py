import sys
import os
import os.path
import random
import datetime
import cv2
import numpy as np
from IPython.display import Image,display_png
import matplotlib.pyplot as plt

#######################################################

# 画像出力用関数
def display_cv_image(image, format='.png'):
    decoded_bytes = cv2.imencode(format, image)[1].tobytes()
    display(Image(data=decoded_bytes))
    
#######################################################

# 背景作成

BOARD_W = 359
BOARD_H = 223
NUM_COLOR = 3

boardimage = np.ones((BOARD_H, BOARD_W , NUM_COLOR), np.uint8)*100
#display_cv_image(boardimage)

#######################################################

# 牌画取得

TEMPLATE_DIR_PATH = './paiga'
PAIGA_W = 31
PAIGA_H = 47

paiga_listdir = os.listdir(TEMPLATE_DIR_PATH)
paigas = []

for filename in paiga_listdir:
    paiga = cv2.imread(TEMPLATE_DIR_PATH + '/' + filename)
    paigas.append([filename,paiga])
    '''
                ### paiga[n][0] -> filename
                ### paiga[n][1] -> image
                n = 30
                print(paigas[n][0])
                display_cv_image(paigas[n][1])
    '''
    
#######################################################

# 牌座標取得関数
def paipos(w,h):
    xmin_ = w
    ymin_ = h
    xmax_ = w + PAIGA_W
    ymax_ = h + PAIGA_H
    return xmin_, ymin_, xmax_, ymax_

# アノテーション作成関数
def annotation1(now):
    annotation1_ = ""
    annotation1_ = annotation1_ + "<annotation>\n"
    annotation1_ = annotation1_ + "  <folder>XXX</folder>\n"
    annotation1_ = annotation1_ + "  <filename>" + now + ".png</filename>\n"
    annotation1_ = annotation1_ + "  <source>\n"
    annotation1_ = annotation1_ + "    <database>XXX</database>\n"
    annotation1_ = annotation1_ + "    <annotation>XXX</annotation>\n"
    annotation1_ = annotation1_ + "    <image>XXX</image>\n"
    annotation1_ = annotation1_ + "    <flickrid>XXX</flickrid>\n"
    annotation1_ = annotation1_ + "  </source>\n"
    annotation1_ = annotation1_ + "  <owner>\n"
    annotation1_ = annotation1_ + "    <flickrid>XXX</flickrid>\n"
    annotation1_ = annotation1_ + "    <name>?</name>\n"
    annotation1_ = annotation1_ + "  </owner>\n"
    annotation1_ = annotation1_ + "  <size>\n"
    annotation1_ = annotation1_ + "    <width>" + str(BOARD_W) + "</width>\n"
    annotation1_ = annotation1_ + "    <height>" + str(BOARD_H) + "</height>\n"
    annotation1_ = annotation1_ + "    <depth>3</depth>\n"
    annotation1_ = annotation1_ + "  </size>\n"
    annotation1_ = annotation1_ + "  <segmented>0</segmented>\n"
    return annotation1_

def annotation2(painame, xmin, ymin, xmax, ymax):
    annotation2_ = ""
    annotation2_ = annotation2_ + "  <object>\n"
    annotation2_ = annotation2_ + "    <name>" +painame + "</name>\n"
    annotation2_ = annotation2_ + "    <pose>Unspecified</pose>\n"
    annotation2_ = annotation2_ + "    <truncated>0</truncated>\n"
    annotation2_ = annotation2_ + "    <difficult>0</difficult>\n"
    annotation2_ = annotation2_ + "    <bndbox>\n"
    annotation2_ = annotation2_ + "      <xmin>" + str(xmin) + "</xmin>\n"
    annotation2_ = annotation2_ + "      <ymin>" + str(ymin) + "</ymin>\n"
    annotation2_ = annotation2_ + "      <xmax>" + str(xmax) + "</xmax>\n"
    annotation2_ = annotation2_ + "      <ymax>" + str(ymax) + "</ymax>\n"
    annotation2_ = annotation2_ + "    </bndbox>\n"
    annotation2_ = annotation2_ + "  </object>\n"
    return annotation2_

def annotation3():
    annotation3_ = ""
    annotation3_ = annotation3_ + "</annotation>"
    return annotation3_


# 牌画埋め込み
YOHAKU = 20
img = boardimage.copy()
img_name = []
for num in range(0,int(sys.argv[1])):
    img_random = random.sample(paigas, len(paigas))
    i = 0
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    xml = annotation1(now)
    for h in range(YOHAKU, BOARD_H - YOHAKU + 1, PAIGA_H + 1):
        for w in range(YOHAKU, BOARD_W - YOHAKU + 1, PAIGA_W + 1):
            img[h:h+PAIGA_H, w:w+PAIGA_W] = img_random[i][1]
            xmin, ymin, xmax, ymax = paipos(w,h)
            painame = img_random[i][0].replace('.png', '')
            #print('{},{},{},{},{}'.format(painame, xmin, ymin, xmax, ymax))
            xml = xml + annotation2(painame, xmin, ymin, xmax, ymax)
            if i == 36 :
                break
            else:
                i += 1
    xml = xml + annotation3()
    #display_cv_image(img)
    #print(xml)

    folder_xml = "./VOCdevkit/VOC2007/Annotations/"
    folder_png = "./VOCdevkit/VOC2007/JPEGImages/"
    with open(folder_xml + now + ".xml", "w") as f:
        f.write(xml)
    cv2.imwrite(folder_png + now + ".png", img)