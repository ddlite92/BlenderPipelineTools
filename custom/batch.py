import os
import sys
import subprocess
import time
import datetime

# B = {}
def modification_date_time(file_name):
    time = os.path.getmtime(file_name)
    return datetime.datetime.fromtimestamp(time)


"""Configure blend files"""
blendfiles = []
for current_dir, _, files in os.walk("."):
    for f in sorted(files):
        if (
            not f.endswith(".blend1")
            and not ".2021" in f
            and not ".2022" in f
            #and "SH016" in f
#            and not "SH002" in f
#            and not "SH003" in f
#            and not "SH004" in f
#            and not "SH005" in f
#            and not "SH006" in f
#            and not "SH007" in f
#            and not "SH008" in f
#            and not "SH009" in f
            and f.endswith(".blend")
        ):
            f_relpath = os.path.join(current_dir, f)
            f_abspath = os.path.abspath(f_relpath)
            blendfiles.append(f_abspath)

print("------------")
"""Script for running"""
for blendfile in sorted(blendfiles):
    # for blendfile in sorted(blendfiles, key=lambda t: os.stat(t).st_mtime):
    # blendfile = os.path.abspath(file)
    # modified_time = os.path.getmtime(blendfile)
    # convert_time = time.ctime(modified_time)
    if sys.platform.startswith("win32"):
        # command = (
        #     'C:\\blender\\blender.exe -b "%s"' % blendfile + " -y -P command.py"
        # )
        command2 = (
            'C:\\blender\\blender.exe -b "%s"' % blendfile + " -y -P transmission_ray.py"
        )
        # if 'Apr 24' in convert_time:
        # print(command)
        # print (blendfile + " | " + blendfile[-15:] + " | " + convert_time)
        # subprocess.run(r'C:\WINDOWS\system32\cmd.exe /C "%s"' % command)
        subprocess.run(r'C:\WINDOWS\system32\cmd.exe /C "%s"' % command2)
    elif sys.platform.startswith("linux"):
        command = (
            '/opt/cgru/software_setup/start_blender.sh -b "%s"' % blendfile
            + " -y -P settings.py "
        )
        subprocess.run(command, shell=True)
        # print(command)
