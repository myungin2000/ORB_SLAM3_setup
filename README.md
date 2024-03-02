참고자료

https://www.youtube.com/watch?v=DxqzwBQVCNw => youtube 그대로 따라하면 됨

https://github.com/Mauhing/ORB_SLAM3 => ORB_SLAM3 유튜브에나온 링크

https://github.com/UZ-SLAMLab/ORB_SLAM3 => ORB_SLAM3 원작자 링크

https://github.com/shanpenghui/ORB_SLAM3_Fixed => 여러 문제점을 개선했다고 나온 ORB_SLAM3. 중국어로 되있으니 번역기 돌려야되는 불편함이 있어서 버렸음





##################################################################
핵심 파일 설명 

1)Vocabulary/ORBvoc.txt => ORB_SLAM3 실행을 위해 반드시 들어가는 항목

2)~~~.yaml => 카메라 특성값을 불러오는 파일. para meter를 조절할 수 있으며, fps, 카메라 resolution 등이 들어감. 

3) .so 파일 (확장자가 없는것처럼 보여짐) => .cc파일을 cmake등으로 build 하면 생기는 라이브러리 파일. 저장위치, 데이터 불러오는 위치 지정 및 카메라 세팅 일부 가능




#################################################################
에러 해결법

#에러 관련 참고 사이트 : https://sidosidopy.tistory.com/51



#error : slots_reference does not exist? 와 같은 에러가 뜨는 경우
sed -i 's/++11/++14/g' CMakeLists.txt
를 하고 다시 build 하기. cmakelist.txt 파일이 없다고 뜨면 그 파일이 있는 폴더로 cd (폴더명)으로 찾아가 줘야됨



#opencv설치 후 build 과정에서 stdlib.h 경로 어쩌구 못 부를 때
복사붙이기 한 define이 include앞에 있으면 발생함



#pangolin 어쩌구가 안 뜰 때
sudo idconfig


#orb slam3 build 할 때 안 되는 경우
sudo apt-get install libopenexr-dev   (openexr설치)


#customed 확장자 없는 파일(shared library파일 - 위에 핵심파일설명 3번째) 만들고싶을 때(저장 위치, 데이터 불러오는 위치 지정 가능)
1) ORB_SLAM3폴더의 CMakeLists.txt 파일 열기
2) #Monocular examples 처럼 된 부분에서 두줄 복사해서 원하는 파일 이름 만들어서 붙여넣기
3) 해당 경로에 있는 아무 .cc 확장자 파일을 복사해서 원하는 파일 이름으로 바꾸기
4) ORB_SLAM3 빌드하기 (chmod +x build.sh && ./build.sh )
5) 해당 파일에서 파일 데이터 경로 등 수정하기


# Segmentation fault core dumped 문제
ORB_SLAM3/src/Settings.cc 파일에 들어가서 
560줄 근처의
for(size_t i=0; i<settings.originalCalib2_->size();i++)
부분을
if(settings.sensor_ != System::IMU_STEREO){
    for(size_t i = 0; i < settings.originalCalib2_->size(); i++){
        output << " " << settings.originalCalib2_->getParameter(i);
    }
}
으로 교체



#rs::invalid_value_error ~~~ "option 52" 에러
Examples/Stereo-inertial/stereo_inertial_realsense_D435i.cc 파일의 
142,143번째 줄
// sensor.set_option(RS2_OPTION_ENABLE_AUTO_EXPOSURE, 1);
// sensor.set_option(RS2_OPTION_AUTO_EXPOSURE_LIMIT,5000);
로 주석처리하기

# Camera Calibration
카메라로 찍은 영상의 왜곡을 없야기 위해 Camere Caliration 과정을 반드시 거쳐야한다.

해당 영상을 참고하여 진행하였다
https://www.youtube.com/watch?v=iOmYtms45ho

Calibration을 위해서는 camera calibration checkerboard을 찍은 사진들이 필요하다. 영상 말대로 10개 내외의 사진들을 getImages.py 코드를 이용해 캡쳐하였다.

이후, calibrate_phone.py 코드를 이용하여 Caliration을 진행한다. 코드 안에 사진들의 경로를 설정해주고, 본인이 이용한 camera calibration checkerboard의 크기에 맞게 숫자들을 바꿔준다.

Calibration이 정상적으로 이루어졌다면 VS Code의 터미널에 카메라 파라메터들이 출력된다.

해당 값들은 ORB_SLAM 코드의 yaml 파일에 대입해주고 다시 build 후 ORB_SLAM을 실해해주면 된다.
  
예시  
Camera1.fx: 1.17447062e+03
Camera1.fy: 1.17354335e+03
Camera1.cx: 6.25808153e+02
Camera1.cy: 3.60915223e+02

Camera1.k1: -0.12183388
Camera1.k2: 0.56770901
Camera1.p1: -0.00073029
Camera1.p2: -0.00281733

![image](https://github.com/myungin2000/ORB_SLAM3_setup/assets/143677198/e3db96f9-1eb7-4d96-9666-91ee47e03914)
<img width="563" alt="image" src="https://github.com/myungin2000/ORB_SLAM3_setup/assets/143677198/049fb874-6824-44b6-a39a-4b3e84907756">

![image](https://github.com/myungin2000/ORB_SLAM3_setup/assets/143677198/de2b881b-4825-450b-a45d-161c3e5ae888)


# Webcam 으로 구동

https://robot-vision-develop-story.tistory.com/10
위 사이트에 있는 코드를 그대로 mono_tum.cc 파일에 복붙해주고 다시 빌드 후 '$ ./Examples/Monocular/mono_tum Vocabulary/ORBvoc.txt ./Examples/Monocular/TUM1.yaml'을 통해 실행해 주면 된다.

다만, 에러가 뜰텐데 53번째 줄에 있는 'ORB_SLAM2' 라고 나와있는 부분 두 개를 'ORB_SLAM3'으로 고쳐주면 된다.

웹캠을 쓰니까 TUM1.yaml 파일에 있는 파라메터들도 본인의 카메라에 맞는 것으로 바꿔주도록 한다.







