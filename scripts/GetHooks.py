#!/usr/bin/env python
'''\
	Hook Documentation Compiler
		By N3X15

	(GPL2 here)
'''

import types
import re

## {{{ http://code.activestate.com/recipes/499305/ (r3)
import os, fnmatch

def locate(pattern, root=os.curdir):
	'''Locate all files matching supplied filename pattern in and below
	supplied root directory.'''
	for path, dirs, files in os.walk(os.path.abspath(root)):
		for filename in fnmatch.filter(files, pattern):
			yield os.path.join(path, filename)
## end of http://code.activestate.com/recipes/499305/ }}}


Hooks=dict({})
HookWiki="""
== Documented Hooks ==

The following are hooks that have been documented in Luna (latest pull).

{| class="awesometable"
|-
! Name ! Arguments ! File ! Description
"""

HookDocs="""\
-- AUTOMATICALLY GENERATED BY scripts/GetHooks.py! DO NOT MODIFY! --

"""
HookPattern=re.compile("@hook (\S+)\((.*)\) (.*)")

def ParseFile(fname):
	if fname == '': 
		return
	f = open(fname,"r")
	i=0
	for line in f:
		i+=1
		# @hook ExampleHook(a,b,c) lol description
		m = HookPattern.search(line)
		if m is not None:
			hookname = m.group(1)
			hookargs = m.group(2)
			hookdesc = m.group(3)
			if hookname:
				if not hookname in Hooks:
					#hookfile= "indra/newview/%s:%d" % (fname.replace(os.path.abspath(os.curdir),""),i)
					hookfile= "indra/newview/%s:%d" % (os.path.relpath(fname),i)
					Hooks[hookname]=( hookargs,hookfile,hookdesc )
					print "[HOOK]\t%s\t%s" % (hookname,hookdesc)
	f.close() 

print "Searching for hooks (WILL take a while)...\n"

for v in locate("*.cpp"):
	ParseFile(v)
	
#Hooks=sorted(Hooks)

for k,v in Hooks.iteritems():
	(args,file,desc) = v
	HookWiki += "|-\n! [[%s]]\n| %s\n| %s\n| %s\n" % (k, args, file, desc)
	HookDocs += "\n-- defined in %s\nRegisterHook(\"%s\", \"%s\")\n" % (file,k,desc.strip())

HookWiki += """
|-
|}

"""

f = open("lua/HookDocs.wiki","w")
f.write(HookWiki)
f.close()

f = open("lua/HookDocs.lua","w")
f.write(HookDocs)
f.close()
