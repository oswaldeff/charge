## 결제시스템 아키텍처
![architecture](https://user-images.githubusercontent.com/66583879/180588967-ac750b23-eaa6-4568-94a5-dd77eacde972.png)

## 데이터베이스 다이어그램
![erd](https://user-images.githubusercontent.com/66583879/180588962-2f57e93f-7d6d-4b4e-bdff-401af4101e49.png)

## 프로젝트 개요
1. db_gen()은 local에서 migrate & runserver로 테스트db 생성용도입니다.
2. 등록된 카드와 아임포트를 통해 포인트 충전을 할 수 있도록 하였습니다.
3. 충전소 이용의 경우 프론트에서 결제방법에 대한 정보를 받아 두가지 시나리오로 구현
4. 후불의 경우 비동기로 redis&celery로 task수행, db업데이트 후 redis의 해당 key-value삭제

## 구현기능
- [x] 데이터베이스 모델링
- [X] 아임포트를 이용하여 포인트충전 구현
- [ ] 두가지 시나리오 구현
- [ ] 비동기task redis&celery로 구현

## KPT
- Keep:
    - 결제시스템에 대한 경험이 없었는데, 결제시스템의 구현방법에 대해 생각해볼 수 있는 기회였습니다.
- Problem:
    - 결제시스템 요구사항에 대하여 명확한 DB relation을 파악하지 못하여 DB modeling에 대한 수정이 빈번하였습니다.
    - 결제가 실패할 경우 transaction처리를 제대로 하지 못하였습니다.
    - 두가지 시나리오에 대한 비동기 task를 구현하지 못하였습니다.
- Try:
    -