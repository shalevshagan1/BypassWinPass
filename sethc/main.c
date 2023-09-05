#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

#define MAX_USERNAME_LENGTH 20
#define BUFFSIZE 128

// TODO check if Hebrew username causes Hebrew locale and code page
int main()
{
	wchar_t input[100]; // Wide character string to store user input
	wchar_t output[100]; // Wide character string to store user input
	setlocale(LC_ALL, "he_IL.CP862");

	wprintf(L"Enter a UNICODE string: ");
	wscanf_s(L"%99ls", input, (unsigned)_countof(input));
	//MultiByteToWideChar(862, MB_PRECOMPOSED, _In_NLS_string_(cbMultiByte)input, -1, output, 0);
	mbstowcs()
	wprintf(L"You entered: %ls\n", input);
	//printf("running...\n");
	//FILE* pipe;
	//wchar_t buff[BUFFSIZE];
	//wchar_t username[MAX_USERNAME_LENGTH + 1];
	//wchar_t prompt[BUFFSIZE];

	//printf("Enter Username: ");
	//wscanf_s(L"%ls", username, MAX_USERNAME_LENGTH);

	//swprintf_s(prompt, BUFFSIZE, L"echo | net user %ls * 2>&1", username);
	//pipe = _wpopen(prompt, L"rt");

	//fgetws(buff, BUFFSIZE, pipe);
	//if (wcsstr(buff, L"successfully") != NULL)
	//{
	//	printf("WE GOOD, NO PASSWORD! Enter empty password");
	//}
	//else
	//{
	//	printf("something went wrong...\nPlease open an issue on github.com/shalevshagan1/<PROJECT_NAME>/issues with the following output:\n");
	//	_putws(buff); // TODO - Make buff only stderr
	//}

	//_pclose(pipe);
	//system("pause");
}