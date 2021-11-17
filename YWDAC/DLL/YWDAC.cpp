#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>


BOOL APIENTRY DllMain(HMODULE hModule, DWORD  ul_reason_for_call, LPVOID lpReserved)
{
    UNREFERENCED_PARAMETER(hModule);
    UNREFERENCED_PARAMETER(ul_reason_for_call);
    UNREFERENCED_PARAMETER(lpReserved);

    SYSTEMTIME st, lt;
    GetSystemTime(&st);
    GetLocalTime(&lt);

    char msgboxTitle[] = "You Wouldn't Download A Car";
    char msgboxMsg[1024];
    _snprintf_s(msgboxMsg, 1024, 1024, "\"You Wouldn't Download A Car\" executed at %02d/%02d/%02d %02d:%02d:%02d", lt.wMonth, lt.wDay, lt.wYear, lt.wHour, lt.wMinute, lt.wSecond);
    int msgboxID = MessageBoxA(
        NULL,
        msgboxMsg,
        msgboxTitle,
        MB_ICONEXCLAMATION
    );

	return true;
}