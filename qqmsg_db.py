#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import alp_sqldb
import qqmsg_item



#db: id INTEGER PRIMARY KEY, name VARCHAR(20), uid VARCHAR(20), time VARCHAR(20), timestamp INTEGER, content TEXT
msg_table_item_types = "id INTEGER PRIMARY KEY, name VARCHAR(20), uid VARCHAR(20), time VARCHAR(20), timestamp INTEGER, content TEXT"
msg_table_items = "(id, name, uid, time, timestamp, content)"

class Qqmsg_db(object):
	""" QQ消息的数据库 """
	def __init__(self, dbname, msg_logname, table_name="qqmsg"):
		""" 初始化，默认消息表名为qqmsg """
		self.msg_table_name = table_name
		self.msg_logname = msg_logname

		self.db = alp_sqldb.Alp_sqldb(dbname)

		if self.db.table_is_exist(self.msg_table_name) == False:
			self.db.table_create(self.msg_table_name, msg_table_item_types)


	def get_last_one_by_condition(self, condition):
		""" 读取数据库中最后一次符合条件的消息记录，并返回对象 """
		m = self.db.find_one(self.msg_table_name, condition, "id desc")
		if m:
			msg = qqmsg_item.MsgItem(self.msg_logname)
			msg.name = m[1]
			msg.uid = m[2]
			msg.time = m[3]
			msg.timestamp = m[4]
			msg.content = m[5]
			return msg
		else:
			return None	

	def get_last_one(self):
		""" 读取数据库中最后一次消息记录并返回对象 """
		return self.get_last_one_by_condition(None)

	def get_last_one_by_name(self, name):
		""" 读取数据库中最后一次该name的消息记录并返回对象 """
		cond = "name='" + name + "'"
		return self.get_last_one_by_condition(cond)


	def save_msg(self, msg):
		""" 保存一条消息到数据库 """
		timestamp = '%d' %msg.timestamp
		sql = "INSERT INTO " + self.msg_table_name + " " + msg_table_items + " Values(NULL, " \
			   + "'" + msg.name + "', " \
			   + "'" + msg.uid  + "', " \
			   + "'" + msg.time + "', " \
			   + timestamp + ", " \
			   + "'" + msg.content + "') " 
		try:
			self.db.execute(sql)
			self.db.commit()
		except:
			print("db.execute error:", sql)

