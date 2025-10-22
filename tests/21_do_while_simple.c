int main() {
    int i;
    int sum;
    i = 0;
    sum = 0;
    do {
        sum = sum + i;
        i = i + 1;
    } while (i < 5);
    debug sum;
    return 0;
}
