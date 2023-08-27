#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_USERNAME_LENGTH 20
#define BUFFSIZE 128

int main()
{
	printf("running...\n");

	FILE* pipe;
	char buff[BUFFSIZE];
	char username[MAX_USERNAME_LENGTH + 1];
	char prompt[BUFFSIZE];

	printf("Enter Username: ");
	scanf_s("%s", username, MAX_USERNAME_LENGTH);

	sprintf_s(prompt, BUFFSIZE, "echo | net user %s * 2>&1", username);
	pipe = _popen(prompt, "rt");

	fgets(buff, BUFFSIZE, pipe);
	if (strstr(buff, "successfully") != NULL)
	{
		printf("WE GOOD, NO PASSWORD! Enter empty password");
	}
	else
	{
		printf("something went wrong...\nPlease open an issue on github.com/shalevshagan1/<PROJECT_NAME>/issues with the following output:\n");
		puts(buff); // TODO - Make buff only stderr
	}

	_pclose(pipe);
	system("pause");
}