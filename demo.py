import subprocess
import os
import sys

cur_path = os.getcwd()
print(cur_path)
if len(sys.argv) > 2:
    front_picture = sys.argv[1]
    side_picture =sys.argv[2]
else:
    front_picture = 'hee_f'
    side_picture  = 'hee_r'


front_detection_path = cur_path + '/Detectlandmark/Detect-Facial-Features/'
side_detection_path = cur_path + '/Detectlandmark/Side_view_detector/'
fitting_path = cur_path + '/3DMM-fitting/test/'
blender_script_path = cur_path + '/3DModelCreater'
subprocess.run('python ' + side_detection_path+ 'detect.py --shape-predictor ' + side_detection_path + 'left_custom_weights.dat --image '+side_picture+'.jpg', shell= True)
subprocess.run('python ' + front_detection_path+'/detect_face_features.py --shape-predictor '+ front_detection_path + '/shape_predictor_68_face_landmarks.dat --image ' +front_picture+'.jpg', shell= True)
# subprocess.run('python ' + fitting_path + 'fitting_test.py '+ front_picture+' '+ side_picture)
# subprocess.run('blender --python '+cur_path+'/main.py -o ' + cur_path + '/output -f 2', shell=True)