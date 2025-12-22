# poc_mathia

Tentative de reproduction partielle de l'application MathIA.

## Objectif 

1. Créer un assistant pédagogique pour l'enseignement des mathématiques en primaire (cycle 2-3)
2. Développer l'application en utilisant différents modèles IA
3. Intégrer une fonctionnalité d'apprentissage adaptatif pour que le modèle adapte ses réponses

## Fonctionnalités clés

- Conversation de type textuelle : l'élève s'exprime à l'écrit et reçoit une réponse textuelle
- Echange oral : l'élève utilise le micro pour poser une question et peut recevoir une réponse textuelle ou audio
- Adaptative learning : création d'une logique adaptative (identification des erreurs-type de l'élève) pour avoir des réponses répondant au mieux aux besoin de l'élève
- Historisation : mise en place d'un suivi de l'élève en conservant sa progression et les difficultés rencontrés

## Stack

- Langage : Python
- IA : API Mistral (mistral-small-latest) / Azure Speech (traitement audio STT/TTS)
- Librairie : Streamlit (front)

## Adaptative Learning

Afin d'adapter au mieux les réponses du modèle, il est nécessaire de lui fournir les données qui lui permette d'identifier le niveau de l'élève.

Pour ce faire, l'application doit pouvoir mettre en place un système d'évaluation en fonction de l'apprentissage visé ; le point de départ est la notion abordée (calcul, problèmes, calcul mental...) et la classe de l'élève. A partir de ces informations, l'application peut proposer un exercice type sur lequel l'élève va travailler ou l'élève va expliciter ses difficultés. L'enjeu sera donc d'orienter le modèle sur les difficultés rencontrées, l'utilisation d'une logique d'apprentissage adaptatif rentre en jeu. Il consiste à fournir au modèle des informations sur le type de problème rencontré: en se basant sur les travaux de BROUSSEAU G. et FOUCHET-ISAMBARD, K. ET MILLON-FAURE, on fournit à l'application un ensemble de données qui explicite les erreurs-type. Chaque type d'erreur contient alors un ensemble d'informations spécifiques à une erreur données ; on fournit un exemple type ainsi qu'une remédiation.

### Cas des troubles "dys"

L'application devra fournir un contenu adaptatif en fonction des diverses pathologies de l'élève. 

## Etat actuel de l'application (22/12/2025)

L'implémentation de l'adaptative learning n'est pas encore fonctionnel ; il faut revoir la logique du traitement des informations par le LLM dans le sens où l'ordre d'appel des fonctions doit être revu :

Pour le moment, le LLM reçoit les inputs utilisateurs, respecte les instructions de base, utilise la fonction ```calculate``` pour gérer les calculs. Cependant, le système d'apprentissage adaptatif n'est pas utilisé et doit être intégré en amont de la génération de réponse.

## Axes d'améliorations

- Intégrer l'adaptative learning
- Créer des catégories d'exercices pour adapter au mieux le LLM aux réponses à fournir
- Tester la génération d'illustration et l'intégrer au POC
- Déploiement test

## Ressources

[LES ERREURS DES ÉLÈVES EN MATHÉMATIQUES - Guy Brousseau, 2001](https://irem.univ-grenoble-alpes.fr/medias/fichier/57x1_1561038496369-pdf)

[Personnalisation adaptative de problèmes
mathématiques arithmétiques pour élèves de CM1-CM2
à l’aide de grands modèles de langue via ingénierie de
prompt. - Ousseynou Gueye, 2025](https://theses.hal.science/tel-05219692/file/2024PA100106.pdf)

[ÉLABORATION D’UNE TYPOLOGIE DES ERREURS EN MATHEMATIQUES POUR CONCEVOIR DES FEEDBACKS ADAPTATIFS - FOUCHET-ISAMBARD, K. ET MILLON-FAURE, 2025](https://hal.science/hal-05361521v1/document)
