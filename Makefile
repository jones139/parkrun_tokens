# Makefile for docker image
# I know it is old fashioned and there is probably a trendy modern way of
# doing this...but this makes it very simple for us old folks to undersatand:
# 	make build - build docker image (tokens-app)
#       make start - start running the image (it attempts to shut down and remove any existing containers first).
#       make stop - stop the running container.
#       make clean - remove the container and image.
#
# Graham Jones, December 2021

APP=tokens-app

build:
	docker build -t ${APP} .
start:
	-docker stop ${APP}
	-docker rm ${APP}   # - allows Make to continue if rm gives error because APP does not exist.
	docker run -d --restart always --name ${APP} -p 56733:80 ${APP}
stop:
	-docker stop ${APP}
shell:
	docker exec -it ${APP} bash
logs:
	docker logs ${APP}
clean:
	-docker stop ${APP}
	-docker rm ${APP}
	-docker image rm -f ${APP}
