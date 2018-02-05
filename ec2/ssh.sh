#!/bin/bash
cd $(cd "$(dirname "$0")" ; pwd) && cd ../ec2
ssh -i ebiz17-team14-key.pem ec2-user@ec2-54-90-105-60.compute-1.amazonaws.com
