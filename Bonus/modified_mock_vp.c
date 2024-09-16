
#include <stdio.h>
#include <string.h>
#include <unistd.h>

char items[3][10];

void func_a(){
    char buff[40];
    int i = 0;
    do{
        printf("input item:");
        fgets(buff, 40, stdin);
        buff[strcspn(buff, "\n")] = 0;
        if (strlen(buff) != 0 && strlen(buff) <= 10) {
            strcpy(&items[i][0], buff);
            i++;
        }
    }while(strlen(buff)!=0);
}

void func_b(){
    char *buff;
    printf("done adding items\n");
    int j;
    printf("display item #:");
    scanf("%d", &j);
    if (j >= 0 && j < 3) {
        buff = &items[j][0];
        printf("item %d: %s\n", j, buff);
    }
}

#ifndef ___TEST___
int main()
{

    func_a();

    func_b();


    return 0;
}
#endif
