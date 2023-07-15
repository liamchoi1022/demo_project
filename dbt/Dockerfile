# Download base image ubuntu 22.04
FROM ubuntu:20.04

# Update Ubuntu Software repository
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt-get update
RUN apt-get upgrade
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get install -y tzdata
RUN apt install python3.9-distutils -y
RUN apt install python3-pip -y
RUN apt install python3.9 -y
RUN apt install git -y
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
RUN pip install dbt-postgres

RUN apt install openssh-server sudo -y

RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 airflow 
RUN echo 'airflow:airflow' | chpasswd
RUN service ssh start

EXPOSE 8080 22

RUN rm -rf /var/lib/apt/lists/*
RUN apt clean

CMD ["/usr/sbin/sshd","-D"]


#RUN mkdir -p /dbt/dbt
#RUN chown -R www-data:www-data /var/www/html
#RUN chown -R www-data:www-data /run/dbt

# Expose Port for the Application 
