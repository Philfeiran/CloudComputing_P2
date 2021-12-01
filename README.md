# CloudComputing_P2

 
 For running spark job without docker on single ec2 instance with:\
 connect ec2 instance using its Public DNS:\
 ec2-3-84-42-216.compute-1.amazonaws.com\
 with phil.pem Auth Key
$ cd/spark\
$ bin/spark-submit wine.py --master local-cluster[4,1,1024]
