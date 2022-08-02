#include "base.h"

int main() {
    init(8192, 0, 8192);

    /* g: globals[0] */
    globals[0] = iconst(1);

    goto functend_calcul;

funct_calcul:
    /* on « alloue » la mémoire pour les variables locales : elles
     * seront sur la pile, toujours à la même position par rapport à
     * bp */
    push(iconst(2)); /* bp[-1] */
    push(iconst(3)); /* bp[-2] */

    push(iconst(2));
    push(globals[0]);

    pop(r1);
    pop(r2);
    imul(r1,r2,r1);
    push(r1);

    push(iconst(4));
    push(bp[-1]);

    pop(r1);
    pop(r2);
    imul(r1,r2,r1);
    push(r1);

    pop(r1);
    pop(r2);
    iadd(r1,r2,r1);
    push(r1);

    push(iconst(8));
    push(bp[-2]);

    pop(r1);
    pop(r2);
    imul(r1,r2,r1);
    push(r1);

    pop(r1);
    pop(r2);
    iadd(r1,r2,r1);
    push(r1);

    push(iconst(16));
    push(bp[3]);

    pop(r1);
    pop(r2);
    imul(r1,r2,r1);
    push(r1);

    pop(r1);
    pop(r2);
    iadd(r1,r2,r1);
    push(r1);

    push(iconst(32));
    push(bp[4]);

    pop(r1);
    pop(r2);
    imul(r1,r2,r1);
    push(r1);

    pop(r1);
    pop(r2);
    iadd(r1,r2,r1);
    push(r1);

    /* return */
    pop(r1);
    drop(2); /* supprime les variables locales de la pile */
    ret(r1);

    assert(0); /* tous les chemins doivent passer par un ret ! */

functend_calcul:

    /* on empile les arguments en ordre inverse (nombre variable
     * d’arguments... */
    push(iconst(5));
    push(iconst(4));
    call(funct_calcul);

    pop(r1);
    drop(2);
    debug_reg(r1);

    return 0;
}
