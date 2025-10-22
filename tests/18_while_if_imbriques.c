int main() {
    int a;
    int i;
    int count;
    a = 10;
    count = 0;
    if (a > 5) {
        i = 0;
        while (i < 3) {
            count = count + 1;
            i = i + 1;
        }
    } else {
        count = 99;
    }
    debug count;
    return 0;
}
