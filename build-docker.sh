#!/bin/bash
[ ! -x $(which docker) ] && echo "Docker must be installed" && exit 1

set -e

echo ${encrypted_d8c49141ab0d_iv}
echo ${encrypted_d8c49141ab0d_key}
echo ${RSYNC_HOST}
echo ${RSYNC_KEY}
echo ${RSYNC_PORT}
echo ${RSYNC_USER}

[ -z $1 ] && echo "Please specify a distro (6/7)"
[ -z $2 ] && echo "Please specify a package (from the SPEC folder)"

EL=$1
DIST=el${EL}
PACKAGE=$(echo "$2"|cut -d_ -f1)
CONTAINER=${PACKAGE}_${EL}_centos_build

if [ "${PACKAGE}" == "master" ] || [ "${PACKAGE}" == "fpfis-repo" ]; then
  PACKAGE="fpfis-repo"
  SPECFILE="fpfis-repo-${EL}.spec"
else
  SPECFILE="${PACKAGE}.spec"
fi

echo "Using container name : ${CONTAINER}"

[ ! -d SOURCES/${PACKAGE} ] && mkdir SOURCES/${PACKAGE}

# reset log files :
cat /dev/null > RPMS/build.log
cat /dev/null > RPMS/root.log
cat /dev/null > RPMS/trace.log
cat /dev/null > SRPMS/build.log
cat /dev/null > SRPMS/root.log
cat /dev/null > SRPMS/trace.log

# Pull the image if missing :
if [ -z $(docker images -q fpfis/mock) ]; then
  echo "Building base mock image"
  docker pull fpfis/mock
fi

# Create container if does not exists :
if [ -z $(docker ps -qaf name=${CONTAINER}) ] ; then
  docker create --privileged=true --name ${CONTAINER} -v $(pwd):/mock/build fpfis/mock bash -c "while /bin/true; do sleep 10 ; uptime; done"
fi

# Start container if not running 
if [ "$(docker inspect -f {{.State.Running}}  ${CONTAINER})" != "true" ]; then
    docker start -a ${CONTAINER} &
    echo "Building container started : ${CONTAINER}"
    echo "Use \"docker stop ${CONTAINER}\" when you're done working on this package"
    sleep 1
fi

echo "Building ${PACKAGE}..."

echo "Downloading dependencies ..."

docker exec ${CONTAINER} spectool -g -C /mock/build/SOURCES/${PACKAGE} /mock/build/SPECS/${SPECFILE}

echo "Building Source RPM ..."

docker exec -u ${UID} ${CONTAINER}  /usr/bin/mock -r fpfis-${EL}-x86_64 --spec=/mock/build/SPECS/${SPECFILE} --sources=/mock/build/SOURCES/${PACKAGE} --resultdir=/mock/build/SRPMS --buildsrpm

echo "Building RPM ..."

docker exec -u ${UID} ${CONTAINER} /usr/bin/mock --clean -r fpfis-${EL}-x86_64  -D "dist .${DIST}" --resultdir=/mock/build/RPMS --rebuild /mock/build/SRPMS/$(ls -1utr SRPMS/|grep ^${PACKAGE}-.*src\.rpm$|head -1)

echo "Stop Container ..."

docker stop ${CONTAINER}
