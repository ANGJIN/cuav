# Daily log of Kyungyeon Park

## 2019-09-04 ~ 2019-09-06

### 2019-09-04
- 구체적인 주제 회의
  - 센서 개발
  - 웹 인터페이스
  - 데이터 전송 딜레이 최적화
  - ROS 및 웹 연동
  
### 2019-09-05
- 논문 읽기
  - Realization of an Autonomous, Air-to-Air Counter Unmanned Aerial System (CUAS)
  
### 2019-09-06
- `counterUAV` 안의 `README.md` 수정
  - ros 설치 방법이 구체적이지 않아 조금 더 구체적으로 작성해 놓음
- `RNN.py` 수정
  - `/home/project/counterUAV/ROS_system/catkin_ws/src/ros_counteruav/scripts` 안의 `RNN.py`를 수정함
  - `time_list.npy`가 `RNN.py`에서 인식이 되지 않아 상대경로에서 절대경로로 바꿔 놓음
- `ROS_system` 파일 실행
  - `$ rosrun ros_counteruav scripts/start.sh` 명령어를 통해 `ROS_system`를 실행시켜 봄
  - [결과](https://ibb.co/0hWLjYv) >> 이렇게 뜨는게 맞는지 모르겠음

<br/>

## 2019-09-09 ~ 2019-09-13

### 2019-09-09
- 코드 분석
  - `start.sh`안의 프로그램 실행 구조 파악
  - `visualizer.py`, `data_analyzer.py`, `data_receiver.py`, `fake_data_sender.py`안의 코드들을 분석해봄
  
### 2019-09-10
- 논문 읽기
  - Combination of Radar and Audio Sensors for Identification of Rotor-type Unmanned Aerial Vehicles
- ROSpy 공부

### 2019-09-11
- 전체 회의
  - **Making rail using Stepping Motor** 로 나의 목표가 정해짐 > 9월 전에 제작을 목표로
- Stepping Motor 조사
  - stepping motor의 종류, 장단점에 대해 알아봄
  - 만들어야 할 rail의 형태를 조사해 봄

### 2019-09-12
- Stepping Motor 조사
  - 구매 어떻게 할지 알아봄
  - 이번주 토요일에 radar팀이 radar를 받아보고, 크기와 무게를 알려주면 모터와 프로파일 선정 예정
- job fair 구경

### 2019-09-13
- 전체 회의
  - 계획
    - ~ 9/20: 레일 및 모터 구매(스텝으로 2인치 움직이고 멈췄다가 가는걸 반복하는 알고리즘을 구현(모터 구매 하면서 해봄))
    - ~ 9/25: 제작
    - ~ 9/30: 초당 2인치씩 움직이도록 제어
  - 앞으로 해야할 일
    - 랩에 stepping motor 있는지 확인하기
    - 제어 부분을 빨리 시작해야 함 -> 별매인 제품들 먼저 구매하고 라즈베리파이로 먼저 개발 시작
    - 레일을 고정하는것 어떻게 할지 생각해보기 -> 하드웨어를 전반적으로 스케치 해봤으면 좋겠음
    -  바닥에 고정시키면 레이더 전파가 반사돼서 방해가 됨 -> 1.1m~1.5m정도 지면에서 떨어져 있었으면 좋겠음. 바닥에서 어느정도 떨어져야 할지 최솟값 구하기
    - 레이더 받은거를 그대로 사용하지는 않음. 프로파일같은거 다 삭제하고 레이더만 남기면 좋을듯. 안테나를 작은 프링글스통만한거를 사용하는쪽으로

- 랩에 stepping motor 있는지 확인 -> Car E가 찾아봐야 아는데 지금 휴가를 가서 다다음주에 돌아온다고 함. 일단 교수님께 여쭤본 상태
- 라즈베리파이 B2를 받아 Raspbian 설치 및 파이썬 설치

<br/>

## 2019-09-16 ~ 2019-09-20

### 2019-09-16
- rail을 만들때 필요한 stepper motor와 driver를 선정
  - [stpper motor](https://www.amazon.com/Usongshine-Geared-Stepper-Motor-Ratio/dp/B07V359RFB/ref=sr_1_5?keywords=nema+17&qid=1568662364&s=hi&sr=1-5)
  - [driver](https://www.amazon.com/Stepper-Driver-TB6600-Controller-Single/dp/B07H55MH23/ref=asc_df_B07H55MH23/?tag=hyprod-20&linkCode=df0&hvadid=309802506143&hvpos=1o4&hvnetw=g&hvrand=13175866527852851402&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9016722&hvtargid=pla-558289099173&psc=1)

### 2019-09-17
- rail을 만들때 필요한 ball screw와 coupler 선정
  - [ball screw](https://www.amazon.com/CNCCANEN-SFU1605-1200mm-Antibacklash-Machining-Ballscrew/dp/B07T1QM8KN/ref=sr_1_45?keywords=ballscrew&qid=1568730875&sr=8-45)
  - [coupler](https://www.amazon.com/YOTINO-Flexible-Couplings-RepRap-3D/dp/B07DC2CV6T/ref=sr_1_4?crid=3I30KJH6BL5VR&keywords=nema+17+coupler&qid=1568733483&s=industrial&sprefix=nema17+cou%2Cindustrial%2C158&sr=1-4)
- stepper motor를 제어하기 위한 python 코드 개발

### 2019-09-18
- [rail 초안 작성](https://ibb.co/PcphmZz): 선에 가해지는 스트레스가 지속적으로 발생할 것 같다는 피드백을 받음
  => 먼저 레일을 완성하고 radar 팀과 상의하여 최대한 간섭이 없는 방향으로 설치할 예정
- stepper motor를 제어하기 위한 python 코드 개발

### 2019-09-19
- 주문한 stepper motor와 drive를 수령함
- stepper motor 조립
  - [stepper motor와 driver를 조립함](https://ibb.co/pdK1Vh2)
- stepper motor 실행
  - [작성한 파이썬 코드를 가지고 모터를 작동시켜 봄](https://youtu.be/C7Emrwi_g5c)
  - 주문한 driver의 어뎁터가(12V, 3A) 아직 도착하지 않아 기존에 있는 어뎁터(12V, 1A)를 사용하여
작동시에 조금 속도가 느림(모터는 12V, 1.6A)

### 2019-09-20
- 영어 수업
- [rail 관련 위키](https://github.com/seonghapark/cuav/wiki/Making-Rail) 작성
- 전체 회의
  - 계획
    - 아직 Eric 교수님이 학교에 오시지 않아 주문이 제대로 안되는 상태. 다음주 안으로 레일까지 제작할 예정

<br/>

## 2019-09-23 ~ 2019-09-27

### 2019-09-23
- 레이더 코드를 읽어보고 분석해 봄

### 2019-09-24
- Ubuntu 18.04에서 kinetic을 사용하기 위해 docker에 대해 공부함
- Eric 교수님께서 부품 주문을 하셨고, 아직 오지 않은 상태

### 2019-09-25
- 부품이 아직 오지 않았음
- ROS kinetic을 Docker위에서 실행시켜 봄
  - [관련 Wiki](https://github.com/seonghapark/cuav/wiki/Run-in-Ubuntu-18.04) 작성
  
### 2019-09-26
- 전체 회의
- 라즈베리파이에 ROS 설치 시도 >> 계속 오류 발생. OS를 Raspbian이 아닌 Ubuntu mate으로 바꿔서 시도 예정

### 2019-09-27
- 영어 수업
- Motor driver의 어뎁터가 도착함. 드라이버와 연결해서 정상 작동 확인해 봄
- 다음 값을 계산해 [Wiki](https://github.com/seonghapark/cuav/wiki/Making-Rail#calculate-step-size)에 작성
  - 모터가 정확히 한 바퀴 도는데 필요한 Step
  - 모터를 돌려 물체가 1 inch 가는데 필요한 Step

<br/>

## 2019-09-30 ~ 2019-10-04

### 2019-09-30
- 라즈베리파이에 ros kinetic 설치를 시도해봄
  - 포맷하고 다시해봤는데도 저번주 목요일과 같은 오류가 계속 발생
  - 다른 버전의 raspbian으로 시도해 보고, 안되면 다른 OS 사용 예정
  - raspbian이 라즈베리파이가 추천하는 OS이기 때문에 최대한 rapbian을 사용하는 방향으로 가려고 함.

### 2019-10-01
- 레일이 도착, 레일을 조립함
  - coupler는 도착하지 않아 아직 모터와 연결을 못한 상태
  - profile을 새로 사고 레일 위에 올릴 받침대는 직접 만들어야 할듯
- radar 팀의 세미나를 잠깐 들음

### 2019-10-02
- rail 라즈베리파이에 raspbian jessie를 깔아봄
  - raspbian buster에는 ros kinetic이 안깔리는 것을 확인
- radar 팀의 세미나를 들음

### 2019-10-03
- fire starter 수업을 들음.

<br/>

## 2019-10-07 ~ 2019-10-11

### 2019-10-10
- profile, coupler, nut housing이 도착함.
- 조립을 하고 필요한 connector를 3D프린터로 모델링함.

### 2019-10-11
- 모델링한 결과물이 출력됨.
- KSQ에 부품과 맞는 나사가 없어 사러 갔다 옴.
- 관련 [Wiki](https://github.com/seonghapark/cuav/wiki/Making-Rail#making-rail)를 작성함.

<br/>

## 2019-10-14 ~ 2019-10-18

### 2019-10-14
- fire starter 수업을 들음.

### 2019-10-15
- 모터를 고정시킬 connector를 만들어야 한다는걸 꺠달음.
- BK12, BF12를 다시 조립하고 치수를 정확하게 측정하여 도면을 그림.
- 영어수업

### 2019-10-16
- 모터까지 고정시킬 connector를 새로 모델링함.
- 레이더를 고정시킬 connector를 모델링함.

### 2019-10-17

### 2019-10-18


## 2019-10-21 ~ 2019-10-25

### 2019-10-21

### 2019-10-22

### 2019-10-23

### 2019-10-24

### 2019-10-25


## 2019-10-28 ~ 2019-11-01

### 2019-10-28

### 2019-10-29

### 2019-10-30
