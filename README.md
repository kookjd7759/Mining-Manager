# 암호화폐 채굴 모니터링 프로그램 Mining Manager
![Mining Manager Logo](https://github.com/kookjd7759/Mining-Manager/assets/67672017/0c942f56-db7a-49bf-b2a9-b9b1b119d724)

## 프로젝트 소개
- Mining Manager는 암호화폐 채굴 수행 상태를 수시로 모니터링하는 프로그램입니다.
- Mining Pool 과 Device 와의 Network Connection, Worker의 동작 상태를 모니터링해 문제 발생시 사용자에게 알림을 보냅니다.
-전체 채굴 현황을 요약하여 사용자에게 전송합니다.

- 지원하는 Mining Pool 
  - [kaspa-pool.org](https://kaspa-pool.org)
  - [kas.2miners.com](https://kas.2miners.com)

## 개발 환경
- Front-end : PyQt5
- Back-end : Web Request, Discord API

## 주요 기능
Network 및 Worker 상태를 모니터링 하고, Discord([Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks))를 통해 사용자에게 알림을 전송.
### 전체 실행 화면
![Mining Manager v1.0.0Beta1 Excuted window](https://github.com/kookjd7759/Mining-Manager/assets/67672017/c45f379e-816b-483a-892d-601a76db2e76)



## 세부 기능
### Webhook Menu
![webhook](https://github.com/kookjd7759/Mining-Manager/assets/67672017/99ebe6e3-0fec-48a3-ae34-27235de88943)

Webhook Link와 관련한 메뉴 창
- 저장된 Webhook Link를 표시
- [Edit] : Webhook Link를 수정 및 업데이트 (보조 창을 띄워 입력을 받은 후 적용)
- [Delete] : Webhook Link를 삭제 
- [Connection Test] : 해당 Webhook Link를 통해 Test message(인증 코드 4자리) 전송

### Option Menu
![option](https://github.com/kookjd7759/Mining-Manager/assets/67672017/9c8aa501-559f-42f3-9bb1-cdb247bb7b62)

Option 설정이 가능한 메뉴 창
- [Checking Time (min)] : 채굴 수행 상태를 확인할 주기를 분 단위로 설정
- [Receive notification when] : 알림을 수신할 조건을 설정
- [Receive following information] : 수신할 정보를 설정
- [Reset default values] : 옵션 설정을 기본값으로 변경

### Menu And Excution console 
![menu and excution console](https://github.com/kookjd7759/Mining-Manager/assets/67672017/f8968685-be5a-49ee-bfbb-ebbbe3c6f77c)

- [Quit] : 프로그램 종료
- [Restart] : 프로그램 재시작
- [Start] : 설정된 Webhook과 Option 설정으로 모니터링을 시작
- [Stop] : 모니터링 종료
- Excution Console : 현재 실행 정보를 볼 수 있는 콘솔 화면
