/* memtest2.c*/ 
#include <stdio.h> 
int main()
{
	char first[12]; char last[12];
	printf("Type in your first name: "); 
	gets(first);
	printf("Type in your last name: "); 
	gets(last);
	printf("Hello %s %s\n", first, last);
	return 0;
}
