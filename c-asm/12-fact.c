#include "base.h"

/* traduction du code */

int main() {
    /* initialisation */
    init(8192, 0, 0);

    /* traduction du code */
    goto functend_factorial;

funct_factorial:
    /* n == 0 */
    push(bp[3]);    /* n */
    push(iconst(0)); /* 0 */

    pop(r1);
    pop(r2);
    ieq(r1,r2,r1);
    push(r1);

    /* n == 1 */
    push(bp[3]);    /* n */
    push(iconst(1)); /* 1 */

    pop(r1);
    pop(r2);
    ieq(r1,r2,r1);
    push(r1);

    /* (n == 0) || (n == 1) */
    pop(r1);
    pop(r2);
    lor(r1,r2,r1);
    push(r1);

    /* if ... */
    pop(r1);
    lneg(r1,r1);
    if(asbool(r1)) goto else1;

    /* 1 */
    push(iconst(1));

    /* return */
    pop(r1);
    ret(r1);

    goto endif1;

else1:
endif1:

    push(bp[3]);    /* n */

    /* n - 1 */
    push(bp[3]);    /* n */
    push(iconst(1)); /* 1 */

    pop(r1);
    pop(r2);
    isub(r1,r2,r1);
    push(r1);

    /* appel proprement dit ; il laisse la valeur de retour sur la
     * pile */
    call(funct_factorial);

    /* la pile contient encore les arguments de l’appel, on doit
     * nettoyer */
    pop(r1);
    drop(1);
    push(r1);

    /* multiplication */
    pop(r1);
    pop(r2);
    imul(r1,r2,r1);
    push(r1);

    /* return */
    pop(r1);
    ret(r1);

    assert(0); /* tous les chemins doivent passer par un ret ! */

functend_factorial:

    push(iconst(3)); /* 3 */
    call(funct_factorial);
    pop(r1);
    drop(1);

    /* information de débugage */
    debug_reg(r1);

    return 0;

}
