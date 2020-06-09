import cv2
import dlib
import os, sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

def test_left_face(file_name, lines):
    nose = int(float(lines[2].split(',')[0]))
    ear = int(float(lines[18].split(',')[0]))

    if nose > ear: # right_face
        return file_name
    else:
        print("Flipped")
        img = cv2.imread(file_name)
        file_name = file_name.replace(".jpg", "_flip.jpg")
        img = cv2.flip(img, 1)
        cv2.imwrite(file_name, img)

        return file_name

############################################################
# Main
############################################################
output_name = "side_face.xml"
if len(sys.argv) > 1 and sys.argv[1] == "flip":
    output_name = "side_face_flip.xml"
output_f = open(output_name, "w")
cnn_face_detector = dlib.cnn_face_detection_model_v1("cnn.dat")
files = []
for file_name in os.listdir('./side_face'):
    if file_name.endswith('.jpg') and (file_name.find("_flip") == -1):
        files.append(file_name)

dataset = ET.Element("dataset")
images = ET.Element("images")
for i, file_name in enumerate(files):
    file_name = os.path.join('C:\\Users\\woong\\Desktop\\Side_view_detector\\side_face', file_name)
    txt_name = file_name.replace("jpg", "txt")


    # face box
    print(file_name)
    face = cv2.imread(file_name)
    w, h, _ = face.shape
    rects = cnn_face_detector(face, 1)
    if len(rects) > 0:
        right = int(rects[0].rect.right()) if int(rects[0].rect.right()) < w else w-1
        left = int(rects[0].rect.left()) if int(rects[0].rect.left()) > 0 else 0
        bottom = int(rects[0].rect.bottom()) if int(rects[0].rect.bottom()) < h else h-1
        top = int(rects[0].rect.top()) if int(rects[0].rect.top()) > 0 else 0
    else:
        continue
    box = ET.Element("box", top=str(top), left=str(left), width=str(right-left), height=str(bottom-top))

    # part
    f = open(txt_name, 'r')
    if f == None:
        continue
    lines = f.readlines()
    if len(sys.argv) > 1 and sys.argv[1] == "flip":
        file_name = test_left_face(file_name, lines)
    for i, line in enumerate(lines):
        name = "%02d" % (i)
        x = int(float(line.split(',')[0]))
        y = int(float(line.split(',')[1]))
        if file_name.find("_flip") != -1:
            x = w-x
        part = ET.Element("part", name=name, x=str(x), y=str(y))
        box.append(part)

    # Image
    image = ET.Element("image", file=file_name)
           
    image.append(box)
    images.append(image)
    f.close()

dataset.append(images)
xlmstr = minidom.parseString(ET.tostring(dataset)).toprettyxml(indent="   ")
output_f.write(xlmstr)
output_f.close()
