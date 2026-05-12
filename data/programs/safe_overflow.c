#include <stdio.h>
int main(){
    char buf[10];
    fgets(buf, sizeof(buf), stdin);
    return 0;
}
