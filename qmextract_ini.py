#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import os


class Qqmsg_ini(object):
	""" ini 文件解析和写入 
	[qq_config]
	names = 山长 清一;刘明慧
	inputfile = ./qqmsg.txt
	outdir = d:/
	"""
	def __init__(self, filename, section):
		self.fname = filename
		self.section = section
		self.cf = configparser.ConfigParser()

		self._names = []
		self._infile = ""
		self._outdir = ""
		self._outtype= ""
		self._nickfile = ""

		if os.path.exists(self.fname) == False:
			self.__create_ini()
		else:
			self.cf.read(self.fname, encoding='utf8')
			if self.cf.has_section(self.section):
				self._names = self.cf.get(self.section, "names").split(";")
				self._names = [name.strip() for name in self._names]
				# print("important names:", self._names)

				self._infile = self.cf.get(self.section, "inputfile")
				self._outdir = self.cf.get(self.section, "outdir")
				self._outtype = self.cf.get(self.section, "outype")
				self._nickfile = self.cf.get(self.section, "nickfile")
			else:
				self.__create_ini()	


	def __create_ini(self):
		self.cf.add_section(self.section)
		self.cf.set(self.section, 'names', '') 
		self.cf.set(self.section, 'inputfile', '') 
		self.cf.set(self.section, 'outdir', '') 
		self.cf.set(self.section, 'outype', '') 
		self.cf.set(self.section, 'nickfile', '') 
		self.cf.write(open(self.fname, "w", encoding='utf8'))

		self.cf.read(self.fname, encoding='utf8')

	def get_names(self):
		return self._names

	@property
	def inputname(self):
		return self._infile

	@inputname.setter
	def inputname(self, filename):
		self.infile = filename
		self.cf.set(self.section, "inputfile", filename)
		self.cf.write(open(self.fname, "w", encoding='utf8'))

	@property
	def outputdir(self):
		return self._outdir

	@outputdir.setter
	def outputdir(self, dirname):
		self._outdir = dirname
		self.cf.set(self.section, "outdir", dirname)
		self.cf.write(open(self.fname, "w", encoding='utf8'))

	@property
	def outputype(self):
		return self._outtype

	@property
	def nickfile(self):
		return self._nickfile

	@nickfile.setter
	def nickfile(self, filename):
		self._nickfile = filename
		self.cf.set(self.section, "nickfile", filename)
		self.cf.write(open(self.fname, "w", encoding='utf8'))

def test():
	myini = Qqmsg_ini("./qmextract.ini", "wx_config")
	print(myini.get_names())

	myini.inputname="./weixin.txt"
	myini.outputdir = "d:/"
	print(myini.outputdir)
	print(myini.inputname)


if __name__=='__main__':
	test()	

