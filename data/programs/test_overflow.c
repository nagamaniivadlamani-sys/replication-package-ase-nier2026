#include <stdio.h>
#include <klee/klee.h>

int main() {
    char buffer[8];

    klee_make_symbolic(buffer, sizeof(buffer), "buffer");

    klee_assume(buffer[0] >= 'A');
    klee_assume(buffer[0] <= 'Z');

    if (buffer[0] == 'A' && buffer[1] == 'A') {
        int *p = NULL;
        *p = 10;
    }

    return 0;
}
