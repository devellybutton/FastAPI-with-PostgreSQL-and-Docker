# FastAPI with PostgreSQL and Docker

> - 1. [Creating the PostgreSQL Docker Container](https://github.com/devellybutton/FastAPI-with-PostgreSQL-and-Docker?tab=readme-ov-file#1-creating-the-postgresql-docker-container)
> - 2. [Creating the Database](https://github.com/devellybutton/FastAPI-with-PostgreSQL-and-Docker?tab=readme-ov-file#2-creating-the-postgresql-docker-container)
> - 3. [Python project setup and connecting the database](https://github.com/devellybutton/FastAPI-with-PostgreSQL-and-Docker?tab=readme-ov-file#3-python-project-setup-and-connecting-the-database)
> - 4. [Model Creation](https://github.com/devellybutton/FastAPI-with-PostgreSQL-and-Docker?tab=readme-ov-file#4-model-creation)
> - 5. [Schema Creation](https://github.com/devellybutton/FastAPI-with-PostgreSQL-and-Docker?tab=readme-ov-file#5-schema-creation)
> - 6. [Building the API](https://github.com/devellybutton/FastAPI-with-PostgreSQL-and-Docker?tab=readme-ov-file#6-building-the-api)

---

## 1. Creating the PostgreSQL Docker Container

### 1) Docker Hub에서 postgres:alpine 이미지를 다운로드
```
docker pull postgres:alpine
```
- Alpine Linux : 작고 가벼운 Linux 배포판
- 기본적인 PostgreSQL 이미지보다 크기가 작음.
- 다운로드 시간이 짧음, 컨테이너를 실행할 때 메모리 및 디스크 공간을 절약할 수 있음.

### 2) 도커 이미지 목록 표시
```
docker images
```

- <b>도커 이미지</b>
    - 컨테이너를 생성하기 위한 템플릿 또는 파일 시스템의 스냅샷
    - 애플리케이션과 그에 필요한 환경을 포함하는 읽기 전용 템플릿

### 3) PostgreSQL 데이터베이스를 Docker 컨테이너에서 실행
```
docker run --name fastapi-postgres -e POSTGRES_PASSWORD=비밀번호 -d -p 5432:5432 postgres:alpine
```
- `--name fastapi-postgres`: 컨테이너의 이름을 fastapi-postgres로 지정
- `-e POSTGRES_PASSWORD=비밀번호`: 환경변수 POSTGRES_PASSWORD를 설정하여 PostgreSQL의 비밀번호를 지정
- `-d`: 백그라운드에서 컨테이너를 실행합니다 (Detached 모드).
- `-p 5432:5432`: 호스트의 5432 포트를 컨테이너의 5432 포트와 매핑
- `postgres:alpine`: 사용할 Docker 이미지는 postgres의 alpine 태그 버전

<details>
<summary>참고) 도커 관련 명령어</summary>

### 현재 실행 중인 도커 컨테이너 상태 확인
```
docker ps
```
- ps : process status의 약자

### 종료된 컨테이너 목록까지 상태 확인
```
docker ps -a
```

### 특정 포트를 사용하는 프로세스 확인
```
netstat -ano | findstr :5432
```
- `Ctrl + Shift + Esc` 또는 `Ctrl + Alt + Del`을 누르고 "작업 관리자" 선택
- PID 찾아서 "작업 끝내기"

### 이미 존재하는 도커 컨테이너 실행
```
docker start fastapi-postgres
```
- fastapi-postgres 라는 컨테이너를 실행
- ps 명령어로 확인해보면 STATUS가 변경되어 있음.

</details>

### 4) 실행 중인 도커 컨테이너 안에서 새로운 명령어를 실행
```
docer exec --it fastapi-postgres bash
```
- 위 명령어는 컨테이너가 실행중이어야 가능함.
- 'fastapi-postgres'라는 이름을 가진 실행 중인 컨테이너에 bash 쉘 열기
- `-i` : 인터랙티브 모드 (컨테이너와 상호작용 가능)
- `-t` : 터미널을 할당

![image](https://github.com/user-attachments/assets/16eccde7-c55d-44c4-a2db-e69f508c129e)

### 5) PostgreSQL에 접속
```
psql -U postgres
```
- `psql` : PostgreSQL과 상호작용하는 커맨드라인 클라이언트
- `-U postgres` : postgres라는 사용자로 DB에 접속함.

-----

## 2. Creating the PostgreSQL Docker Container

### 1) 새로운 데이터베이스 생성
```
create database fastapi_database;
```
- 'fastapi_database'라는 이름의 데이터베이스 생성

### 2) 새로운 사용자 생성 후 비밀번호 설정
```
create user myuser with encrypted password 'password';
```
- myuser : 생성할 사용자의 이름
- 'password' : 원하는 대로 변경

### 3) 데이터베이스에 대한 권한을 부여
```
grant all privileges on database fastapi_database to myuser;
```
- myuser라는 사용자에게 fastapi_database라는 DB의 모든 권한을 부여

### 4) 데이터베이스 내부에 접속
```
\c fastapi_database;
```
- `\c` : PostgreSQL에서 데이터베이스를 전환하는 명령어

![image](https://github.com/user-attachments/assets/cede0ee2-0b18-4948-b516-739040c8ff99)

### 5) 프로젝트 폴더에서 파이썬 가상환경 생성 후 실행
생성
```
python -m venv venv
```
실행
```
.\venv\Scripts\Activate
```

<details>
<summary>참고) 가상 환경 비활성화 명령어</summary>

```
deactivate
```

</details>

### 6) 필요한 패키지 설치
```
pip3 install "fastapi[all]" SQLAlchemy psycopg2-binary 
```
- `fastapi[all]` : FastAPI 설치시 추가적인 선택적 기능들도 설치
- `SQLAlchemy` : Python의 ORM 라이브러리
- `psycopg2-binary` : Python에서 PostgreSQL 데이터베이스와 연결하는 데 사용되는 드라이버

![image](https://github.com/user-attachments/assets/450f838e-1d68-4b90-8e10-7f123982c11e)

---

## 3. Python project setup and connecting the database

### 1) __init__.py 파일, database.py 파일 생성 후 database.py 파일에 다음 코드 작성

<details>
<summary> database.py </summary>

```
import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
import os
from dotenv import load_dotenv

# .env 파일에서 환경변수 읽기
load_dotenv()

# 환경변수에서 DATABASE_URL 가져오기
DATABASE_URL = os.getenv("DATABASE_URL")

engine = _sql.create_engine(DATABASE_URL)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()
```

</details>

- `create_engine` : SQLAlchemy에서 DB와의 연결 설정
- `sessionmaker` : SQLAlchemy에서 DB와의 세션 생성
- `autocommit=False` : 명시적으로 커밋하기 전까지 DB 변경이 반영되지 않음.
- `bind=engine` : engine 객체를 세션에 바인딩. 이 세션에서 실행되는 모든 쿼리가 이 연결을 통해 실행
- `SessionLocal` : 세션을 생성할 때 사용할 클래스를 반환
- `declarative_base()` : SQLAlchemy ORM에서 사용할 기본 클래스인 Base를 생성
    - 이 Base 클래스를 상속받은 클래스들은 데이터베이스 테이블과 매팅됨. 

<details>
<summary>파이썬에서 환경변수 로드</summary>

### .env 파일 여부
- <b>.env 파일 사용하여 환경변수 설정</b> : `load_dotenv()`를 통해 .env 파일을 읽고, `os.getenv()`를 사용하여 환경변수 불러오기
- <b>.env 파일 없이 시스템 환경변수에만 의존</b> : `os.getenv()`만 사용

### 환경변수 잘 불러왔는지 확인
print로 직접 출력
```
import os

# 환경변수에서 DATABASE_URL 값을 가져오기
DATABASE_URL = os.getenv("DATABASE_URL")

# 가져온 값을 출력하여 확인
if DATABASE_URL:
    print(f"DATABASE_URL: {DATABASE_URL}")
else:
    print("환경변수 DATABASE_URL이 설정되지 않았습니다.")
```

환경변수 목록 출력하기
```
import os

# 환경변수 목록 출력
print("현재 환경변수 목록:")
for key, value in os.environ.items():
    print(f"{key}: {value}")
```
- `os.environ` : 모든 환경변수를 딕셔너리 형태로 제공

</details>
<details>
<summary>파이썬 터미널에서 출력</summary>

```
python 파일명.py
```

</details>

---

## 4. Model Creation

---

## 5. Schema Creation

---

## 6. Building the API

---

### 참고 링크

- [FastAPI with PostgreSQL and Docker](https://youtu.be/2X8B_X2c27Q?feature=shared)
