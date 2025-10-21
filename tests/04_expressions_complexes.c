int main() {
    int a;
    int b;
    int c;
    int result;
    a = 2;
    b = 3;
    c = 4;
    result = a + b * c;
    debug result;
    result = (a + b) * c;
    debug result;
    result = a * b + c * 2;
    debug result;
    result = (a + b) * (c - 1);
    debug result;
    return 0;
}