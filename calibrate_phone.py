import numpy as np
import glob, cv2

criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30 ,0.001)

objp = np.zeros((10*7,3),np.float32)

objp[:,:2] = np.mgrid[0:10,0:7].T.reshape(-1,2)

objpoints = []
imgpoints = []

images = glob.glob('/Users/myungin/Desktop/ORB_SLAM/calibration/CameraCalibration-main/광각 휴대폰 캡쳐/*.png')

for name in images:
    img = cv2.imread(name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (10, 7), None)

    if ret == True:

        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        imgpoints.append(corners2)

        img = cv2.drawChessboardCorners(img, (10, 7), corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(200)
cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

print("Camera Calibrated : ", ret)
print("\nCamera Matrix :\n",mtx)
print("\nDistortion Parameters:",dist)
print("\nRotation Vectors :\n",rvecs)
print("\nTranslation Vectors:\n",tvecs)

img = cv2.imread('/Users/myungin/Desktop/ORB_SLAM/calibration/CameraCalibration-main/광각 휴대폰 캡쳐/img0.png')

h,w = img.shape[:2]

newcameraMtx, roi = cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

dst = cv2.undistort(img,mtx,dist,None,newcameraMtx)

x,y,w,h = roi

dst = dst[y:y+h,x:x+w]

cv2.imwrite('calibRes.png',dst)

np.savez('calib.npz',ret=ret,mtx=mtx,dist=dist,rvecs=rvecs,tvecs=tvecs)

mean_error = 0

for i in range(len(objpoints)):

    imgpoints2,_ = cv2.projectPoints(objpoints[i],rvecs[i],tvecs[i],mtx,dist)

    error = cv2.norm(imgpoints[i],imgpoints2,cv2.NORM_L2)/len(imgpoints2)
    mean_error += error

print("Total error : {0}".format(mean_error/len(objpoints)))