# CO-NOx Combination Dashboard

가스터빈 센서 데이터를 기반으로 CO/NOX 배출량과 운전 변수 간 관계를 탐색하는 시각화 대시보드.

## 실행 방법

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python src/app.py
```

브라우저에서 `http://127.0.0.1:8050` 접속.

## 테스트

```bash
source .venv/bin/activate
pytest
```
