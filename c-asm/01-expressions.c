#include "base.h"

/* Exemple de traduction du code 01-expressions.js
 * Ne contient que la compilation des deux premières expressions
 * */

int main() {
    init(8192, 0, 0);

    /* expression: 1; */
    push(iconst(1));

    /* débugage : pour chaque ExpressionStatement, on peut afficher /
     * tracer la valeur qui a été laissée sur la pile par l’évaluation
     * de l’expression */
    pop(r1);
    debug_reg(r1);

    /* expression: 1 + 2 */
    push(iconst(1));
    push(iconst(2));

    pop(r1);
    pop(r2);
    iadd(r1,r2,r1);
    push(r1);

    pop(r1);
    debug_reg(r1);

    /* etc. */
    return 0;
}
