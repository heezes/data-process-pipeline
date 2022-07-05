#!/bin/bash

sudo docker run -it -e TABLE_NAME="vim_logged_data" \
-e TABLE_NAME_V2="vim_logged_data_v2" \
-e TRIP_TABLE_NAME="vim-logged-trips" \
-e DTC_TABLE_NAME="vim-logged-dtc" \
-e AWS_ACCESS_KEY_ID="AKIAQMM3NAM3ZG66EJQP" \
-e AWS_SECRET_ACCESS_KEY="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" \
-e AWS_REGION="us-east-1" \
-v /home/ftpuser1/ftp/files:/var \
altamashabdulrahim/data-process-pipeline

# docker run -it -e TABLE_NAME="vim_logged_data" -e AWS_ACCESS_KEY_ID="AKIAQMM3NAM3ZRIZQX4Y" -e AWS_SECRET_ACCESS_KEY="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" -e AWS_REGION="us-east-1" -v /home/ftpuser1/ftp/files:/var altamashabdulrahim/data-process-pipeline

#docker run -it -v E:/Python/Workdir/ci_docker:/var altamashabdulrahim/ci_docker