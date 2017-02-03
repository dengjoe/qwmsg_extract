#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sqlite3


class Alp_sqldb(object):
	""" 数据库接口简化类 """

	def __init__(self, db_name):
		self.conn = sqlite3.connect(db_name)
		self.cur  = self.conn.cursor()

	def __del__(self):
		self.cur.close()
		self.conn.close()


	def table_is_exist(self, table):
		sql = "SELECT COUNT(*) FROM sqlite_master where type='table' and name='" + table + "'"
		ret = self.cur.execute(sql)
		return ret.fetchall()[0][0] == 1

	def table_drop(self, table):
		sql = "DROP TABLE IF EXISTS " + table
		self.cur.execute(sql)
		self.conn.commit()

	def table_create(self, table, titles):
		sql = "CREATE TABLE " + table + " (" + titles + ")"
		#print(sql)
		self.cur.execute(sql)
		self.conn.commit()

	def execute(self, sql):
		self.cur.execute(sql)

	def commit(self):
		self.conn.commit()

	def rollback(self):
		self.conn.rollback()

	def __execute_find(self, table, condition=None, order=None):
		if condition==None:
			sz_cond = ""
		else:
			sz_cond = " where " + condition

		if order==None:
			sz_order = ""
		else:
			sz_order = " order by " + order			

		sql = "SELECT * FROM " + table + sz_cond + sz_order
		# print(sql)
		self.cur.execute(sql)		

	def find_all(self, table, condition=None, order=None):
		self.__execute_find(table, condition, order)
		return self.cur.fetchall()

	def find_one(self, table, condition=None, order=None):
		self.__execute_find(table, condition, order)
		return self.cur.fetchone()


	def update(self, table, sets, condition):
		sql = "update " + table + " set " + sets + " where " + condition
		# print(sql)
		self.cur.execute(sql)
		self.conn.commit()		

	def delete(self, table, condition):
		sql = "delete from " + table + " where " + condition
		#print(sql)
		self.cur.execute(sql)
		self.conn.commit()




def sql_unit_test():
	db = Alp_sqldb("./test.db")

	tablename = "fellows"
	if db.table_is_exist(tablename):
		db.table_drop(tablename)

	db.table_create(tablename, "id INTEGER PRIMARY KEY, name VARCHAR(20), score INTEGER")

	db.execute('INSERT INTO fellows (id, name, score) VALUES(NULL, "apple", 123)')
	db.execute('INSERT INTO fellows (id, name, score) VALUES(NULL, "orange", 456)')
	db.execute('INSERT INTO fellows (id, name, score) VALUES(NULL, "yelp", 789)')
	db.execute('INSERT INTO fellows (id, name, score) VALUES(NULL, "orange", 406)')
	db.commit()

	print(db.find_all(tablename))
	print(db.find_all(tablename, None, "id desc"))
	print(db.find_all(tablename, "name='range'"))
	print(db.find_all(tablename, "name='orange'"))
	print(db.find_all(tablename, "name='orange'", "id desc")) #反向查找
	print(db.find_one(tablename, "name='orange'", "id desc")) #反向查找

	db.update(tablename, "score=1010", "name='yelp'")
	print(db.find_all(tablename))

	db.delete(tablename, "score=456")
	print(db.find_all(tablename))


if __name__ == '__main__':
	sql_unit_test()	