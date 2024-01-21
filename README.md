# 암호화폐 채굴 모니터링 프로그램 Mining Manager (v1.0.0-Alpha)
![Mining Manager Logo](https://github.com/kookjd7759/Mining-Manager/assets/67672017/0c942f56-db7a-49bf-b2a9-b9b1b119d724)

## 프로젝트 소개
- Mining Manager는 암호화폐 채굴 수행 상태를 수시로 모니터링하는 프로그램입니다.
- Mining Pool 과 Device 와의 Network Connection, Worker의 동작 상태를 모니터링해 문제 발생시 사용자에게 알림을 보냅니다.
- (기능 추가 예정) 전체 채굴 현황을 요약하여 사용자에게 전송합니다.

## 개발 환경
- Front-end : PyQt5
- Back-end : Web Request, Discord API

## 기능
설정한 옵션을 따라 Network 및 Worker 상태를 모니터링 하고, Discord([Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks))를 통해 사용자에게 알림을 전송
### 전체 실행 화면
![Mining Manager v1 0 0-Alpha 실행 화면](https://github.com/kookjd7759/Mining-Manager/assets/67672017/e6bad2bc-7b0c-4048-9bd5-078596bb2502)

### 세부 기능
#### Webhook Menu
![Mining Manager v1 0 0-Alpha 웹훅 메뉴](https://github.com/kookjd7759/Mining-Manager/assets/67672017/d58983a4-775f-44d2-8884-f9f926e96305)

Webhook Link와 관련한 메뉴 창
- 저장된 Webhook Link를 표시
- [Edit] : Webhook Link를 수정 및 업데이트 (보조 창을 띄워 입력을 받은 후 적용)
- [Delete] : Webhook Link를 삭제 
- [Connection Test] : 해당 Webhook Link를 통해 Test message(인증 코드 4자리) 전송

#### Option Menu
![Mining Manager v1 0 0-Alpha 옵션 메뉴](https://github.com/kookjd7759/Mining-Manager/assets/67672017/1feb4cf8-2910-43bc-b2e4-6763efc0ddf2)

Option 설정이 가능한 메뉴 창
- [Checking Time (min)] : 채굴 수행 상태를 확인할 주기를 분 단위로 설정
- [Receive notification when] : 알림을 전송할 조건을 설정
- [Receive following information] : 수신할 정보를 설정
- [Reset default values] : 옵션 설정을 기본값으로 변경

#### Main Menu
![Mining Manager v1 0 0-Alpha 4btn 메뉴](https://github.com/kookjd7759/Mining-Manager/assets/67672017/85780a89-5a7e-4442-9a53-6f16fcb41f52)

프로그램 동작에 관한 메뉴 창
- [Quit] : 프로그램 종료
- [Restart] : 프로그램 재시작
- [Start] : 설정된 Webhook과 Option 설정으로 모니터링을 시작
- [Stop] : 모니터링 종료

#### Excution Colsole Menu
![Mining Manager v1 0 0-Alpha 하단 메뉴](https://github.com/kookjd7759/Mining-Manager/assets/67672017/d9fe6e54-086b-4ebd-a2d1-e5966f9a8716)

현재 모니터링 실행 정보를 볼 수 있는 콘솔 화면
