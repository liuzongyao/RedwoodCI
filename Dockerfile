FROM ubuntu:16.04
MAINTAINER Liuzongyao <zyliu@alauda.io>
RUN rm -rf /var/lib/apt/lists/*
RUN apt-get update
RUN apt-get install net-tools -y
RUN apt-get install wget -y
RUN apt-get install libssl1.0.0 libssl-dev -y
RUN apt-get install vim -y
RUN apt-get install python -y
RUN apt-get install python-pip -y
RUN apt-get install git -y
RUN apt-get install python-psycopg2 -y
RUN pip install virtualenv
RUN pip install requests
RUN pip install selenium
RUN pip install dpath
RUN wget -qO- https://deb.nodesource.com/setup_4.x | bash -
RUN apt-get install nodejs -y
COPY RedwoodHQ /RedwoodHQ
COPY automationscripts /automationscripts
WORKDIR /RedwoodHQ
ADD Start.sh  /RedwoodHQ
EXPOSE 3000
CMD ["/bin/bash","Start.sh"]
