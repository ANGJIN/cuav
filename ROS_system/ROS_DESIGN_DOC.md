# ROS Design

Created By: inbae Kang
Last Edited: Sep 23, 2019 3:11 PM
Tags: Document,ROS

## 시나리오

![](https://i.imgur.com/N9idcRi.png)

Rail에 고정된 RADAR는 양 끝을 움직이면서 SAR 이미지를 만들어낸다.

동시에 CAMERA는 사진을 찍는다.

두 가지 이미지는 각각 학습된 모델을 통해서 Object Detection한다.

두 가지 정보를 적절하게 활용하여 UAV, 자동차, 사람을 판별한다.

도출된 결과는 확인할 수 있도록 웹 서비스로 제공한다.

이 과정 중에 모든 데이터 교환은 ROS의 Node 및 Topic으로 정의되어 진행된다.

## ROS 구성

- ROS 구성도 (노드 구성도)

    ![](https://i.imgur.com/PH41JD3.png)

- ROS Node (레일 노드, 레이더 노드, 등) 정의 (생성 시기 / 생성 조건 / 토픽 / 입력 출력 등)
    - 각 노드의 생성 시기 : 기본적으로 모든 노드를 Static하게 생성하고 시작.
    - 생성 조건 : 없음
    - 토픽
        - **is_stop** : rail이 끝에 도달해서 get_data 노드가 데이터를 그만 수집하도록
        - **raw** :  얻은 raw data를 analyzer 노드가 IFFT 처리, binary text를 wav파일로 변환하도록
        - **wav** : make_sar_image 노드가 변환된 wav파일로 SAR이미지를 만들도록
        - **img_radar** : classifier_radar 노드가 SAR이미지를 통해서 분류하도록
        - **img_camera** : classifier_camera 노드가 분류하도록
        - **result_camera, result_radar** : Decision노드가 RADAR와 CAMERA를 통해서 받은 데이터를 바탕으로 결과를 도출할 수 있도록
        - **result** : 최종 결과물을 위한 토픽

- ROS Message Type 정의 (노드에서 사용되는 메시지 정의)

    **[msg type](http://wiki.ros.org/msg) 에 명시된 primitive로 더 구체적으로 구현 예정, message 이름은 아직 미정**

    - railstop : boolean(한 주기 끝)
    - raw : byte array(binary data)
    - wav : 여름 기준 float array와 int(time)으로 구성. 아직 확실하게 모르겠음.
    - img_radar, img_camera : byte array(그림 file)
    - result_radar, result_camera : string(차/사람/드론), float(거리?)
    - result(최종) : byte array(카메라 이미지), byte array(SAR 이미지), string(차/사람/드론), float(거리?)

## 리허설 (처음 노드 구성부터 결과값을 얻기 까지의 진행을 기술)

1. ROS 시스템이 구동되고(master 노드 및 모든 노드들이 생성 됨), RAIL이 움직이면서 RADAR가 데이터 수집을 시작한다. 
2. 동시에 CAMERA도 사진을 촬영하고 모델을 통해서 분류를 한다. (여기서 카메라가 얼마나 사진을 수집하고 분류할 수 있을지에 따라서 어떻게 처리를 할지 추후에 결정) 
3. 레일이 끝에 도달하면,  is_stop 토픽에 한 주기가 끝났다고 message를 publish. 
4. 해당 토픽을 subscribe하고 있는 get_data node는 지금까지 쌓인 binary data를 wav 토픽에 publish함.
5. IFFT 및 wav 데이터로 변환 후에 make_sar_image 노드가 받을 수 있도록 publish함.
6. SAR Image를 만들고 img_radar 토픽에 publish하고, classifier_radar노드가 분류.
7. RADAR와 CAMERA는 각각 result_radar, result_camera 토픽에 publish하여 Decision노드가 받아서 두 정보를 같이 이용할 수 있도록 함. ( 두 정보를 어떻게 사용할지에 대해서는 추후에 결정 )
8. Decision 노드는 최종 결과를 내서 WEB노드가 받아서 visualization 하도록 publish.