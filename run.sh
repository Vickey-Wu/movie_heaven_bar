# global var

echo "
first of all make sure you have install docker at your host, otherwise you can install follow doc:
	https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-engine---community
"

PWD=`pwd`
CONFIG_PATH=${PWD}/db_config


###### if use your own redis, comment these

# you can set your own redis passwd at ${CONFIG_PATH}/redis.conf, default passwd is 'yourpasswd'
echo "start redis contaner now ..."

REDIS_NAME='redis_movie'
docker rm -f ${REDIS_NAME}
docker run -itd --name ${REDIS_NAME} \
 -v ${CONFIG_PATH}/redis.conf:/usr/local/etc/redis/redis.conf \
 -p 8889:6379 \
 redis:latest \
 redis-server /usr/local/etc/redis/redis.conf

sleep 2
echo "redis contaner is started"


###### if use your own mysql, comment these

echo "start mysql contaner now ..."

MYSQL_NAME='mysql_movie'

docker rm -f ${MYSQL_NAME}
docker run -itd --name ${MYSQL_NAME} \
 -p 8886:3306 \
 -e MYSQL_ALLOW_EMPTY_PASSWORD=yes \
 -v ${CONFIG_PATH}/mysql.cnf:/etc/mysql/conf.d/mysql.cnf \
 -v ${CONFIG_PATH}/create_user_and_database.sql:/tmp/create_user_and_database.sql \
 mysql:8

echo 'wait for mysql start, about 15s ...'
sleep 15
docker logs ${MYSQL_NAME}

# import init data into mysql
sleep 2
docker exec -i ${MYSQL_NAME} mysql < ${CONFIG_PATH}/create_user_and_database.sql

echo 'import init data into mysql sucessfully'


###### start movie scrapy project

## start scrapy container

echo 'start scrapy container now ...'

SCRAPY_NAME='scrapy_movie'

docker rm -f ${SCRAPY_NAME}
docker run -itd --name ${SCRAPY_NAME} \
 -v ${PWD}:/home/scrapy_project \
 vickeywu/scrapy-python3

sleep 3

echo '\ncongratulations! you had inited redis and mysql sucessfully!\n'

echo "now you can run bllow cmd to go into container and start scrapy by:
	docker exec -it ${SCRAPY_NAME} /bin/bash
	sh start_scrapy.sh
and you can run bellow cmd to see scrapy log at your host by:
	docker logs -f ${SCRAPY_NAME}
"
