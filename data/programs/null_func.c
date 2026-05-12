#include <stdio.h>
void test(int *p){
    *p = 10;
}
int main(){
    int *p = NULL;
    test(p);
    return 0;
}
