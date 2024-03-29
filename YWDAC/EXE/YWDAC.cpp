#include <Windows.h>
#include <stdio.h>


int main(void) {
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
    return 0;
}