#   Exemples

Ce dépôt contient de petits exemples de code source sur lesquels
tester votre code. Ces petits exemples de « programmes » en syntaxe
JavaScript sont dans le répertoire `src`. Les numéros des exemples
proposent un ordre dans lequel ajouter les constructions du langage
dans vos outils.

`src` contient également un `Makefile` utilisant les outils `babylon`
et `jq` :

-   pour chaque source `*.js`, le `Makefile` permet de générer son AST
    `*.json` en utilisant `babylon`,
-   pour chaque AST `*.json`, le `Makefile` permet aussi de générer
    une version « compacte » `*-compact.json` en supprimant plein
    d’informations qui ne seront pas utiles pour nos projets.

`parser` contient une page web simple qui permet d’utiliser le parser
de babel directement dans un navigateur si vous ne voulez pas ou ne
pouvez pas installer simplement babylon / babel-parser. Il contient un
`Makefile` pour charger la dernière version de `babel.js`.
