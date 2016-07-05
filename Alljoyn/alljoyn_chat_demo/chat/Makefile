#Execute this file once the Alljoyn environment is setup.

#It replaces the older files and creates new one.

# This makefile develops binary for Linux Opearting System

ALLJOYN_DIST := ../..
#ALLJOYN_DIST := ../../../build/linux/x86/debug/dist

ALLJOYN_LIB := $(ALLJOYN_DIST)/lib/liballjoyn.a

CXXFLAGS = -Wall -pipe -std=c++98 -fno-rtti -fno-exceptions -Wno-long-long -Wno-deprecated -g -DQCC_OS_LINUX -DQCC_OS_GROUP_POSIX -DQCC_CPU_X86

LIBS = -lalljoyn -lstdc++ -lcrypto -lpthread -lrt 

.PHONY: default clean

default: chat

clean:
	rm -f chat.o chat

chat: chat.o $(ALLJOYN_LIB)
	$(CXX) -o $@ chat.o -L$(ALLJOYN_DIST)/lib $(LIBS)

chat.o: chat.cc $(ALLJOYN_LIB)
	$(CXX) -c $(CXXFLAGS) -I$(ALLJOYN_DIST)/inc -o $@ chat.cc

