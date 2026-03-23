TARGET = hello_world
TITLE_ID = HELLO0001
APP_NAME = Hello World
APP_VER = 01.00

OBJS = src/main.o

VITASDK ?= /usr/local/vitasdk

CFLAGS = -Wl,-q -O2 -Wall
LIBS = -lSceDebugScreen_stub -lSceDisplay_stub -lSceGxm_stub -lSceSysmodule_stub -lSceLibKernel_stub

ICON0 = sce_sys/icon0.png
LIVEAREA = sce_sys/livearea/contents

include $(VITASDK)/share/vita/build.mk
