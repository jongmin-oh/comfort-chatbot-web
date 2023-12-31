#!/bin/bash

# .env 파일 로드
if [[ -f .env ]]; then
    export $(cat .env | xargs)
fi

echo "기존 ${SERVER_NAME} 서버를 중지합니다."

docker_base_dir="/opt/${SERVER_NAME}"
docker stop ${SERVER_NAME} ; docker rm ${SERVER_NAME} ; docker rmi ${SERVER_NAME}

echo "새로운 ${SERVER_NAME} 서버를 빌드합니다."
docker build --build-arg DIR=$docker_base_dir -t ${SERVER_NAME} .

echo "새로운 ${SERVER_NAME} 서버를 시작합니다."
docker run --name ${SERVER_NAME} --restart=always --network=bridge -v $PWD:$docker_base_dir -d -p 80:80 ${SERVER_NAME}:latest
docker logs ${SERVER_NAME} --tail 20 -f