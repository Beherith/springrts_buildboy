import subprocess
import os
import sys
import argparse

parser = argparse.ArgumentParser(prog="make_portable_package")
parser.add_argument('-b', '--branch', choices=['maintenance', 'develop', 'transition'], required=True,
					default='maintenance')
parser.add_argument('-p', '--platform', choices=['linux', 'win'], required=True, default='win')
parser.add_argument('-a', '--architecture', choices=['32', '64'], required=True, default='64')
parser.add_argument('-v', '--version', required=True, default='latest')
args = parser.parse_args()
def runprint(description,cmd):
	print (description+':',cmd)
	result = os.system(cmd)
	if result != 0:
		raise ValueError("Failed to run command:%s"%cmd)

# TODO:
# also package debug symbols
# upload them somewhere via scp?

print ("Usage: make_portable_package.py [maintenance|develop] [releasetag] [linux|win] [32|64]")

if len(sys.argv) < 4:
	print ("Specify a release tag, platform and arch")
	exit(1)

packagebasename = 'spring_{%s}%s_%s%s-minimal-portable'

os.cwd('~/spring')

git_describe = subprocess.run('git_describe', stdout = subprocess.PIPE, shell = True)
git_versionstring = git_describe.stdout.decode().strip()
print ("Git Version String:",git_versionstring)

packagename = packagebasename%(args.branch,git_versionstring,args.platform, args.architecture)
print ("Package name: packagename")
try:
	runprint("Removing old archive if exists","rm -r -f portable")
	runprint("Creating portable folder","mkdir portable")
	if args.architecture == '64':
		runprint('Copying mingw64 .dlls','cp ./minglibs64/dll/* ./portable')
	elif args.architecture == '32':
		runprint('Copying mingw32 .dlls','cp ./minglibs/dll/* ./portable')
	runprint('Copying executables','cp ./*.exe ./portable')
	runprint('Copying socket.lua','cp ./rts/lib/luasocket/src/socket.lua ./portable/')
	runprint('Copying prdownloader','cp ./rts/lib/luasocket/src/socket.lua ./portable/')
	runprint('Copying springsettings','cp ./springsettings.cfg ./portable/springsettings.cfg')
	runprint('Copying unitsync.dll ','cp ./unitsync.dll ./portable/unitsync.dll')
	runprint('Copying luaui.lua ','cp ./cont/luaui.lua ./portable/luaui.lua')
	runprint('Copying cont/LuaUI ','cp -R ./cont/LuaUI ./portable/cont/LuaUI')
	runprint('Making empty games folder ','mkdir ./portable/games')
	runprint('Making empty maps folder ','mkdir ./portable/maps')
	runprint('Copying Fonts ','cp -R ./cont/fonts ./portable/cont/fonts')
	runprint('Copying examples ','cp -R ./cont/examples ./portable/cont/examples')
	runprint('Making docs folder ','mkdir ./portable/doc')
	runprint('Copying doc ','cp ./AUTHORS ./portable/doc/AUTHORS')
	runprint('Copying doc ','cp ./COPYING ./portable/doc/COPYING')
	runprint('Copying doc ','cp ./FAQ ./portable/doc/FAQ')
	runprint('Copying doc ','cp ./gpl-2.0.txt ./portable/doc/gpl-2.0.txt')
	runprint('Copying doc ','cp ./gpl-3.0.txt ./portable/doc/gpl-3.0.txt')
	runprint('Copying doc ','cp ./LICENSE ./portable/doc/LICENSE')
	runprint('Copying doc ','cp ./README.markdown ./portable/doc/README.markdown')
	runprint('Copying doc ','cp ./THANKS ./portable/doc/THANKS')
	runprint('Copying ctrlpanel.txt ','cp ./cont/ctrlpanel.txt ./portable/ctrlpanel.txt')
	runprint('Copying cmdcolors.txt ','cp ./cont/cmdcolors.txt ./portable/cmdcolors.txt')
	runprint('Copying base  ','cp -R ./cont/base ./portable/cont/base')
	runprint('Making C AI folder ','mkdir ./portable/AI/Interfaces/C/0.1/')
	runprint('Copying C AI interfaces','cp -R ./AI/Interfaces/C/data/ ./portable/AI/Interfaces/C/0.1/')
	runprint('Making Java AI folder ','mkdir ./portable/AI/Interfaces/Java/0.1/')
	runprint('Copying Java AI interfaces','cp -R ./AI/Interfaces/Java/AIInterface.* ./portable/AI/Interfaces/Java/0.1/AIInterface.*')
	runprint('Copying Java AI interfaces','cp -R ./AI/Interfaces/Java/data/InterfaceInfo.lua ./portable/AI/Interfaces/Java/0.1/InterfaceInfo.lua')
	runprint('Making Java AI jlib folder ','mkdir ./portable/AI/Interfaces/Java/0.1/jlib')
	runprint('Copying Java AI interfaces','cp -R ./AI/Interfaces/Java/AIInterface-src.jar ./portable/AI/Interfaces/Java/0.1/jlib/AIInterface-src.jar')
	runprint('Copying Java AI interfaces','cp -R ./AI/Interfaces/Java/data/jvm.properties ./portable/AI/Interfaces/Java/0.1/jvm.properties')

	runprint('Making NullAI folder ','mkdir ./portable/AI/Skirmish/NullAI/')
	runprint('Copying NullAI','cp -R ./AI/Skirmish/NullAI/data/* ./portable/AI/Skirmish/NullAI/')
	runprint('Making Shard folder ','mkdir ./portable/AI/Skirmish/Shard/dev/')
	runprint('Copying NullAI','cp -R ./AI/Skirmish/Shard/data/* ./portable/AI/Skirmish/Shard/dev/')
	runprint('Creating archive','7z a -r %s.7z ./portable/*'%(packagebasename))
except ValueError:
	print ("Failed to create portable!")

print ("Done!")


