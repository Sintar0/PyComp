int add(int x, int y) {
    int result;
    result = x + y;
    return result;
}
int main() {
    int a;
    int b;
    int c;
    a = 5;
    b = 3;
    c = add(a, b);
    debug c;
    return 0;
}