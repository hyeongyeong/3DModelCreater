import subprocess
import os
import sys
import Detectlandmark.Side_view_detector.detect as side_view_detector
import Detectlandmark.Detect_Facial_Features.detect_face_features as front_view_detector
import MM_fitting.test.fitting_test as fitting
import MM_fitting


cur_path = os.getcwd()
if len(sys.argv) > 2:
    front_picture =sys.argv[1]
    side_picture = sys.argv[2]
else:
    front_picture = 'seok_f'
    side_picture = 'seok_l'


front_detection_path = cur_path + '/Detectlandmark/Detect-Facial-Features/'
side_detection_path = 'Detectlandmark/Side_view_detector/'
fitting_path = cur_path + '/3DMM-fitting/test/'
blender_script_path = cur_path + '/3DModelCreater'
side_view_detector.run('left_custom_weights.dat', side_picture +'.jpg')
front_view_detector.run('shape_predictor_68_face_landmarks.dat', front_picture +'.jpg')
fitting.run(front_picture, side_picture)
# subprocess.run('python test.py', shell=True)
# subprocess('python ' + side_detection_path)