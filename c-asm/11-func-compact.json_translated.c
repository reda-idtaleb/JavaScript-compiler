#include "base.h"

int main(){
    init(8192, 0, 8192); 
    

    push(iconst(10)); 
    pop(r1); 
    globals[0] = r1; 
    debug_reg(r1); 
    

    printf("\n");
    goto functend_blob; 
    
funct_blob: 
    push(globals[0]); 
    push(bp[3]); 
    pop(r1); 
    pop(r2); 
    iadd(r1, r2, r1); 
    push(r1); 
    
    pop(r1); 
    push(globals[0]); 
    globals[0].i = r1.i; 
    
    push(globals[0]); 
    pop(r1); 
    drop(1); 
    ret(r1); 
    assert(0); 
    
functend_blob: 
    debug_reg(r1); 
    

    printf("\n");
    debug_reg(r1); 
    

    printf("\n");
    push(iconst(1)); 
    call(funct_blob); 
    pop(r1); 
    drop(1); 
    push(r1); 
    call(funct_print_0); 
    
funct_print_0: 
    debug_reg(bp[3]); 
    drop(1); 
    push(r1); 
    debug_reg(r1); 
    

    printf("\n");
    push(iconst(2)); 
    call(funct_blob); 
    pop(r1); 
    drop(1); 
    push(r1); 
    call(funct_print_1); 
    
funct_print_1: 
    debug_reg(bp[3]); 
    drop(1); 
    push(r1); 
    debug_reg(r1); 
    

    printf("\n");
    debug_reg(r1); 
    

    return 0;
}