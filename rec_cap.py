import os
import cv2
import json

with open('template.xml') as file:
    xml = file.read()

def save_xml(file, xmin, xmax, ymin, ymax, widht, height, channels):
    global xml
    fname = file.split('.')[0]
    with open(fname+'.xml', 'w') as f:
        f.write(xml.format(
            fname = file,
            width = width,
            height = height,
            channels = channels,
            xmin = xmin,
            ymin = ymin,
            xmax = xmax,
            ymax = ymax
        ))
    print (f'Saved {fname}.xml')

all_files = os.listdir()
with open('done_list.json') as file:
    done_list = json.load(file)['done_list']

for file in all_files:
    try:
        if not (file.lower().endswith('.jpg') or file.lower().endswith('.jpeg')):
            continue
        fname = int(file.split('.')[0])
        if fname in done_list:
            continue
        img = cv2.imread(file)
        height, width, channels = img.shape
        #cv2.imshow('image', img)
        r = cv2.selectROI(img, False)
        cv2.destroyAllWindows()
        if len(r) == 4:
            xmin, ymin = r[0], r[1]
            xmax, ymax = r[0] + r[2], r[1] + r[3]
            save_xml(file, xmin, xmax, ymin, ymax, width, height, channels)
            done_list.append(fname)
            done_list.sort()
            with open('done_list.json', 'w') as f:
                f.write(json.dumps({'done_list': done_list}))
    except Exception as e:
        print (str(e))