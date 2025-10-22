int main() {
    int a;
    int b;
    int result;
    a = 10;
    b = 5;
    if (a > 5) {
        if (b < 10) {
            result = 1;
        } else {
            result = 2;
        }
    } else {
        result = 0;
    }
    debug result;
    return 0;
}
