int main() {
    int mem;
    int *p;
    mem[0] = 42;
    p = &mem[0];
    debug *p;
    *p = 100;
    debug mem[0];
    return 0;
}