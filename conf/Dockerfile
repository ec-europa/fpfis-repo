FROM centos
MAINTAINER Gregory Boddin

RUN yum install -y spectool mock
RUN useradd mock -g mock

ADD fpfis-*.cfg /etc/mock/

## Broken see https://github.com/docker/docker/issues/1916

#RUN su mock -c"/usr/bin/mock -r fpfis-6-x86_64 --init"
#RUN su mock -c"/usr/bin/mock -r fpfis-7-x86_64 --init"
