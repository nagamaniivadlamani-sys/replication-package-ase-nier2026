#include <klee/klee.h>

int main() {
    char buf[6];
    klee_make_symbolic(buf, sizeof(buf), "buf");

    if (buf[0] == 'A' && buf[1] == 'B') {
        buf[10] = 'X';  // overflow
    }

    return 0;
}
