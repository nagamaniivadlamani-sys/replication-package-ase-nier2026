#include <klee/klee.h>

int main() {
    int *ptr;

    klee_make_symbolic(&ptr, sizeof(ptr), "ptr");

    // Guide KLEE
    klee_assume(ptr == 0);

    *ptr = 10; // crash

    return 0;
}
