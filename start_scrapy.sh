# go to project dir
#PROJECT_DIR=`pwd`
#cd ${PROJECT_DIR}

# run scrapy crawl spidername command
echo "

# your can run scrapy at backgroup by bellow cmd:

	scrapy crawl newest_movie &

# you can see log at container dir: /var/log/scrapy.log

or at your host by run cmd: docker logs -f --tail 50 your_container_name

# you can stop scrapy by press Ctrl+C two times, 
if run backgroup you can stop scrapy by kill scrapy pid
"

echo 'scrapy is running now...'

scrapy crawl newest_movie

