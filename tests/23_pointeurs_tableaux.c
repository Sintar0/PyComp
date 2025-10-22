int main() {
    int arr;
    int *p;
    p = &arr[0];
    *p = 42;
    debug arr[0];
    p = &arr[2];
    *p = 100;
    debug arr[2];
    return 0;
}