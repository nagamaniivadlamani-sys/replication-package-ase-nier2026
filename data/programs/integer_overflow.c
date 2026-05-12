#include <limits.h>
#include <klee/klee.h>

int main() {
    int x;

    klee_make_symbolic(&x, sizeof(x), "x");

    // Relax constraint
    klee_assume(x > 1000000000);

    if (x > 2147483000) {
        int y = x + 1; // overflow zone
    }

    return 0;
}	
