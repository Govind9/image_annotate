import os
import cv2
import shutil
import json
import random
from tqdm import tqdm
from pathlib import Path

with open('template.xml') as file:
    xml = file.read()

src, dest = Path(''), Path('')
all_files = os.listdir(src)
files = random.sample(all_files, 10000)

for iter, file in enumerate(tqdm(files)):
    try:
        ext = file.split('.')[1]
        if ext.lower() not in ['jpg', 'jpeg', 'png']:
            continue
        
        old_name = src / file
        new_name = dest / f'{iter+1}.{ext}'
        xml_name = dest / f'{iter+1}.xml'

        img = cv2.imread(old_name)
        height, width, channels = img.shape
        #"025-95_113-154&383_386&473-386&473_177&454_154&383_363&402-0_0_22_27_27_33_16-37-15.jpg"
        coords = file.split('-')[3].split('_')
        xmin, ymin, xmax, ymax = float('inf'), float('inf'), float('-inf'), float('-inf') 
        for coord in coords:
            x = int(coord.split('&')[0])
            y = int(coord.split('&')[1])
            if x < xmin:
                xmin = x
            if y < ymin:
                ymin = y
            if x > xmax:
                xmax = x
            if y > ymax:
                ymax = y
        with open(xml_name, 'w') as f:
            f.write(xml.format(
                width = width,
                height = height,
                channels = channels,
                xmin = xmin,
                ymin = ymin,
                xmax = xmax,
                ymax = ymax
            ))
        shutil.copy(old_name, new_name)
    except Exception as e:
        print (str(e))