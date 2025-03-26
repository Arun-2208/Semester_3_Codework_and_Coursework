/* memtest1.c*/ 
#include <stdio.h> 
#define SIZE 8
void test(int*, char*); 
int main(){
	int i = 0;
	char buf[SIZE];
	printf("Type in 5-20 chars into the text buffer\n"); 
	printf("Watch the value of i \n");
	printf("it will be corrupted when you exceed %i chars\n",SIZE); 
	printf("Type \"q\" to exit:\n");
	printf("\t| i posn\t| buf start\t| buf end\t| i value\n"); 
	do {
	test(&i, buf); 
	i++;
	}while(buf[0] != 'q');
	return 0;
}
void test(int *j, char* buf){ 
	scanf("%s",buf);
	printf("OK.\t| %u\t| %u\t| %u\t| %d\n",j, buf, &buf[SIZE],*j); 
	return;
}
