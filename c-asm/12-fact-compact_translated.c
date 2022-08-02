#include "base.h"

int main(){
    init(8192, 0, 8192); 
    

    goto functend_factorial; 
    
funct_factorial: 
    goto if_test_1; 
    
if_test_1: 
    push(bp[3]); 
    push(iconst(0)); 
    pop(r1); 
    pop(r2); 
    ieq(r1, r2, r1); 
    push(r1); 
    
    push(bp[3]); 
    push(iconst(1)); 
    pop(r1); 
    pop(r2); 
    ieq(r1, r2, r1); 
    push(r1); 
    
    pop(r1); 
    pop(r2); 
    lor(r1, r1, r2); 
    push(r1); 
    
    pop(r1); 
    if(asbool(r1)) goto if_consequent_1; 
    goto if_alternate_1; 
    
if_consequent_1: 
    push(iconst(1)); 
    pop(r1); 
    ret(r1); 
    assert(0); 
    goto if_end_1; 
    
if_alternate_1: 
    goto if_end_1; 
    
if_end_1: 
    
    push(bp[3]); 
    push(bp[3]); 
    push(iconst(1)); 
    pop(r1); 
    pop(r2); 
    isub(r1, r2, r1); 
    push(r1); 
    
    call(funct_factorial); 
    pop(r1); 
    drop(1); 
    push(r1); 
    pop(r1); 
    pop(r2); 
    imul(r1, r2, r1); 
    push(r1); 
    
    pop(r1); 
    ret(r1); 
    assert(0); 
    
functend_factorial: 
    debug_reg(r1); 
    

    printf("\n");
    debug_reg(r1); 
    

    printf("\n");
    push(iconst(3)); 
    call(funct_factorial); 
    pop(r1); 
    drop(1); 
    push(r1); 
    debug_reg(r1); 
    

    printf("\n");
    debug_reg(r1); 
    

    return 0;
}