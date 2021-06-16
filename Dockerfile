FROM python:3.7-slim-buster
LABEL maintainer="Nakul"

ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

#setting working directory
ENV SOURCE_DIR="/app"
WORKDIR ${SOURCE_DIR}

COPY ./requirements.txt requirements.txt
# install dependencies
RUN pip install -r ./requirements.txt
ADD fixedwidthparser fixedwidthparser

# chaging the working directory
WORKDIR ${SOURCE_DIR}/fixedwidthparser

# copying the script to execute
COPY ./run.sh run.sh

# creating a user so only dataparser can run and if someone has root access cannot run the files
RUN adduser --disabled-password --gecos '' dataparser
RUN chown -R dataparser: ${SOURCE_DIR}/
USER dataparser

# defining entry point as bash and running the script on starting the container
CMD ["run.sh"]
ENTRYPOINT [ "/bin/bash" ]
