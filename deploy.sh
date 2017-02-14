#!/bin/bash

set +e

[ -z ${RSYNC_HOST} ] && echo "RSYNC_HOST not set, aborting" && exit 1
[ -z ${RSYNC_PORT} ] && echo "RSYNC_PORT not set, aborting" && exit 1
[ -z ${RSYNC_PATH} ] && echo "RSYNC_PATH not set, aborting" && exit 1
[ -z ${RSYNC_USER} ] && echo "RSYNC_USER not set, aborting" && exit 1
[ -z ${RSYNC_KEY}  ] && echo "RSYNC_KEY not set, aborting" && exit 1
rsync -avz -e "ssh -p ${RSYNC_PORT} -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ${RSYNC_KEY}" RPMS/ ${RSYNC_USER}@${RSYNC_HOST}:${RSYNC_PATH}
