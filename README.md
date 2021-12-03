# CloudComputing_P2

 
 For running spark job without docker on single ec2 instance with:\
 connect ec2 instance using its Public DNS:\
 ec2-3-84-42-216.compute-1.amazonaws.com\
 with phil.pem Auth Key\
$ cd spark\
$ bin/spark-submit wine.py --master local-cluster[4,1,1024]\

For running in docker switch to this folder\
$ cd e/home/c2-user/docker\

and pull the image \
$ docker pull philfeiran/cs643_project2:wine-prediction \

build docker and create repository\
$ sudo docker build -t --local/wine-prediction .\
$ aws ecr create-repository --cs643p2 docker-rep\
$ sudo docker tag local/wine-prediction ec2-3-84-42-216.compute-1.amazonaws.com\docker-rep:wine-prediction\
$ sudo docker push ec2-3-84-42-216.compute-1.amazonaws.com\docker-rep:wine-prediction\

run the application with following variable\
$ DOCKER_IMAGE_NAME=ec2-3-84-42-216.compute-1.amazonaws.com/docker-rep:wine-prediction
$ DOCKER_CLIENT_CONFIG=hdfs:///user/hadoop/config.json
$ spark-submit --master yarn \
--deploy-mode cluster \
--conf spark.executorEnv.YARN_CONTAINER_RUNTIME_TYPE=docker \
--conf spark.executorEnv.YARN_CONTAINER_RUNTIME_DOCKER_IMAGE=$DOCKER_IMAGE_NAME \
--conf spark.executorEnv.YARN_CONTAINER_RUNTIME_DOCKER_CLIENT_CONFIG=$DOCKER_CLIENT_CONFIG \
--conf spark.executorEnv.YARN_CONTAINER_RUNTIME_DOCKER_MOUNTS=/etc/passwd:/etc/passwd:ro \
--conf spark.yarn.appMasterEnv.YARN_CONTAINER_RUNTIME_TYPE=docker \
--conf spark.yarn.appMasterEnv.YARN_CONTAINER_RUNTIME_DOCKER_IMAGE=$DOCKER_IMAGE_NAME \
--conf spark.yarn.appMasterEnv.YARN_CONTAINER_RUNTIME_DOCKER_CLIENT_CONFIG=$DOCKER_CLIENT_CONFIG \
--conf spark.yarn.appMasterEnv.YARN_CONTAINER_RUNTIME_DOCKER_MOUNTS=/etc/passwd:/etc/passwd:ro \
--num-executors 2 \
wine.py
