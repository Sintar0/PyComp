int main() {
    int i;
    int sum;
    i = 0;
    sum = 0;
    while (i < 5) {
        sum = sum + i;
        i = i + 1;
    }
    debug sum;
    debug i;
    return 0;
}