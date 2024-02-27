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



