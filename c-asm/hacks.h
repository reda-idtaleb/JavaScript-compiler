#include <stdio.h>
#include <assert.h>

#ifndef _HACKS_H_
#define _HACKS_H_

/** \file hacks.h
 * \brief Déclare les types de base et les macros qui implémentent un
 * code C de style assembleur */

/** Mot processeur.
 *
 * Un mot processeur a une certaine taille (64 bits sur l’architecture
 * x86_64) mais pas de type en soi : les instructions interprètent ces
 * 64 bits. Utilise donc une union pour représenter en C le fait qu’un
 * registre peut contenir des données de n’importe lequel de ces types */
union word_u {
    double d;            /**< ce mot vu comme \c double */
    long int i;          /**< ce mot vu comme \c long */
    unsigned long int u; /**< ce mot vu comme \c unsigned */
    void *a;             /**< ce mot vu comme adresse */
};

/** Mot processeur.
 *
 * Définit \a word_t comme version compact de <tt>union word_u</tt> */
typedef union word_u word_t;


/* Un _magic_ (choisi aléatoirement) pour détecter un problème de
 * cohérence d’état de pile au moment d’un _ret_ */
#define STACK_MAGIC (iconst(0x67ed7e8f706164c8))
extern word_t __hack_register__;

/** Macro permettant d’accéder au contenu du cadre de pile en
 * utilisant la syntaxe C standard pour les tableaux.
 *
 * - <tt>bp[-1]</tt> désigne la première variable locale de la fonction
 * - <tt>bp[-2]</tt> désigne la deuxième variable locale de la fonction
 * - etc.
 * - <tt>bp[3]</tt> désigne le premier argument de la fonction
 * - <tt>bp[4]</tt> désigne le deuxième argument de la fonction
 * - etc.
 * */
#define bp ((word_t *)(rbp.a))
/** Macro permettant d’accéder simplement au haut de pile.
 *
 * Cette macro est surtout utilisée par les autres macros à utiliser :
 * \c push, \c pop et \c drop */
#define sp ((word_t *)(rsp.a))

/** Empile le contenu d’un registre.
 *
 * \param r registre à pousser sur la pile */
#define push(r) rsp.a = (word_t*)(rsp.a)-1; (*sp) = (r)

/** Dépile dans un registre.
 *
 * \param r registre dans lequel charger le haut de la pile */
#define pop(r)  (r) = (*sp); rsp.a = (word_t*)(rsp.a)+1

/** Oublie les \a n éléments en haut de pile.
 *
 * \param n nombre de mots à éliminer */
#define drop(n) rsp.a = (word_t*)(rsp.a)+(n)

/** Définit un mot contenant la valeur \c double donnée. */
#define dconst(x) ((union word_u){.d = (x)})
/** Définit un mot contenant la valeur \c long donnée. */
#define iconst(x) ((union word_u){.i = (x)})
/** Définit un mot contenant la valeur \c unsigned donnée. */
#define uconst(x) ((union word_u){.u = (x)})
/** Définit un mot contenant l’adresse donnée. */
#define aconst(x) ((union word_u){.a = (x)})

/** Affecte à un registre l’addition entière signée de deux mots
 * (qui peuvent être des registres ou des constantes).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define iadd(rdst,rsrc1,rsrc2) ((rdst).i = ((rsrc1).i + (rsrc2).i))
/** Affecte à un registre la soustraction entière signée de deux mots
 * (qui peuvent être des registres ou des constantes).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define isub(rdst,rsrc1,rsrc2) ((rdst).i = ((rsrc1).i - (rsrc2).i))
/** Affecte à un registre la multiplication entière signée de deux mots
 * (qui peuvent être des registres ou des constantes).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define imul(rdst,rsrc1,rsrc2) ((rdst).i = ((rsrc1).i * (rsrc2).i))
/** Affecte à un registre la division entière signée de deux mots
 * (qui peuvent être des registres ou des constantes).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define idiv(rdst,rsrc1,rsrc2) ((rdst).i = ((rsrc1).i / (rsrc2).i))
/** Affecte à un registre le reste de la division entière signée de
 * deux mots (qui peuvent être des registres ou des constantes).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define imod(rdst,rsrc1,rsrc2) ((rdst).i = ((rsrc1).i % (rsrc2).i))
/** Affecte à un registre la valeur booléenne vraie
 * (<tt>asbool(rdst)</tt> sera vrai) si \c rsrc1 est strictement
 * inférieur à \c rsrc2 (comparaison entière signée).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define ilt(rdst,rsrc1,rsrc2) ((rdst).i = ((rsrc1).i < (rsrc2).i))
/** Affecte à un registre la valeur booléenne vraie
 * (<tt>asbool(rdst)</tt> sera vrai) si \c rsrc1 est inférieur ou égal
 * à \c rsrc2 (comparaison entière signée).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define ile(rdst,rsrc1,rsrc2) ((rdst).i = ((rsrc1).i <= (rsrc2).i))
/** Affecte à un registre la valeur booléenne vraie
 * (<tt>asbool(rdst)</tt> sera vrai) si \c rsrc1 est égal à \c rsrc2
 * (comparaison entière signée).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define ieq(rdst,rsrc1,rsrc2) ((rdst).i = ((rsrc1).i == (rsrc2).i))

/** Affecte à un registre l’addition entière non-signée de deux mots
 * (qui peuvent être des registres ou des constantes).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define uadd(rdst,rsrc1,rsrc2) ((rdst).u = ((rsrc1).u + (rsrc2).u))
/** Affecte à un registre la soustraction entière non-signée de deux
 * mots (qui peuvent être des registres ou des constantes).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define usub(rdst,rsrc1,rsrc2) ((rdst).u = ((rsrc1).u - (rsrc2).u))
/** Affecte à un registre la multiplication entière non-signée de deux
 * mots (qui peuvent être des registres ou des constantes).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define umul(rdst,rsrc1,rsrc2) ((rdst).u = ((rsrc1).u * (rsrc2).u))
/** Affecte à un registre la division entière non-signée de deux mots
 * (qui peuvent être des registres ou des constantes).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define udiv(rdst,rsrc1,rsrc2) ((rdst).u = ((rsrc1).u / (rsrc2).u))
/** Affecte à un registre le reste de la division entière non-signée
 * de deux mots (qui peuvent être des registres ou des constantes).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define umod(rdst,rsrc1,rsrc2) ((rdst).u = ((rsrc1).u % (rsrc2).u))
/** Affecte à un registre la valeur booléenne vraie
 * (<tt>asbool(rdst)</tt> sera vrai) si \c rsrc1 est strictement
 * inférieur à \c rsrc2 (comparaison entière non-signée).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define ult(rdst,rsrc1,rsrc2) ((rdst).u = ((rsrc1).u < (rsrc2).u))
/** Affecte à un registre la valeur booléenne vraie
 * (<tt>asbool(rdst)</tt> sera vrai) si \c rsrc1 est inférieur ou égal
 * à \c rsrc2 (comparaison entière non-signée).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define ule(rdst,rsrc1,rsrc2) ((rdst).u = ((rsrc1).u <= (rsrc2).u))
/** Affecte à un registre la valeur booléenne vraie
 * (<tt>asbool(rdst)</tt> sera vrai) si \c rsrc1 est égal à \c rsrc2
 * (comparaison entière non-signée).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define ueq(rdst,rsrc1,rsrc2) ((rdst).u = ((rsrc1).u == (rsrc2).u))

/** Affecte à un registre l’addition flottante de deux mots (qui
 * peuvent être des registres ou des constantes).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define dadd(rdst,rsrc1,rsrc2) ((rdst).d = ((rsrc1).d + (rsrc2).d))
/** Affecte à un registre la soustraction flottante de deux mots (qui
 * peuvent être des registres ou des constantes).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define dsub(rdst,rsrc1,rsrc2) ((rdst).d = ((rsrc1).d - (rsrc2).d))
/** Affecte à un registre la multiplication flottante de deux mots
 * (qui peuvent être des registres ou des constantes).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define dmul(rdst,rsrc1,rsrc2) ((rdst).d = ((rsrc1).d * (rsrc2).d))
/** Affecte à un registre la division flottante de deux mots (qui
 * peuvent être des registres ou des constantes).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define ddiv(rdst,rsrc1,rsrc2) ((rdst).d = ((rsrc1).d / (rsrc2).d))
/** Affecte à un registre la valeur booléenne vraie
 * (<tt>asbool(rdst)</tt> sera vrai) si \c rsrc1 est strictement
 * inférieur à \c rsrc2 (comparaison flottante).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define dlt(rdst,rsrc1,rsrc2) ((rdst).d = ((rsrc1).d < (rsrc2).d))
/** Affecte à un registre la valeur booléenne vraie
 * (<tt>asbool(rdst)</tt> sera vrai) si \c rsrc1 est inférieur ou égal
 * à \c rsrc2 (comparaison flottante).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define dle(rdst,rsrc1,rsrc2) ((rdst).d = ((rsrc1).d <= (rsrc2).d))
/** Affecte à un registre la valeur booléenne vraie
 * (<tt>asbool(rdst)</tt> sera vrai) si \c rsrc1 est égal à \c rsrc2
 * (comparaison flottante).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define deq(rdst,rsrc1,rsrc2) ((rdst).d = ((rsrc1).d == (rsrc2).d))

/** Affecte à un registre le contenu du champ \c field de l’objet \c
 * obj
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc registre contenant l’adresse de l’objet
 * \param obj nom de la structure représentant l’objet
 * \param field nom du champ dans la structure */
#define agetfield(rdst,rsrc,obj,field) ((rdst) = (((struct obj*)((rsrc).a))->field))
/** Affecte à un champ \c field de l’objet \c obj le contenu d’un
 * registre
 *
 * \param rdst registre contenant l’adresse de l’objet
 * \param obj nom de la structure représentant l’objet
 * \param field nom du champ dans la structure
 * \param rval registre ou constante à écrire */
#define asetfield(rdst,obj,field,rval) ((((struct obj*)((rdst).a))->field) = (rval))

/** Interprète un registre comme booléen.
 *
 * À utiliser dans du code comme
 * \code
 * if(asbool(r1)) goto lbl1;
 * \endcode
 * quand le registre \c r1 contient une valeur booléenne */
#define asbool(r)     ((r).i != 0)

/** Affecte à un registre la négation booléenne (logique) d’un mot.
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc opérande (registre ou constante) */
#define lneg(rdst,rsrc)        ((rdst).i = !(rsrc).i)
/** Affecte à un registre le « ou » booléen (logique) de deux mots
 * (qui peuvent être des registres ou des constantes).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define lor(rdst,rsrc1,rsrc2)  ((rdst).i = ((rsrc1).i || (rsrc2).i))
/** Affecte à un registre le « et » booléen (logique) de deux mots
 * (qui peuvent être des registres ou des constantes).
 *
 * \param rdst registre dans lequel écrire le résultat
 * \param rsrc1,rsrc2 opérandes (registres ou constantes) */
#define land(rdst,rsrc1,rsrc2) ((rdst).i = ((rsrc1).i && (rsrc2).i))

/** Effectue un « appel de fonction », suppose que le retour sera
 * effectué via \c ret.
 *
 * Pour effectuer un appel de fonction, empile :
 *
 * - l’adresse de la prochaine instruction à effectuer quand on
 *   retournera de l’appel,
 * - un \a magic pour détecter des problèmes dans le respect de la
 *   convention d’appel
 * - la valeur actuelle de \c rbp
 *
 * puis modifie \c rbp pour qu’il pointe sur le haut courant de la
 * pile et saute à la première instruction de la fonction.
 *
 * \param f étiquette au début du code de la fonction appelée */
#define call(f)                             \
    do {                                    \
        __label__ __hack_return_ip__;       \
        push(aconst(&&__hack_return_ip__)); \
        push(STACK_MAGIC);                  \
        push(rbp);                          \
        rbp = rsp;                          \
        goto f;                             \
    __hack_return_ip__:                     \
        break;                              \
    } while(0)
/** Effectue un « retour d’appel de fonction », en supposant que
 * l’appel a suivi la convention de \c call.
 *
 * Pour effectuer un retour de fonction :
 *
 * - vérifie que toutes les valeurs qui auraient été empilées au cours
 *   de l’appel ont été dépilées (utilisez par exemple \c drop pour
 *   oublier rapidement les variables locales en fin de fonction),
 * - dépile \c rbp pour restaurer le cadre de pile de la fonction
 *   appelante,
 * - dépile le \a magic pour détecter un problème d’alignement,
 * - dépile l’adresse de retour,
 * - empile \a r (registre ou constante, la valeur retournée),
 * - saute à l’adresse de retour (donc dans le code de la fonction
 *   appelante).
 *
 * Une fonction retourne toujours exactement un mot.
 *
 * \param r registre ou constante qui est la valeur à retourner */
#define ret(r)                                    \
    assert(rbp.a == rsp.a);                       \
    pop(rbp);                                     \
    pop(__hack_register__);                       \
    assert(__hack_register__.i == STACK_MAGIC.i); \
    pop(__hack_register__);                       \
    push(r);                                      \
    goto *(__hack_register__.a)

/** Macro de débugage.
 *
 * Affiche un mot processeur à tous les types possibles. */
#define debug_reg(r)                 \
    printf("double:   %f\n"          \
           "long:     %ld\n"         \
           "unsigned: %lu\n"         \
           "address:  %p\n",         \
           (r).d,(r).i,(r).u,(r).a);

#endif
