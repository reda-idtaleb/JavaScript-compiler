var x= 2;

function toto(i) {
    i += x;

    function tata(b) {
        return i+b+x;
    };

    return tata;
} ;

var y = toto(3)(5);
