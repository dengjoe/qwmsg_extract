#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' MsgItem消息对象, 用于保存QQ、微信消息 '

__author__ = 'kevin deng'


import re
import os
import time
import global_data

class MsgItem(object):
	""" 提取qq消息记录的信息：
		name=昵称，不含括号中的qq号或邮箱
		uid=QQ号或邮箱，
		time=发言时间的字符串， timestamp=time转换的时间戳，
		content=多行的信息内容  
	"""
	def __init__(self, logname):
		self.name = ""
		self.uid  = ""
		self.time = ""
		self.timestamp = 0
		self.content = ""
		self.logname = logname

	def set_name(self, name):
		"""分解name，匹配：昵称和QQ号(或邮箱)"""
		m = re.match(r'([\d\w\+\s\!\-\~\@]{0,20})[\(\<]([\w\d\~\.\@\-]+[\>\)]$)', name)
		# m = re.match(r'(\d{0,4}[\+\s\!\-]{0,2}\w{1,10}[\+\s\@\-]{0,3}\w{0,6}[\+\s\@]{0,3}[\w\d]{0,3})[\(\<](.+)', name)
		if m:
			self.name = m.group(1).strip()
			self.uid = m.group(2).rstrip(')').rstrip('>')
		else:
			#print(name) #可能会出错
			log_err_line(self.logname, name)
			# localstring = name.encode('gbk','ignore') #可以，但是乱码
			# print(localstring)

	def set_time(self, ti):
		"""设置时间，并转换字符串为时间戳"""
		self.time = ti
		timeArray = time.strptime(ti, "%Y-%m-%d %H:%M:%S")
		self.timestamp = int(time.mktime(timeArray))
		# print(ti, " :", timeArray, ":", self.timestamp)

	def add_content(self, msg):
		"""换行，并过滤掉表情字符串"""
		if self.content != "":
			self.content += "\n"
		self.content += re.sub(r'\[表情\]', "", msg)

	def output_std(self):
		print("%s %s \t %s(%d):\n %s" % (self.name, self.uid, self.time, self.timestamp, self.content))



def log_err_line(logname, strline):
	""" 记录一条信息到日志文件 """
	global_data.error_name_count += 1
	with open(logname, 'a', encoding='utf8') as f:
		f.write(strline + "\n")


#解析QQ消息
def parse_msg(strlines):
	""" 从字符串列表中提取出逐条信息，格式化后，放入MsgItem的列表中返回 """
	pat =       re.compile(r'^\d{4}\-\d{2}\-\d{2}\s\d{2}:\d{2}:\d{2}\s')
	pat_group = re.compile(r'(^\d{4}\-\d{2}\-\d{2}\s\d{2}:\d{2}:\d{2}) (.+)')
	msgs = []
	msg = MsgItem()

	num = len(strlines)
	i = 0
	ii = 0
	for line in strlines:
		if pat.match(line):
			m = pat_group.match(line)
			#print(line)
			#print(m.group(1))
			#print(m.group(2))

			if ii>0:
				msgs.append(msg)

			msg = MsgItem()
			ii += 1
			msg.set_time(m.group(1))
			msg.set_name(m.group(2))
		else:
			str1 = line.strip()
			if len(str1)>1:
				msg.add_content(str1)

		i += 1
		if i==num:
			msgs.append(msg)

	return msgs


def msgitem_get_at_name(msg, names):
	""" 查找names中的人的msg，并查找其信息中的@xxx的字符，如果有，则提取出来其姓名，返回姓名。 """
	if msg.name in names:
		m = re.match(r'(@\d{0,4}[\+\s]?\w{2,10}[\+\s]{0,3}\w{0,6})\s(.+)', msg.content)
		if m:
			#print(m.groups())
			return m.group(1).strip()[1:]


#============= unit test ============

def test_parse_msg():
	str1 = ["2016-12-29 22:04:01 0614张新 广州(22478530)","全身暖暖的，但我家先生感觉到了凉风","全身非常热，感觉很殊胜。","2016-12-29 22:04:42 刘明慧(704664790)","@0614张新 广州 病气出去了。","2016-12-29 22:04:28 0438蔡丽君上海<cailvshi@sohu.com>","   感谢刘老师。期间全身有能量流动感觉。   左脚有排气感，全身轻松。"]

	print("\ntest_parse_msg --------------")
	msgs = parse_msg(str1)
	for m in msgs:
		m.output_std()


def test_parse_qqinfo(filename):
	print("\ntest_parse_qqinfo --------------")
	pf = open(filename, 'r')

	msgs = parse_msg(pf.readlines())
	names = ("刘明慧", "山长 清一")

	for msg in msgs:
		#msg.print()
		m = msgitem_get_at_name(msg, names)
		if m:
			print(m)
			file_write_msg(msg)
		

def test_file_readlines():
	pf = open("./qqtest.txt", 'r')
	print(len(pf.readlines()))

	for line in pf.readlines():
		print(line.strip())

def file_write_msg(msg):
	""" 记录姓名找不到的错误日志文件 """
	with open("./output.log", 'a') as f:
		f.write(msg.name + " [" + msg.time + "] " + "\n")
		f.write(msg.content + "\n")

if __name__ == '__main__':
	# test_file_readlines()
	test_parse_msg()
	test_parse_qqinfo("./qqtest.txt")				