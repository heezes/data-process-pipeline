#!/bin/bash

sudo docker run -it -e TABLE_NAME="vim_logged_data" \
-e AWS_ACCESS_KEY_ID="AKIAQMM3NAM3ZRIZQX4Y" \
-e AWS_SECRET_ACCESS_KEY="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" \
-e AWS_REGION="us-east-1" \
-v /home/ftpuser1/ftp/files:/var \
altamashabdulrahim/data-process-pipeline

docker run -it -e TABLE_NAME="vim_logged_data" -e AWS_ACCESS_KEY_ID="AKIAQMM3NAM3ZRIZQX4Y" -e AWS_SECRET_ACCESS_KEY="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" -e AWS_REGION="us-east-1" -v /home/ftpuser1/ftp/files:/var altamashabdulrahim/data-process-pipeline

#docker run -it -v E:/Python/Workdir/ci_docker:/var altamashabdulrahim/ci_docker