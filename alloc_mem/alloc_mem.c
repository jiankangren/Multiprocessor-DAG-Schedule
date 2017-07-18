//
// Copyright The Telecommunications Research Center Vienna (FTW) 2015
//
// Author(s): Arian Baer
//

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main(int argc, char *argv[]) {
	int *p;

	int mb = 0;
	if (argc > 1) {
		mb = atoi(argv[1]);
	}

	printf("Allocating %dMB of RAM.\n", mb);

	int inc=1024*1024*sizeof(char);

	int i = 0;
	for(i = 0; i < mb; i++) {
		p=(void*) calloc(1,inc);
		if(!p) {
			printf("Out of memory!\n");
			exit(-1);
		}
		memset(p, 0, inc);
	}

	printf("done.\n");
	while(1) {
		sleep(1000);
	}
}
