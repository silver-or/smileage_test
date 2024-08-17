### 💡 작업동기
- 웹캠으로 이미지 캡쳐 후 감정 분석 하여 사용자에게 표정 관리 트레이닝을 도와주는 시스템

### 🔑 주요 변경사항

- npm install @mui/material @emotion/react @emotion/styled
- npm install @mui/icons-material
- npm install axios


- '테스트 시작하기' 버튼을 누르면 3초 후 이미지를 캡쳐하여 모달로 결과 띄우는 기능까지만 우선 구현했습니다.
- main.py를 만들어 fastapi 코드를 작성했습니다.
- axios를 이용해 API 서버와 통신했습니다.
- jsconfig.json 파일을 만들어 절대경로 설정하였습니다.
- mui 이용해서 디자인 개선했습니다.
- 누끼 따기 기능 추가했습니다. (08.16)
- 누끼 딴 후 감정별(happy, sad, angry) 배경 삽입하는 기능 추가했습니다. + 코드 최적화 (08.17)
- 추후 계속해서 업데이트할 예정입니다.
  + 다른 감정 배경 삽입 및 배경 이미지 원본 비율 유지하는 코드 작성 필요

### 🏞 스크린샷
- 08.15 (기본 실행 화면)
![image](https://github.com/user-attachments/assets/17088203-06a8-446d-9f29-893173fb3c85)
- 08.16 (누끼 따기 기능 추가)
![image](https://github.com/user-attachments/assets/a15a1482-7601-431e-94a9-20ed136817a5)
- 08.17 (누끼 딴 후 배경 삽입)
![image](https://github.com/user-attachments/assets/c36a18af-4583-4059-bc3c-55090f916e75)

