#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.filedialog as filedialog
import sys
import datetime
import re

import global_data
import qmextract_ini
import qmextract_cmd


class WinInput(object):
	""" 输入文件名和目录，并执行的主Frame """
	def __init__(self, master, meini):
		self.master = master
		frame = tk.Frame(master, height = 200,width = 400)
		frame.pack()				# 只有pack的组件实例才能显示

		self._ini = meini
		self._qqfin = meini.inputname
		self._qqout = meini.outputdir
		self._nickfile = meini.nickfile

		tk.Label(frame, text="QQ聊天记录:").grid(row=0, sticky='w')
		tk.Label(frame, text="导出目录:").grid(row=1, sticky='w')
		tk.Label(frame, text="昵称对照:").grid(row=2, sticky='w')

		default_v1 = tk.StringVar()
		default_v1.set(self._qqfin)
		self.fin = tk.Entry(frame, width=50, textvariable = default_v1)
		self.fin.grid(row=0, column=1)
		fbtn = tk.Button(frame, text='...', command=self.find_infile)
		fbtn.grid(row=0, column=2)

		default_v2 = tk.StringVar()
		default_v2.set(self._qqout)
		self.dout = tk.Entry(frame, width=50, textvariable = default_v2)
		self.dout.grid(row=1, column=1)
		dbtn = tk.Button(frame, text='...', command=self.find_outdir)
		dbtn.grid(row=1, column=2)

		default_v3 = tk.StringVar()
		default_v3.set(self._nickfile)
		self.nickin = tk.Entry(frame, width=50, textvariable = default_v3)
		self.nickin.grid(row=2, column=1)
		dbtn = tk.Button(frame, text='...', command=self.find_nickfile)
		dbtn.grid(row=2, column=2)

		dbtn = tk.Button(frame, text='昵称清空', command=self.clear_nick)
		dbtn.grid(row=3, column=0, sticky="W"+"E")

		dbtn = tk.Button(frame, text='QQ提取', command=self.run_qmex)
		dbtn.grid(row=3, column=1, sticky="W"+"E")

		dbtn = tk.Button(frame, text='昵称载入', command=self.run_nick)
		dbtn.grid(row=3, column=1, sticky="W")

		self.txt = tk.Text(frame, width=65)
		self.txt.grid(row=4, column=0, columnspan=3, sticky='w') 


	def find_infile(self):
		 # define options for opening or saving a file
		self.file_opt = options = {}
		options['defaultextension'] = '.txt'
		options['filetypes'] = [('text files', '.txt'), ('all files', '.*')]
		options['initialdir'] = 'C:\\'
		options['initialfile'] = '*.txt'
		options['parent'] = root  # self.master 一样
		options['title'] = '选择文件'
		self._qqfin = filedialog.askopenfilename(**self.file_opt)   
		# 显示，保存
		self.fin.delete(0, "end")
		self.fin.insert(0, self._qqfin)
		self._ini.inputname = self._qqfin


	def find_outdir(self):
		self._qqout = filedialog.askdirectory()
		# 显示，保存
		self.dout.delete(0, "end")
		self.dout.insert(0, self._qqout)
		self._ini.outputdir = self._qqout

	def find_nickfile(self):
		self.file_opt = options = {}
		options['defaultextension'] = '.txt'
		options['filetypes'] = [('text files', '.txt'), ('all files', '.*')]
		options['initialdir'] = 'C:\\'
		options['initialfile'] = '*.txt'
		options['parent'] = root  # self.master 一样
		options['title'] = '选择文件'
		self._nickfile = filedialog.askopenfilename(**self.file_opt)   
		# 显示，保存
		self.nickin.delete(0, "end")
		self.nickin.insert(0, self._nickfile)
		self._ini.nickfile = self._nickfile


	def run_qmex(self):
		global_data.init_global_data()
		# 根据dout生成输出文件名fout，再运行提取。
		foutname = self._qqout + "\\" + global_data.runtime.strftime('%Y-%m%d_%H%M%S') + self._ini.outputype
		print(foutname)

		qmextract_cmd.qqmsg_extract(qmextract_cmd.filename_db, foutname, self._qqfin)
		self.txt.insert(0.0, qmextract_cmd.extract_result())

	def run_nick(self):
		qmextract_cmd.qqmsg_save_nicknames(qmextract_cmd.filename_db, self._nickfile)

	def clear_nick(self):
		qmextract_cmd.qqmsg_clear_nicknames(qmextract_cmd.filename_db)


root = tk.Tk()

def main_win():
	ini = qmextract_cmd.qqmsg_init()

	global root
	root.title('群消息提取器')    #定义窗体标题
	# root.geometry('400x200')     #定义窗体的大小，是400X200像素
	app = WinInput(root, ini)
	root.mainloop()


if __name__=='__main__':
	main_win()