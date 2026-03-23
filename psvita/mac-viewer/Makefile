TARGET = bt_mac_viewer
TITLE_ID = BTMAC0001
APP_NAME = BT MAC Viewer

OBJS = src/main.o

CFLAGS = -O2 -Wall
LDFLAGS =

LIBS = -lSceDisplay_stub -lSceCtrl_stub -lSceKernelThreadMgr_stub -lm

all: $(TARGET).vpk

%.vpk: %.elf
	vita-mksfoex -s TITLE_ID=$(TITLE_ID) "$(APP_NAME)" param.sfo
	vita-pack-vpk -s param.sfo -b $< -a sce_sys/icon0.png=sce_sys/icon0.png $@

%.elf: $(OBJS)
	$(CC) $(CFLAGS) $(LDFLAGS) $^ $(LIBS) -o $@
	$(VITASDK)/bin/arm-vita-eabi-strip $@

clean:
	rm -f $(TARGET).elf $(TARGET).vpk $(OBJS) param.sfo
