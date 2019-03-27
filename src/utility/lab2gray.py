
import numpy as np
import cv2

lab_arr = np.array([[[139,124,149]]])
# rgb_arr = cv2.cvtColor(lab_arr, cv2.COLOR_LAB2RGB)
gray = cv2.cvtColor(lab_arr, cv2.COLOR_RGB2GRAY)
print(gray)
