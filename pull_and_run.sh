if [[ -f .env ]]; then
    export $(cat .env | xargs)
fi

docker stop ${SERVER_NAME} ; docker rm ${SERVER_NAME} ; docker rmi ${AWS_ECR_URL}/${SERVER_NAME} ; docker rmi ${SERVER_NAME}

aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin ${AWS_ECR_URL}
docker pull ${AWS_ECR_URL}/${SERVER_NAME}:latest

docker tag ${AWS_ECR_URL}/${SERVER_NAME}:latest ${SERVER_NAME}:latest
docker run --name ${SERVER_NAME} --restart=always --network=bridge -d -p ${PORT}:${PORT} ${SERVER_NAME}:latest