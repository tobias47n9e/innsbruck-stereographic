import os, sys
from os.path import join
from subprocess import call
import nsist

localizations = ["de", "es", "fr", "it", "nl"]

for lc in localizations:
    cmd = "zanata po pull --project-id=innstereo --project-version=beta3.1 --lang={} --dstdir=po".format(lc)
    call(cmd, shell=True)

gsettings = "data/org.gtk.innstereo.gschema.xml"

if os.path.isfile(gsettings):
    call("cp data/org.gtk.innstereo.gschema.xml pynsist_pkgs64/gnome/share/glib-2.0/schemas/", shell=True)
    call("cp data/org.gtk.innstereo.gschema.xml pynsist_pkgs32/gnome/share/glib-2.0/schemas/", shell=True)
else:
    print("Copying failed")
    sys.exit()

try:
    call("glib-compile-schemas pynsist_pkgs64/gnome/share/glib-2.0/schemas/", shell=True)
    call("glib-compile-schemas pynsist_pkgs32/gnome/share/glib-2.0/schemas/", shell=True)
except:
    print("GSettings could not be compiled")
    sys.exit()

translations = "po/"

if os.path.isdir("innstereo/locale") is False:
    call("mkdir innstereo/locale", shell=True)

for root, dirs, filenames in os.walk(translations):
    for f in filenames:
        if f[-3:] == ".po":
            command = "msgfmt -o po/{0}.mo po/{0}.po".format(f[:-3])
            call(command, shell=True)

            #command = "cp po/{0}.mo pynsist_pkgs64/gnome/share/locale/{0}/LC_MESSAGES/innstereo.mo".format(f[:-3])
            #call(command, shell=True)
            #command = "cp po/{0}.mo pynsist_pkgs32/gnome/share/locale/{0}/LC_MESSAGES/innstereo.mo".format(f[:-3])
            #call(command, shell=True)

            command = "innstereo/locale/{0}".format(f[:-3])
            if os.path.isdir(command) == False:
                call("mkdir {}".format(command), shell=True)

            command = "innstereo/locale/{0}/LC_MESSAGES/".format(f[:-3])
            if os.path.isdir(command) == False:
                call("mkdir {}".format(command), shell=True)

            command = "cp po/{0}.mo innstereo/locale/{0}/LC_MESSAGES/innstereo.mo".format(f[:-3])
            call(command, shell=True)

            command = "rm po/{}.mo".format(f[:-3])
            call(command, shell=True)

appname = "InnStereo {} {}"
version = "beta3"
shortcuts = {"InnStereo beta3 64bit": {"entry_point": "innstereo:startup",
                           "extra_preamble": "gnome_preamble.py",
                           "console": False,
                           "icon": "innstereo_icon.ico"}}
icon = "innstereo_icon.ico"
project_dir = os.path.abspath(os.path.dirname(__file__))
icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), icon))
pkg_list = ["innstereo", "gi", "cairo", "dbus", "gnome", "pygtkcompat",
            "numpy", "matplotlib", "six", "dateutil", "pyparsing", "scipy",
            "mplstereonet", "cycler"]
inst_name = "InnStereo {}.exe".format(version + " {}")

installer64 = nsist.InstallerBuilder(appname.format(version, "64bit"),
                                     version,
                                     shortcuts,
                                     icon=icon_path,
                                     packages=pkg_list,
                                     extra_files=None,
                                     py_version="3.4.3",
                                     py_bitness=64,
                                     py_format="installer",
                                     build_dir="build/nsis",
                                     installer_name=inst_name.format("64bit"),
                                     nsi_template=None,
                                     exclude=None)

# FIXME check for conflicting folder before move
command = "mv {} {}".format(join(project_dir, "pynsist_pkgs64"),
                            join(project_dir, "pynsist_pkgs"))
call(command, shell=True)
installer64.run()
command = "mv {} {}".format(join(project_dir, "pynsist_pkgs"),
                            join(project_dir, "pynsist_pkgs64"))
call(command, shell=True)

shortcuts = {"InnStereo beta3 32bit": {"entry_point": "innstereo:startup",
                           "extra_preamble": "gnome_preamble.py",
                           "console": False,
                           "icon": "innstereo_icon.ico"}}
installer32 = nsist.InstallerBuilder(appname.format(version, "32bit"),
                                     version,
                                     shortcuts,
                                     icon=icon_path,
                                     packages=pkg_list,
                                     extra_files=None,
                                     py_version="3.4.3",
                                     py_bitness=32,
                                     py_format="installer",
                                     build_dir="build/nsis",
                                     installer_name=inst_name.format("32bit"),
                                     nsi_template=None,
                                     exclude=None)
command = "mv {} {}".format(join(project_dir, "pynsist_pkgs32"),
                            join(project_dir, "pynsist_pkgs"))
call(command, shell=True)
installer32.run()
command = "mv {} {}".format(join(project_dir, "pynsist_pkgs"),
                            join(project_dir, "pynsist_pkgs32"))
call(command, shell=True)
