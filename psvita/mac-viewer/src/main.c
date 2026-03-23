#include <psp2/debugScreen.h>
#include <psp2/kernel/processmgr.h>
#include <psp2/kernel/threadmgr.h>

int main(void)
{
    sceDebugScreenInit();
    psvDebugScreenPrintf("Hello World!\n");
    sceKernelDelayThread(5 * 1000 * 1000);
    sceKernelExitProcess(0);
    return 0;
}

