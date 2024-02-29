import cv2

cap = cv2.VideoCapture('/Users/myungin/Desktop/ORB_SLAM/calibration/CameraCalibration-main/광각 휴대폰 캡쳐/vid.mp4')

num = 0

while cap.isOpened():

    succes, img = cap.read()

    k = cv2.waitKey(5)

    if k == 27:
        break
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('/Users/myungin/Desktop/ORB_SLAM/calibration/CameraCalibration-main/광각 휴대폰 캡쳐/img' + str(num) + '.png', img)
        #/Users/myungin/Desktop/ORB_SLAM/calibration/CameraCalibration-main
        print("image saved!")
        num += 1

    cv2.imshow('Img',img)

# Release and destroy all windows before termination
cap.release()

cv2.destroyAllWindows()