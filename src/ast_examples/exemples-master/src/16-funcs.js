var global = 10;

function externe(a) {
    function interne(b) {
        return a + b + global;
    };

    return interne;
};

var f = externe(11);

print(f(12));
