int factorial(int n) {
    int result;
    if (n <= 1) {
        result = 1;
    } else {
        result = n * factorial(n - 1);
    }
    return result;
}
int main() {
    int val;
    val = factorial(5);
    debug val;
    val = factorial(3);
    debug val;
    return 0;
}