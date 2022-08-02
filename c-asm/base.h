#include "hacks.h"

#ifndef _BASE_H_
#define _BASE_H_

/** \file base.h
 * \brief Déclare les variables et définit les fonctions nécessaires
 * pour un code C de style assembleur; « réexporte » hacks.h qui
 * définit les macros correspondant aux instructions type assembleur */

/** registre général */
extern word_t r1;
/** registre général */
extern word_t r2;
/** registre général */
extern word_t r3;
/** registre général */
extern word_t r4;
/** registre général */
extern word_t r5;
/** registre général */
extern word_t r6;
/** registre général */
extern word_t r7;
/** registre général */
extern word_t r8;
/** registre général */
extern word_t r9;
/** registre général */
extern word_t r10;
/** registre général */
extern word_t r11;
/** registre général */
extern word_t r12;
/** registre général */
extern word_t r13;
/** registre général */
extern word_t r14;
/** registre général */
extern word_t r15;
/** registre général */
extern word_t r16;

/** base pointer (base du cadre de pile) */
extern word_t rbp;
/** stack pointer (haut de pile) */
extern word_t rsp;

/** variables globales
 *
 * Les variables globales sont stockées dans ce tableau dont chaque
 * case est un mot processeur (comme un registre). */
extern word_t * globals;
/** pile
 *
 * La pile est vue comme un grand tableau dont chaque case est
 * un mot processeur (comme un registre). */
extern word_t * stack;
/** tas
 *
 * Le tas est vu comme une grande zone mémoire, sans structure fixe
 * (sans typage) : la structure sera fixée suivant les besoins
 * (allocations). */
extern void * heap;


/** initialisation (allocation de la pile, du tas et des variables globales) */
extern void init(unsigned stack_size, unsigned heap_size, unsigned globals_size);

#endif
