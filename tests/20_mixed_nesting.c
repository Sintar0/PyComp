int main() {
    int x;
    int sum;
    x = 0;
    sum = 0;
    while (x < 3) {
        if (x % 2 == 0) {
            int y;
            y = 0;
            while (y < 2) {
                sum = sum + x + y;
                y = y + 1;
            }
        } else {
            sum = sum + 10;
        }
        x = x + 1;
    }
    debug sum;
    return 0;
}
