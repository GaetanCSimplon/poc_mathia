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

## Ressources

[LES ERREURS DES ÉLÈVES EN MATHÉMATIQUES - Guy Brousseau, 2001](https://irem.univ-grenoble-alpes.fr/medias/fichier/57x1_1561038496369-pdf)

[Personnalisation adaptative de problèmes
mathématiques arithmétiques pour élèves de CM1-CM2
à l’aide de grands modèles de langue via ingénierie de
prompt. - Ousseynou Gueye, 2025](https://theses.hal.science/tel-05219692/file/2024PA100106.pdf)
