int main() {
    int i;
    int j;
    int count;
    i = 0;
    count = 0;
    while (i < 2) {
        if (i == 0) {
            j = 0;
            while (j < 2) {
                count = count + 1;
                j = j + 1;
            }
        } else {
            count = count + 10;
        }
        i = i + 1;
    }
    debug count;
    return 0;
}
