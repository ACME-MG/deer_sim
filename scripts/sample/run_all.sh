#!/bin/bash

nohup python3 sample_617_s3.py 0 > out_0.log 2>&1 &
nohup python3 sample_617_s3.py 1 > out_1.log 2>&1 &
nohup python3 sample_617_s3.py 2 > out_2.log 2>&1 &
nohup python3 sample_617_s3.py 3 > out_3.log 2>&1 &
