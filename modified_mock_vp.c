
#include <stdio.h>
#include <string.h>

char items[3][10];

void func_a(){
    char* buff;
    int i = 0;
    do{
        printf("input item:");
        buff = &items[i][0];
        i++;
        scanf("%s", buff);
    } while (i < 3);
}

void func_b(){
    char *buff;
    printf("done adding items
");
    int j;
    printf("display item #:");
    scanf("%d", &j);
    if (j >= 0 && j < 3) {
        buff = &items[j][0];
        printf("item %d: %s
", j, buff);
    } else {
        printf("Invalid item number. Please enter a value between 0 and 2.
");
    }
}

#ifndef ___TEST___
int main() {
    func_a();
    func_b();
    return 0;
}
#endif
