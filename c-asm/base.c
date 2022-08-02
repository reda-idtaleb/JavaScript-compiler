#include <stdlib.h>
#include <assert.h>

#include "base.h"

/** \file base.c
 * \brief Déclare les variables et définit les fonctions nécessaires
 * pour un code C de style assembleur */

/** registre général */
word_t r1;
/** registre général */
word_t r2;
/** registre général */
word_t r3;
/** registre général */
word_t r4;
/** registre général */
word_t r5;
/** registre général */
word_t r6;
/** registre général */
word_t r7;
/** registre général */
word_t r8;
/** registre général */
word_t r9;
/** registre général */
word_t r10;
/** registre général */
word_t r11;
/** registre général */
word_t r12;
/** registre général */
word_t r13;
/** registre général */
word_t r14;
/** registre général */
word_t r15;
/** registre général */
word_t r16;

/** base pointer (base du cadre de pile) */
word_t rbp;
/** stack pointer (haut de pile) */
word_t rsp;

/** variables globales
 *
 * Les variables globales sont stockées dans ce tableau dont chaque
 * case est un mot processeur (comme un registre). */
word_t * globals = NULL;

/** pile
 *
 * La pile est vue comme un grand tableau dont chaque case est
 * un mot processeur (comme un registre). */
word_t * stack = NULL;
/** tas
 *
 * Le tas est vu comme une grande zone mémoire, sans structure fixe
 * (sans typage) : la structure sera fixée suivant les besoins
 * (allocations). */
void * heap = NULL;

word_t __hack_register__;

/** initialisation (allocation de la pile, du tas et des variables globales) */
void init(unsigned stack_size, unsigned heap_size, unsigned globals_size) {
    /* on ne peut pas s’en sortir correctement sans pile */
    assert(stack_size > 0);

    stack = malloc(stack_size);
    assert(stack != NULL);
    rbp.a = ((char*)stack) + stack_size;
    rsp.a = ((char*)stack) + stack_size;

    if(heap_size > 0) {
        heap = malloc(heap_size);
        assert(heap != NULL);
    }
    if(globals_size > 0) {
        globals = malloc(globals_size);
        assert(globals != NULL);
    }
}
