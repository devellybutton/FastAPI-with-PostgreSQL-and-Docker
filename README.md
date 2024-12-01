# FastAPI with PostgreSQL and Docker

> - 1. Creating the PostgreSQL Docker Container
> - 2. Creating the Database
> - 3. Python project setup
> - 4. Connecting the database
> - 5. Model Creation
> - 6. Schema Creation
> - 7. Building the API

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

### 6) 새로운 데이터베이스 생성
```
create database fastapi_database;
```
- 'fastapi_database'라는 이름의 데이터베이스 생성

### 7) 새로운 사용자 생성 후 비밀번호 설정
```
create user myuser with encrypted password 'password';
```
- myuser : 생성할 사용자의 이름
- 'password' : 원하는 대로 변경

### 8) 데이터베이스에 대한 권한을 부여
```
grant all privileges on database fastapi_database to myuser;
```
- myuser라는 사용자에게 fastapi_database라는 DB의 모든 권한을 부여

### 9) 데이터베이스 내부에 접속
```
\c fastapi_database;
```
- `\c` : PostgreSQL에서 데이터베이스를 전환하는 명령어

![image](https://github.com/user-attachments/assets/cede0ee2-0b18-4948-b516-739040c8ff99)

### 10) 프로젝트 폴더에서 파이썬 가상환경 생성 후 실행
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

### 11) 필요한 패키지 설치
```
pip3 install "fastapi[all]" SQLAlchemy psycopg2-binary 
```
- `fastapi[all]` : FastAPI 설치시 추가적인 선택적 기능들도 설치
- `SQLAlchemy` : Python의 ORM 라이브러리
- `psycopg2-binary` : Python에서 PostgreSQL 데이터베이스와 연결하는 데 사용되는 드라이버

![image](https://github.com/user-attachments/assets/450f838e-1d68-4b90-8e10-7f123982c11e)