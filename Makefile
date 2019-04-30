###### EDIT #####################
# Directory with ui and resource files, without trailing SLASH
DESIGNER_DIR = designer

# Directory for compiled resources, without trailing SLASH
COMPILED_DIR = pygaps-gui/gui

# UI files to compile, separated by SPACE
UI_FILES = mainwindow.ui
# Qt resource files to compile, separated by SPACE
QRC_FILES = resources.qrc

# Qt resource compiler binaries
PYUIC = pyside2-uic
PYRCC = pyside2-rcc

#################################
# DO NOT EDIT FOLLOWING

COMPILED_UI = $(UI_FILES:%.ui=$(COMPILED_DIR)/%.py)
COMPILED_QRC = $(QRC_FILES:%.qrc=$(COMPILED_DIR)/%_rc.py)

all : resources ui

resources : $(COMPILED_QRC)

ui : $(COMPILED_UI)

$(COMPILED_DIR)/%.py : $(DESIGNER_DIR)/%.ui
	$(PYUIC) $< -o $@ --from-imports

$(COMPILED_DIR)/%_rc.py : $(DESIGNER_DIR)/%.qrc
	$(PYRCC) $< -o $@

clean :
	$(RM) $(COMPILED_UI) $(COMPILED_QRC) $(COMPILED_UI:.py=.pyc) $(COMPILED_QRC:.py=.pyc)