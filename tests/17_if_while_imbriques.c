int main() {
    int i;
    int count;
    i = 0;
    count = 0;
    while (i < 5) {
        if (i % 2 == 0) {
            count = count + i;
        }
        i = i + 1;
    }
    debug count;
    return 0;
}
