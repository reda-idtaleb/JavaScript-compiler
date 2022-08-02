#include "base.h"

int main(){
    init(8192, 0, 8192); 
    

    push(aconst(0)); 
    pop(r1); 
    globals[0] = r1; 
    debug_reg(r1); 
    

    printf("\n");
    goto for_init_1; 
    
for_init_1: 
    push(iconst(0)); 
    pop(r1); 
    push(globals[0]); 
    globals[0].i = r1.i; 
    goto test_stmt_1; 
    
test_stmt_1: 
    push(globals[0]); 
    push(iconst(20)); 
    pop(r1); 
    pop(r2); 
    ilt(r1, r2, r1); 
    push(r1); 
    
    pop(r1); 
    if(asbool(r1)) goto for_body_1; 
    goto end_stmt_1; 
    
for_body_1: 
    push(globals[0]); 
    call(funct_print_0); 
    
funct_print_0: 
    debug_reg(bp[3]); 
    drop(1); 
    push(r1); 
    
    goto test_stmt_2; 
    
test_stmt_2: 
    push(globals[0]); 
    push(iconst(10)); 
    pop(r1); 
    pop(r2); 
    ilt(r1, r2, r1); 
    push(r1); 
    
    pop(r1); 
    if(asbool(r1)) goto for_body_2; 
    goto end_stmt_2; 
    
for_body_2: 
    push(globals[0]); 
    call(funct_print_1); 
    
funct_print_1: 
    debug_reg(bp[3]); 
    drop(1); 
    push(r1); 
    push(iconst(2)); 
    pop(r1); 
    push(globals[0]); 
    globals[0].i += r1.i; 
    goto test_stmt_2; 
    
end_stmt_2: 
    push(globals[0]); 
    globals[0].i += 1; 
    goto test_stmt_1; 
    
end_stmt_1: 
    debug_reg(r1); 
    

    printf("\n");
    debug_reg(r1); 
    

    return 0;
}