# 🛠️ 3주차 실습: 법선-접선좌표(n-t), 극좌표(r-θ) 및 원통/구면좌표계

> **Author / Rights Holder:** 전북대학교 생물산업기계공학과 유동수 (ryudongsoo@jbnu.ac.kr)

[뒤로가기(한국어 메인)](../README.md)

본 폴더는 **생물역학 3주차 강의**에서 다룬 곡선운동 좌표계(법선-접선좌표, 극좌표, 원통/구면좌표계) 관련 파이썬 시뮬레이션 및 3D 동역학 GIF 애니메이션 실습 자료입니다.

## 📌 제공되는 시뮬레이션 및 애니메이션 코드

### 1. 교재 예제 (Examples)
- `ex2_7_car_curve.py` / `.gif`: 예제 2/7 곡선 도로 주행 자동차 ($n\text{-}t$ 좌표계)
- `ex2_8_rocket_flight.py` / `.gif`: 예제 2/8 로켓 비행 궤적 및 속도/가속도 ($n\text{-}t$ 좌표계)
- `ex2_9_robot_arm.py` / `.gif`: 예제 2/9 로봇 팔의 신축과 회전 운동 ($r\text{-}\theta$ 극좌표계)
- `ex2_10_radar_tracking.py` / `.gif`: 예제 2/10 레이더의 비행체 극좌표 추적
- `ex2_11_power_screw.py` / `.gif`: 예제 2/11 동력 나사 칼라의 3D 원통나선 운동

### 2. 연습 문제 (Problems)
- `prob2_101_parabolic_slot.py` / `.gif`: 문제 2/101 포물선 슬롯과 수직 가이드 봉의 핀 운동
- `prob2_131_baseball_throw.py` / `.gif`: 문제 2/131 야구 선수의 원운동 송구 및 극좌표 레이더 추적
- `prob2_135_corkscrew.py` / `.gif`: 문제 2/135 코르크 스크루(원통나선 곡률반지름 및 가속도)
- `prob2_136_radar_jet.py` / `.gif`: 문제 2/136 레이더의 제트기 구면좌표계($R\text{-}\theta\text{-}\phi$) 추적
- `prob2_140_robot_manipulator.py` / `.gif`: 문제 2/140 산업용 로봇의 원통좌표계($r\text{-}\theta\text{-}z$) 기구학

### 3. 좌표계 종합 비교 시각화 자료 (Coordinate Systems Comparison)
- `coord_systems_3d_comparison.py` / `.png`: 3차원 공간 직각좌표계, 원통좌표계, 구면좌표계 4-in-1 정밀 비교 다이어그램

### 4. 과제 뼈대 코드 (Homework)
- `homework_skeleton_polar.py`: 극좌표계 가속도 계산 실습 뼈대 코드

## ▶️ 실행 방법
터미널에서 아래 명령어로 스크립트를 실행합니다. (사전에 `numpy`, `matplotlib` 설치 필수)
```bash
python prob2_140_robot_manipulator.py
```

---
## 📝 변경 이력 (Changelog)
- **2026-09-13** [[ryu-dongsoo](mailto:ryudongsoo@jbnu.ac.kr)] feat: 문제 2/140, 2/136, 2/135, 2/131, 2/101 3D 정밀 애니메이션 및 시각화 전면 개편
- **2026-05-22** [[ryu-dongsoo](mailto:ryudongsoo@jbnu.ac.kr)] feat: 3주차 실습 안내 및 뼈대 코드 추가
