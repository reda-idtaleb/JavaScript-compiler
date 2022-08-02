function factorial(n) {
    if (n == 0 || n == 1) {
        return 1;  // 0! = 1! = 1
    }
    return n * factorial(n - 1);
} ;

factorial(3); // returns 6
