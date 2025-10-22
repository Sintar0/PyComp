int main() {
    int i;
    int sum;
    i = 0;
    sum = 0;
    while (i < 10) {
        if (i % 2 == 0) {
            i = i + 1;
            continue;
        }
        if (i == 7) {
            break;
        }
        sum = sum + i;
        i = i + 1;
    }
    debug sum;
    return 0;
}
