function testSwitch(v) {
    switch(v) {
        case 12:
            return 0;
        case 15:
            return 1;
        case 1234:
            return 2;
        default:
            return 3;
    }

    return 12345678;
}

var x = 123;

function neg(y) {
    return (-y);
}

function testSwitchEvil(v) {
    switch(v) {
        case 12:
            return 0;
        case x + 1:
            return 1;
        case neg(x):
            return 2;
        default:
            return 3;
    }

    return 12345678;
}

var print = console.log;

print(testSwitch(1234));
print(testSwitch(1235));
print(testSwitchEvil(124));
print(testSwitchEvil(-123));
