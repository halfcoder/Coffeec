# coding=utf-8
# Coffeescript compiler for Sublime Text 2 in windows
# http://github.com/halfcoder/coffeec
# Licensed under the WTFPL

import os, sys, re, subprocess, functools, sublime, sublime_plugin

package_name = 'coffeec'

#print sys.getdefaultencoding()
#vars()

def coffeec(fileroot):
	execmd = '@cscript //nologo "'+sublime.packages_path()+'\\'+package_name+'\\coffeec.wsf"'+' "'+fileroot+'.coffee"'+' "'+fileroot+'.js"'

	execmd = execmd.encode("gbk") #先将编码转换到gbk

	res = subprocess.Popen(execmd,stdin = subprocess.PIPE,stdout=subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
	res.wait()

	error = res.stderr.read()
	print error.decode("gbk")  #解码gbk
	
	remsg = '';
	if error=='':
		remsg = 'compiled:'+fileroot+'.js'
		print remsg
	else:
		errorinfo = error.split("\r\n")
		remsg = errorinfo[2]+"    "+errorinfo[6]+""

	sublime.set_timeout(functools.partial(status,remsg),1200);
	sublime.set_timeout(functools.partial(reloadJs,fileroot),400);


#状态栏消息
def status(msg):
	sublime.status_message(msg)

#重新读取js文件
def reloadJs(fileroot):
	for win in sublime.windows():
		for view in win.views():
			if(view.file_name()==fileroot+".js"):
				view.run_command("reopen",{"encoding": "utf-8" })

class EventListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		filepath = view.file_name()
		(fileroot, fileext) = os.path.splitext(filepath)
		if(fileext=='.coffee'):
			coffeec(fileroot)


