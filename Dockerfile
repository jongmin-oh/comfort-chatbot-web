FROM python:3.11.5-slim

ARG DIR
ENV DIR $DIR

# 디렉터리 생성
RUN mkdir $DIR

# 소스코드 복사
COPY . $DIR

#작업 폴더 설정
WORKDIR $DIR

RUN pip install -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port", "80"]