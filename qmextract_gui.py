#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.filedialog as filedialog
import sys
import datetime

import global_data
import qmextract_ini
import qmextract_cmd


class WinInput(object):
	""" 输入文件名和目录，并执行的主Frame """
	def __init__(self, master, meini):
		self.master = master
		frame = tk.Frame(master, height = 200,width = 400)
		frame.pack()				# 只有pack的组件实例才能显示

		self.ini = meini
		self.qqfin = meini.inputname
		self.qqdout = meini.outputdir

		tk.Label(frame, text="QQ聊天记录:").grid(row=0, sticky='w')
		tk.Label(frame, text="导出目录:").grid(row=1, sticky='w')

		default_v1 = tk.StringVar()
		default_v1.set(self.qqfin)
		self.fin = tk.Entry(frame, width=50, textvariable = default_v1)
		self.fin.grid(row=0, column=1)
		fbtn = tk.Button(frame, text='...', command=self.find_infile)
		fbtn.grid(row=0, column=2)

		default_v2 = tk.StringVar()
		default_v2.set(self.qqdout)
		self.dout = tk.Entry(frame, width=50, textvariable = default_v2)
		self.dout.grid(row=1, column=1)
		dbtn = tk.Button(frame, text='...', command=self.find_outdir)
		dbtn.grid(row=1, column=2)

		dbtn = tk.Button(frame, text='QQ提取', command=self.run_qmex)
		dbtn.grid(row=2, columnspan=2)

		self.txt = tk.Text(frame, width=65)
		self.txt.grid(row=3, column=0, columnspan=3, sticky='w') 


	def find_infile(self):
		 # define options for opening or saving a file
		self.file_opt = options = {}
		options['defaultextension'] = '.txt'
		options['filetypes'] = [('text files', '.txt'), ('all files', '.*')]
		options['initialdir'] = 'C:\\'
		options['initialfile'] = '*.txt'
		options['parent'] = root  # self.master 一样
		options['title'] = '选择文件'
		self.qqfin = filedialog.askopenfilename(**self.file_opt)   
		# 显示，保存
		self.fin.delete(0, "end")
		self.fin.insert(0, self.qqfin)
		self.ini.inputname = self.qqfin


	def find_outdir(self):
		self.qqdout = filedialog.askdirectory()
		# 显示，保存
		self.dout.delete(0, "end")
		self.dout.insert(0, self.qqdout)
		self.ini.outputdir = self.qqdout


	def run_qmex(self):
		global_data.init_global_data()
		# 根据dout生成输出文件名fout，再运行提取。
		foutname = self.qqdout + "\\" + global_data.runtime.strftime('%Y-%m%d_%H%M%S') + ".txt"

		qmextract_cmd.qqmsg_extract(qmextract_cmd.filename_db, foutname, self.qqfin)
		self.txt.insert(0.0, qmextract_cmd.extract_result())


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