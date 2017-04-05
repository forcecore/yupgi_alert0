ENGINEDIR    ?= ../../engine
MODNAME      = yupgi_alert
MODDIRNAME   = OpenRA.Mods.$(MODNAME)
DLLNAME      = $(MODDIRNAME).dll
DEPENDENCIES = $(ENGINEDIR)/mods/common/OpenRA.Mods.Common.dll $(ENGINEDIR)/mods/common/OpenRA.Mods.Cnc.dll ../as/OpenRA.Mods.AS.dll

############################## TOOLCHAIN ###############################
#
SDK         ?=
CSC         = mcs $(SDK)
CSFLAGS     = -nologo -warn:4 -codepage:utf8 -unsafe -warnaserror
DEFINE      = TRACE
COMMON_LIBS = System.dll System.Core.dll System.Data.dll System.Data.DataSetExtensions.dll System.Drawing.dll System.Xml.dll $(ENGINEDIR)/thirdparty/download/ICSharpCode.SharpZipLib.dll $(ENGINEDIR)/thirdparty/download/FuzzyLogicLibrary.dll $(ENGINEDIR)/thirdparty/download/MaxMind.Db.dll $(ENGINEDIR)/thirdparty/download/Eluant.dll $(ENGINEDIR)/thirdparty/download/SmarIrc4net.dll
STD_MOD_LIBS=  $(ENGINEDIR)/OpenRA.Game.exe
NUNIT_LIBS_PATH :=
NUNIT_LIBS  := $(NUNIT_LIBS_PATH)nunit.framework.dll

DEBUG = true
ifeq ($(DEBUG), $(filter $(DEBUG),false no n off 0))
CSFLAGS   += -debug:pdbonly -optimize+
else
CSFLAGS   += -debug:full -optimize-
DEFINE    := DEBUG;$(DEFINE)
endif



######################### UTILITIES/SETTINGS ###########################
#
# install locations
prefix ?= /usr/local
datarootdir ?= $(prefix)/share
datadir ?= $(datarootdir)
mandir ?= $(datarootdir)/man/
bindir ?= $(prefix)/bin
libdir ?= $(prefix)/lib
gameinstalldir ?= $(libdir)/openra

BIN_INSTALL_DIR = $(DESTDIR)$(bindir)
DATA_INSTALL_DIR = $(DESTDIR)$(gameinstalldir)

# install tools
RM = rm
RM_R = $(RM) -r
RM_F = $(RM) -f
RM_RF = $(RM) -rf
CP = cp
CP_R = $(CP) -r
INSTALL = install
INSTALL_DIR = $(INSTALL) -d
INSTALL_PROGRAM = $(INSTALL) -m755
INSTALL_DATA = $(INSTALL) -m644

# program targets
CORE = pdefault game utility server
TOOLS = gamemonitor
VERSION     = $(shell git name-rev --name-only --tags --no-undefined HEAD 2>/dev/null || echo git-`git rev-parse --short HEAD`)

# dependencies
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
os-dependencies = osx-dependencies
else
os-dependencies = linux-dependencies
endif



######################## PROGRAM TARGET RULES ##########################
#
# Mod
mod_LIBS = $(COMMON_LIBS) $(STD_MOD_LIBS) $(DEPENDENCIES)
mod: $(DLLNAME)
$(DLLNAME): $(shell find $(MODDIR) -iname '*.cs')
	@echo CSC $@
	@$(CSC) $(mod_LIBS:%=-r:%) \
		-out:$(@) $(CSFLAGS) \
		-define:"$(DEFINE)" \
		-t:library \
		$^
	@chmod a-x $@

check-scripts:
	@echo

check:
	@echo
	@echo "Checking for code style violations in the mod..."
	@mono --debug $(ENGINEDIR)/OpenRA.Utility.exe $(shell echo `pwd`) --check-code-style $(MODDIRNAME) 

test:
	@echo
	@echo "Testing mod's MiniYAML..."
	@mono --debug $(ENGINEDIR)/OpenRA.Utility.exe $(shell echo `pwd`) --check-yaml

########################## MAKE/INSTALL RULES ##########################
#
default: core

core: dependencies game platforms mods utility server

all: mod check-scripts check test 

clean:
	@-$(RM_F) *.exe *.dll *.dylib *.dll.config ./OpenRA*/*.dll ./OpenRA*/*.mdb *.mdb mods/**/*.dll mods/**/*.mdb *.resources
	@-$(RM_RF) ./*/bin ./*/obj
	@-$(RM_F) StyleCopViolations.xml

help:
	@echo 'to compile, run:'
	@echo '  make [DEBUG=false]'
	@echo
	@echo 'to compile with development tools, run:'
	@echo '  make all [DEBUG=false]'
	@echo
	@echo 'to check the official mods for erroneous yaml files, run:'
	@echo '  make test'

########################### MAKEFILE SETTINGS ##########################
#
.DEFAULT_GOAL := default

.SUFFIXES:

.PHONY: core all mod check-scripts check test clean
