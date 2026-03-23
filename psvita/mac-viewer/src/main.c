#include <stdio.h>
#include <string.h>

#include <psp2/ctrl.h>
#include <psp2/display.h>
#include <psp2/kernel/processmgr.h>
#include <psp2/kernel/threadmgr.h>

#define MAX_MAC_TEXT 64

#define DISPLAY_WIDTH 960
#define DISPLAY_HEIGHT 544
#define DISPLAY_STRIDE 960

static uint32_t frame_buf[DISPLAY_STRIDE * DISPLAY_HEIGHT];

static void set_framebuffer(void)
{
    SceDisplayFrameBuf fb;
    fb.size = sizeof(SceDisplayFrameBuf);
    fb.base = frame_buf;
    fb.pitch = DISPLAY_STRIDE;
    fb.pixelformat = SCE_DISPLAY_PIXELFORMAT_A8B8G8R8;
    fb.width = DISPLAY_WIDTH;
    fb.height = DISPLAY_HEIGHT;
    sceDisplaySetFrameBuf(&fb, SCE_DISPLAY_SETBUF_NEXTFRAME);
}

static void clear_screen(uint32_t color)
{
    for (int y = 0; y < DISPLAY_HEIGHT; ++y) {
        uint32_t *row = frame_buf + y * DISPLAY_STRIDE;
        for (int x = 0; x < DISPLAY_WIDTH; ++x) {
            row[x] = color;
        }
    }
}

static int get_glyph(char c, uint8_t out[7])
{
    memset(out, 0, 7);
    switch (c) {
        case 'B': out[0]=0x1E; out[1]=0x11; out[2]=0x11; out[3]=0x1E; out[4]=0x11; out[5]=0x11; out[6]=0x1E; return 1;
        case 'T': out[0]=0x1F; out[1]=0x04; out[2]=0x04; out[3]=0x04; out[4]=0x04; out[5]=0x04; out[6]=0x04; return 1;
        case 'M': out[0]=0x11; out[1]=0x1B; out[2]=0x15; out[3]=0x11; out[4]=0x11; out[5]=0x11; out[6]=0x11; return 1;
        case 'A': out[0]=0x0E; out[1]=0x11; out[2]=0x11; out[3]=0x1F; out[4]=0x11; out[5]=0x11; out[6]=0x11; return 1;
        case 'C': out[0]=0x0E; out[1]=0x11; out[2]=0x10; out[3]=0x10; out[4]=0x10; out[5]=0x11; out[6]=0x0E; return 1;
        case ':': out[0]=0x00; out[1]=0x04; out[2]=0x00; out[3]=0x00; out[4]=0x04; out[5]=0x00; out[6]=0x00; return 1;
        case ' ': return 1;
        case '0': out[0]=0x0E; out[1]=0x11; out[2]=0x13; out[3]=0x15; out[4]=0x19; out[5]=0x11; out[6]=0x0E; return 1;
        case '1': out[0]=0x04; out[1]=0x0C; out[2]=0x04; out[3]=0x04; out[4]=0x04; out[5]=0x04; out[6]=0x0E; return 1;
        case '2': out[0]=0x0E; out[1]=0x11; out[2]=0x01; out[3]=0x06; out[4]=0x08; out[5]=0x10; out[6]=0x1F; return 1;
        case '3': out[0]=0x0E; out[1]=0x11; out[2]=0x01; out[3]=0x06; out[4]=0x01; out[5]=0x11; out[6]=0x0E; return 1;
        case '4': out[0]=0x02; out[1]=0x06; out[2]=0x0A; out[3]=0x12; out[4]=0x1F; out[5]=0x02; out[6]=0x02; return 1;
        case '5': out[0]=0x1F; out[1]=0x10; out[2]=0x1E; out[3]=0x01; out[4]=0x01; out[5]=0x11; out[6]=0x0E; return 1;
        case '6': out[0]=0x06; out[1]=0x08; out[2]=0x10; out[3]=0x1E; out[4]=0x11; out[5]=0x11; out[6]=0x0E; return 1;
        case '7': out[0]=0x1F; out[1]=0x01; out[2]=0x02; out[3]=0x04; out[4]=0x08; out[5]=0x08; out[6]=0x08; return 1;
        case '8': out[0]=0x0E; out[1]=0x11; out[2]=0x11; out[3]=0x0E; out[4]=0x11; out[5]=0x11; out[6]=0x0E; return 1;
        case '9': out[0]=0x0E; out[1]=0x11; out[2]=0x11; out[3]=0x0F; out[4]=0x01; out[5]=0x02; out[6]=0x0C; return 1;
        case 'F': out[0]=0x1F; out[1]=0x10; out[2]=0x10; out[3]=0x1E; out[4]=0x10; out[5]=0x10; out[6]=0x10; return 1;
        case 'E': out[0]=0x1F; out[1]=0x10; out[2]=0x10; out[3]=0x1E; out[4]=0x10; out[5]=0x10; out[6]=0x1F; return 1;
        case 'D': out[0]=0x1E; out[1]=0x11; out[2]=0x11; out[3]=0x11; out[4]=0x11; out[5]=0x11; out[6]=0x1E; return 1;
    }
    return 0;
}

static void draw_char(int x, int y, char c, uint32_t color)
{
    uint8_t rows[7];
    if (!get_glyph(c, rows)) {
        return;
    }
    for (int row = 0; row < 7; ++row) {
        uint8_t bits = rows[row];
        for (int col = 0; col < 5; ++col) {
            if (bits & (1 << (4 - col))) {
                int px = x + col;
                int py = y + row;
                if (px >= 0 && px < DISPLAY_WIDTH && py >= 0 && py < DISPLAY_HEIGHT) {
                    frame_buf[py * DISPLAY_STRIDE + px] = color;
                }
            }
        }
    }
}

static void draw_text(int x, int y, const char *text, uint32_t color)
{
    int cursor = x;
    for (const char *p = text; *p; ++p) {
        draw_char(cursor, y, *p, color);
        cursor += 6;
    }
}

static int get_bt_mac(char *out, size_t out_len)
{
    (void)out_len;
    // TODO: ligar a API correta do VitaSDK para obter o MAC Bluetooth.
    // Se nao estiver disponivel, diz-me qual o header/funcao que tens.
    snprintf(out, out_len, "Bluetooth MAC: (indisponivel)");
    return 0;
}

int main(void)
{
    SceCtrlData pad;
    char mac_text[MAX_MAC_TEXT];

    sceCtrlSetSamplingMode(SCE_CTRL_MODE_ANALOG);
    set_framebuffer();
    clear_screen(0xFF000000);
    get_bt_mac(mac_text, sizeof(mac_text));

    while (1) {
        sceCtrlPeekBufferPositive(0, &pad, 1);
        if (pad.buttons & SCE_CTRL_START) {
            break;
        }

        clear_screen(0xFF000000);
        draw_text(20, 20, mac_text, 0xFFFFFFFF);
        sceKernelDelayThread(10000);
    }

    sceKernelExitProcess(0);
    return 0;
}
