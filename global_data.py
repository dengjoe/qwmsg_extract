#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime


# 统计数据
error_name_count = 0
error_msg_count = 0
output_msg_count = 0

#运行开始时间
runtime = datetime.datetime.now()


def init_global_data():
	global runtime
	global error_name_count
	global error_msg_count
	global output_msg_count

	error_name_count = 0
	error_msg_count = 0
	output_msg_count = 0
	runtime = datetime.datetime.now()