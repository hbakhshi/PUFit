SRC_DIR :=src
OBJ_DIR :=lib/objs
SRC_FILES := $(wildcard $(SRC_DIR)/*.cxx)
OBJ_FILES := $(patsubst $(SRC_DIR)/%.cxx,$(OBJ_DIR)/%.o,$(SRC_FILES))
HEADER_FILES := $(patsubst $(SRC_DIR)/%.cxx,%.h,$(SRC_FILES))
HEADER_FILES_INDIR := $(patsubst $(SRC_DIR)/%.cxx,include/%.h,$(SRC_FILES))
LDFLAGS := $(shell root-config --libs) -lRooFitCore -lRooFit -lRooFitMore -fPIC -shared 
CPPFLAGS := -I$(shell root-config --incdir) -I./include/
CXXFLAGS := -fPIC -std=c++17
#-DDEBUGL=7

all: $(OBJ_DIR) lib/libPUFit.so lib/DEFS_rdict.pcm

lib/libPUFit.so: $(OBJ_FILES) $(OBJ_DIR)/DEFS.o
	g++ $(LDFLAGS) -o $@ $^

lib/DEFS_rdict.pcm: $(OBJ_DIR)/DEFS_rdict.pcm
	ln -s $(shell pwd)/$^ $@

$(OBJ_DIR)/DEFS.o: $(OBJ_DIR)/DEFS.cxx
	g++ $(CPPFLAGS) $(CXXFLAGS) -c -o $@ $<

$(OBJ_DIR)/DEFS_rdict.pcm: $(OBJ_DIR)/DEFS.cxx

$(OBJ_DIR)/DEFS.cxx: $(SRC_DIR)/LinkDef.h
	cd include && rootcling -f ../$@ -c $(HEADER_FILES) ../$<

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cxx include/%.h include/Common.h
	g++ $(CPPFLAGS) $(CXXFLAGS) -c -o $@ $<

$(OBJ_DIR):
	mkdir -p $@

clean:
	rm -f lib/objs/*
	rm -rf lib/*

