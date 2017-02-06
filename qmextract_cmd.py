#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'提取qq的消息文本中: 关注的人的所有发言，如果是发言内容有：@xxx 的，则反向将xxx的话也提取出来，形成问答格式。'

__author__ = 'kevin deng'

import os
import sys
import re
import getopt
import time

import qqmsg_db
import qqmsg_item
import qmextract_ini
import global_data

# 配置文件的部分内容
important_names = ["刘明慧", "山长 清一"]
#section_wx = "wx_config"

filename_db    = "msgs.db"
error_filename = "error_msg.log"
errname_filename = "error_name.log"



# 判断是否关注人的消息，如果是，则搜索内容是否为带@的应答，如果是应答，则找回原先的问题。
# 将问题和应答存入输出文件。如果找不到应答，信息全部存入错误日志
last_time = ""

def output_important_msg(db, fout, msg):
	""" 提取重要的人的应答消息，并输出到文件 """
	global last_time
	if msg.time[0:10] > last_time:
		print("last:",last_time, "now:", msg.time[0:10])
		fout.write(msg.time[0:10] + "\n\n")

	last_time = msg.time[0:10]

	if msg.name in important_names:
		m = re.match(r'(@\d{0,4}[\+\s]?\w{2,10}[\+\s]{0,3}\w{0,6})\s(.+)', msg.content)
		if m:
			# 是含有应答对象的内容，提取出对象的姓名
			name = m.group(1).strip()[1:]

			msg_last = db.get_last_one_by_name(name)
			if msg_last:
				output_msg(fout, msg_last)
			else:
				log_errmsg_at_name(msg, name)

		output_msg(fout, msg, "\n")
		global_data.output_msg_count += 1



def output_msg(fout, msg, append=None):
	# stime = "["+ msg.time +"]"
	stime = ""
	#过滤掉表情
	content = re.sub(r'\[表情\]', "", msg.content) 
	try:
		if append:
			fout.write(stime + msg.name + "：" + content + append)
		else:
			fout.write(stime + msg.name + "：" + content)
	except:
		print("err content:", stime + msg.name + "：" + content)

def log_errmsg_at_name(msg, name):
	""" 记录姓名找不到的错误日志文件 """
	global_data.error_msg_count += 1
	with open(error_filename, 'a') as f:
		f.write(msg.name + " [" + msg.time + "] " + "error name: " + name + "\n")
		f.write(msg.content + "\n")


def log_run_time(filename):
	""" 记录运行时间到日志文件 """
	with open(filename, 'a', encoding='utf8') as f:
		prefix = " --------------- "
		f.write("\n" + prefix + global_data.runtime.strftime('%Y-%m-%d %H:%M:%S') + prefix +"\n\n")


#解析QQ消息-->DB
def parse_msg(db, fout, strlines):
	""" 从字符串列表中提取出逐条信息，格式化后，存入数据库 """

	log_run_time(error_filename)

	#读取最后一次写入的消息时间
	skip_flag = 0
	last_msg = db.get_last_one()
	if last_msg:
		skip_flag = 1
		old_time = last_msg.timestamp
		print("oldtime:", last_msg.time)

	#逐行提取消息
	pat =       re.compile(r'^\d{4}\-\d{2}\-\d{2}\s\d{1,2}:\d{1,2}:\d{1,2}\s')
	pat_group = re.compile(r'(^\d{4}\-\d{2}\-\d{2}\s\d{1,2}:\d{1,2}:\d{1,2}) (.+)')
	msg = qqmsg_item.MsgItem(errname_filename)

	for line in strlines:
		if pat.match(line):
			m = pat_group.match(line)
			# print(line)
			# print("1:",m.group(1), "2:", m.group(2))

			# 对比时间，跳过已经处理过的消息
			time_array = time.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
			now_time = int(time.mktime(time_array))

			if skip_flag==1 and old_time>now_time:
				continue

			if msg.time !="":
				output_important_msg(db, fout, msg)
				db.save_msg(msg)

			msg = qqmsg_item.MsgItem(errname_filename)
			msg.set_time(m.group(1))
			msg.set_name(m.group(2))
		else:
			str1 = line.strip()
			if len(str1)>1:
				msg.add_content(str1)

	#记录最后一条消息
	output_important_msg(db, fout, msg)
	db.save_msg(msg)



#0、打开数据库，获取最后一条信息的时间和内容，对比QQ记录，找到对应时间的下一条记录，从这里开始
#1、先按行开头的日期时间，来确定一条记录。并提取本行后面的昵称\时间，记录到自己的类，保存到数据库。
#2、如果含有：刘明慧(704664790),  山长 清一(1920602454)，则一定要记录并执行3、4
#3、搜索后续内容中是否有'\@\w+\s'，有则提取出该名字
#4、在之前记录中搜索该名字的最近一条记录，并写入在本条之前。如果没有找到，报一错误，并记录当前时间和内容
#5、如果3、4有结果，先写入4的记录，再记录本条记录。否则只记录本条记录

def qqmsg_extract(dbname, outputname, inputname):
	db = qqmsg_db.Qqmsg_db(dbname, errname_filename)
	fin = open(inputname, 'r', encoding='utf8', errors='ignore')
	fout = open(outputname, 'w')
	try:
		parse_msg(db, fout, fin.readlines())

	finally:
		if fin:
			fin.close()
		if fout:
			fout.close()

def qqmsg_init():
	""" 定位当前目录，并重新确定各配置和出错的文件路径，并读取配置文件 """
	global filename_db
	global error_filename
	global errname_filename
	path = sys.path[0]
	filename_db      = path + "/" + filename_db
	error_filename   = path + "/" + error_filename
	errname_filename = path + "/" + errname_filename

	# 读取配置文件
	global important_names
	filename_ini  = path + "/" + "qmextract.ini"
	section       = "qq_config"
	meini = qmextract_ini.Qqmsg_ini(filename_ini, section)
	important_names = meini.get_names()
	return meini

def extract_result():
	str_result = "\n ---------------------------------- \n" \
	+ "开始时间：   " + global_data.runtime.strftime('%Y-%m-%d %H:%M:%S') + "\n" \
	+ "无法识别的名字数量：    " + str(global_data.error_name_count) + "\n" \
	+ "无法找到提问的消息数量：" + str(global_data.error_msg_count) + "\n" \
	+ "提取消息数量：          " + str(global_data.output_msg_count) + "\n" 
	return str_result


def main():
	args = sys.argv
	usage = args[0] + " -i inputname -o outputname"
	if len(args)<5:
		print(usage)
		return -1

	opts, args = getopt.getopt(sys.argv[1:], "i:o:")
	input_file=""
	output_file=""

	for op, value in opts:
		if op == "-i":
			input_file = value
		elif op == "-o":
			output_file = value

	if input_file == "" or output_file == "":
		print(usage)
		return -2


	# 提取qq消息，保存并导出关注的内容
	qqmsg_init()
	global_data.init_global_data()

	qqmsg_extract(filename_db, output_file, input_file)
	#qqmsg_extract(filename_db, "./out2.txt","./清粉家园群02.txt")

	# 输出运行统计
	print(extract_result())




if __name__ == '__main__':
	main()	