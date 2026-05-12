#include <klee/klee.h>

int main() {
    int x;
    klee_make_symbolic(&x, sizeof(x), "x");

    int *p = 0;

    if (x > 100) {
        *p = 5;   // null dereference
    }

    return 0;
}
