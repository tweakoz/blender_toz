#!/usr/bin/python

import sys
import os

argc = len(sys.argv)

print "argc<%d>" % argc

def spawn(cmd):
  print "execute command<%s>" % cmd
  os.system(cmd)

###########################

def check():
  if False==os.path.exists("git"):
    print "no git folder found ! (should be sibling to the build folder)"
    sys.exit(-1) 
  if False==os.path.exists("build"):
    print "no build folder found ! (should be sibling to the git folder)"
    sys.exit(-1)

############################

def init_common():
  os.chdir("git")
  spawn("git submodule update --init --recursive")
  spawn("git submodule foreach git checkout master")
  spawn("git submodule foreach git pull --rebase origin master")
  os.chdir("..")
  spawn("git clone git://gitorious.org/blenderprojects/extensions.git" ) # 18fb9c67efb5846a4ba06043a05a885ba03b8f3e
  spawn("cp -r extensions/trunk/py/scripts/addons git/release/scripts/addons")
  spawn("cp -r extensions/contrib/py/scripts/addons git/release/scripts/addons_contrib")
  #spawn("cp -r tozext/render_3delight git/release/scripts/addons/")
  spawn("mkdir lib")

##############################

def init_osx():
  #cmd = "cp git/build_files/scons/config/darwin-config.py blender/user-config.py"
  cmd = "cp git/toz/working-osx-config.py git/user-config.py"
  spawn(cmd)	
  os.chdir("lib")
  spawn( "svn co https://svn.blender.org/svnroot/bf-blender/trunk/lib/darwin-9.x.universal" )
  os.chdir("..")

#############################

def init():
  init_common()
  init_osx()

#############################

def make():
 os.chdir("git")
 spawn( "python scons/scons.py -j 4" )

##############################

def clean():
 spawn( "rm -rf ./build" )
 os.chdir("git")
 spawn( "python scons/scons.py clean" )

###########################

check()

if argc == 2:
  print "exec <%s>" % sys.argv[1]
  cmd = sys.argv[1]
  if cmd=="init":
    init()
  elif cmd=="make":
    make()
  elif cmd=="clean":
    clean()

else:
  print "usage do.py target where target is one of:"
  print "  init - one time init of working copy"
  print "  make - build it"
