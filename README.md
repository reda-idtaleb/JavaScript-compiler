#   Projet de compilation

## Binome:
 Manal LAGHMICH - Réda ID-TALEB

# Pretty-printer
## Remarque importante

Nous avions commencé le projet sur deux dépots différents, la partie pretty-printer a été réalisée dans deux dépots différents avant de l'intégrer dans le dépot actuel. 

Afin de trouver la trace des commits réalisés pendant la première semaine(sur les anciens dépots) voici les liens des dépots:
- dépot Manal LAGHMICH : https://gitlab.univ-lille.fr/manal.laghmich.etu/projet-compil
- dépot Reda ID-TALEB : https://gitlab.univ-lille.fr/reda.idtaleb.etu/compilation-project

## Execution
Placez vous à la racine(là où se situe le /src) et passer la commande suivante:
```bash
$ make pprinter
```
Ensuite vous aurez un affichage qui vous indique de saisir un fichier parmi ceux qui sont affichés. 
Vous copier/coller le nom du fichier(avec le numéro) et confirmez votre choix.

**Note: Le numérotage des fichiers font parti du nom des fichiers**

## Quelle partie du langage couverte
- Les expressions(y compris les expressions vicieuses):
    - expression binaires.
    - expression d'affectations.
    - expression logiques.
    - expression de mise à jour.
    - expression unaire.
    - expression d'appels.
    - expression de membres(a[b] ou a.b).
    - expression d'objets.
    - expression this.
    - expression new.
- Les declarations de variables. 
- Les boucles for/while(y compris les boucles imbriquées).
- Les conditions(y compris les condtions imbriquées).
- Le switch.
- Le switch contenant les instructions break ou/et continue.
- While contenant les instructions 'break' ou/et 'continue'.
- Appel aux fonctions(y compris le cas où nous avons une fonction contenant une fonction imbriquée).
- Les fonctions 'classiques'.
- Les fonctions récursives.
- Les fonctions imbriquées.
- Les instanciations via le mot clé 'new'.
- Instruction return.
- Spread elements.
- Les littéreaux:
    - littéreaux numériques.
    - littéreaux null.
    - littéreaux de type string.
    - littéreaux de type booléan.
## Les choix effectués
- Afin que le pretty-printer ne soit pas restreint qu'aux exemples fournis, l'outil s'appuit largement sur la grammaire définit dans la spécification du Babel. En effet, l'outil devient plus générique et permet d'analyser plus d'exemples de code.
- Pour les conditions nous produisons pas la même structure(le shéma) que celui du code source mais plutôt un shéma qui lui est équivalent. La prodution n'est pas la même dans le cas où nous avons un shéma de conditions avec des 'else if'.

Par exemple, considérons le shéma suivant:
```bash
if(exp1){
    instr1;
}
else if(exp2){
    instr2;
}
else{
   instr3; 
}
```
On produit le résultat suivant:
```bash
if(exp){
    instr1;
}
else{
    if(exp2){
        instr2;
    }
    else{
        instr3; 
    }
}
```
En effet, si une condition n'est pas évaluée alors le champs 'alternate' est executée, qui est lui même une instruction de condition donc on interprète cela comme le cas contraire de la première condition. 
## Etat d'avancement de l'outil 

L'outil à présent couvre tous les exemples fournis dans le dépôt de l'énoncé. En plus, des exemples suplémentaires ont été ajouté:
- Le cas des conditions imbriqués
- Le cas des boucles(while et for) imbriqués
## Tests effectués
Le pretty printer fonctionne sur tous les exemples qui sont fournis.

# Interprète

## Execution
Placez vous à la racine(là où se situe le /src) et passer la commande suivante:
```bash
$ make interpreter
```
Ensuite vous aurez un affichage qui vous indique de saisir un fichier parmi ceux qui sont affichés. 
Vous copier/coller le nom du fichier(avec le numéro) et confirmez votre choix.

**Note: Le numérotage des fichiers font parti du nom des fichiers**

## Quelle partie du langage couverte
- les expressions arithmétiques 
- les déclarations de variables 
- l’appel de la fonction print
- les expressions booléennes
- les instructions conditionnelles : if
- les boucles while et for (simples et imbriquées)
- les déclarations de fonction
- les appels de fonctions
- les fonctions récursives
- les objets JS

## Les choix effectués
- Pour les déclarations de variables, un dictionnaire ("globalVariables") a été mis en place pour stocker la valeur d'un identifieur. Le dictionnaire a pour clé: le nom de l'identifieur et comme clé sa valeur.
- Nous avons définit l'appel à la fonction Print, comme un cas particulier des appels aux fonctions. Pour ce cas spécifique, l'entrée de la fonction est calculée et affichée. Pour le cas des identifieurs, on affiche leur valeur.
- Pour les déclarations des fonctions, Nous associons le nom de la fonction avec ses paramètres ainsi que son corps dans un dictionnaire que nous avons appelé "functions".
- Au moment de l'appel de la fonction, Nous associons les paramètres de la fonctions avec leurs valeurs dans un dictionnaire appelé "paramsValues", lors de l'exécution de la fonction, Pour récupérer les valeurs des identifieurs, nous vérifions d'abord si'il est présent dans le dictionnaire "paramsValues",sinon nous vérifions si'il est présent dans le dictionnaire des variables locales et si'il n'est présent dans aucun des deux, nous récupérons sa valeur dans le dictionnaires des variables globales. Dans le cas où sa valeur n'est présente dans aucun des trois dictionnaire, nous levons une exception ("Undefined variable").
- Pour les fonctions récursives, nous avons utilisé une pile qui contient les appels de la fonction. Chaque appel de fonction est défini par : la valeur de retour de de la fonction et un boolean "isFinished" qui définit si c'est le dernier appel (si on a atteint le cas de base). Quand on atteint le cas de base et on obtient une valeur de retour, on met le champs "isFinished" de cet appel à vrai. Lors d'un appel de fonction, on vérifie si le dernier appel ajouté à la pile est le dernier (cas de base) et on retourne sa valeur.

## Les tests

l'interprète couvre les exemples suivants fournis dans le dépôt de l'énoncé:
- 01-expressions
- 02-declarations
- 03-while
- 04-if-while
- 05-fors
- 11-func-compact
- 12-fact-compact
- 14-obj-compact

En plus, des exemples suplémentaires ont été ajouté:
- 21-if-elseif : Le cas des conditions imbriqués
- 22-while-imbrique : Le cas des boucles while imbriquées
- 23-fors-imbrique : Le cas des boucles for imbriquées
- 24-declarations-integers et 29-variables+expressions : Déclarations des variables
- 25-glob-loc-arg : Pour tester l'appel d'une variable globale au sein d'une fonction
- 26-parametres-fonction : Pour vérifier si les valeurs des paramètres des fonctions se réinitialisent après l'éxécution de la fonction
- 27-variables-expressions : Déclarations des variables
- 28-appels-fonctions-recursive : Pour vérifier si les valeurs les valeurs du dictionnaire des appels de fonction se réinitialisent après l'éxécution de la fonction
- 29-variables-locales-fonctions: Pour vérifier si les valeurs des variable locales des fonctions se réinitialisent après l'éxécution de la fonction

# Compilateur

## Execution
Placez vous à la racine(là où se situe le /src) et passer la commande suivante:
```bash
$ make compilation
```
Ensuite vous aurez un affichage qui vous indique de saisir un fichier parmi ceux qui sont affichés. 
Vous copier/coller le nom du fichier(avec le numéro) et confirmez votre choix.

**Note: Le numérotage des fichiers font parti du nom des fichiers**

Enfin, le programme vous indique qu'un fichier nommé code_translated.c est bien généré et ajouté au dossier c-asm/code_translated.c

Vous pouvez executer ce programme en vous plaçant dans le dossier /c-asm :

Tout d'abord, compilez les sources avec make: 
```bash
$ make
```
Un executable nommé code_translated est normalement généré.

Executez dans le même dossier cette commande:
```bash
$ ./code_translated
```


## Quelle partie du langage couverte
Nous avons couvert:
- Les expressions:
    - expression binaires.
    - expression d'affectations.
    - expression logiques.
    - expression de mise à jour.
    - expression unaire.
    - expression d'appels.
- Les declarations de variables. 
- Les boucles for/while(y compris les boucles imbriquées).
- Les conditions(y compris les condtions imbriquées).
- While contenant les instructions 'break' ou/et 'continue'.
- Appel aux fonctions.
- Les fonctions 'classiques'(non imbriquées).
- Les fonctions récursives.
- Instruction return.
- Les littéreaux:
    - littéreaux numériques.
    - littéreaux null.

## Les choix effectués
- Utilisation d'une pile pour les déclarations de fonctions. 
- Utilisation d'un dictionnaire pour représenter les variables locales. Les clés sont les noms des variables et les valeurs sont leurs indices dans la base pointer qui commencent à -1.
- Utilisation d'un dictionnaire pour les paramètre d'une fonction. Les clés sont les noms des varaibles et les valeurs sont leurs indice dans le base pointer qui commancent à 3.
- Utilisation d'un dictionnaire pour les variables globales. Les clés sont sont les noms des variables et les valeurs sont leurs indices dans le tableau globals.
- Pour le cas des fonctions d'affichages(comme print()) nous avons utilisé des debug_reg() pour afficher le contenu de son paramètre.

## Etats d'avancement de l'outil
Nosu avons eu des difficultés au niveau des fonctions spécifiquement avec les déclarations des labels. 
Pour les optimisations: une grande diffuclté avec les fonctions imbriquées que nous avons pas réussi. Le principal problème est comment récupèrer l'adresse de la fonction dans le cas des fonction d'ordre supérieur?

## Test effectués
Voici les exemples qui fonctionnent avec notre compilateur: 
Ces exemples sont dans src/compilation/examples
```bash
01-expressions-compact.json            11-func-compact.json                   25-glob-loc-arg-compact.json  
02-declarations-integers-compact.json  12-fact-compact.json                   
03-while-compact.json                  21-if-elseif.json                      
04-if-while-compact.json               22-while-imbrique-compact.json         
05-fors-compact.json                   23-variables-expressions-compact.json  
06-while-break-compact.json            23-fors-imbrique-compact.json 
```