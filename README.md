# JSonBus #

## Principes ##

Il s'agit d'un bus décentralisé utilisant `UDP/IP Multicast` (UDPM) pour s'abonner et publier.

Au dessus de la couche UDPM, un service d'abonnement logique est proposé selon le principe *Publish-Subscribe*.

Le sujet de l'abonnement logique, le *topic* est une clef unique.

La donnée véhiculée par le bus est indexée par la clef.

Pour réaliser l'encodage et le décodage, le format `JSON` est utilisé.
Le type exact d'une donnée associée à un topic peut donc varier dans le temps, en fonction des écrivains.

La cohérence globale à la fois en terme de types et de valeurs est totalement à la charge des applicatifs, ce bus n'assure que le transfert de données opaques.
Une bonne pratique consiste à bannir les écrivains concurrents.
Ainsi, si la cohérence des données locales est garantie, la cohérence globale le sera également, sous réserve que les données soient
indépendantes.

## Conception globale ##

D'un point de vue purement fonctionnel, la base des souscriptions de chaque noeud du réseau n'a pas besoin d'être partagée car le filtrage s'effectue du côté consommateur mais au prix de publications inutiles quand il n'existe pas de souscripteur.

Si on souhaite optimiser l'activité réseau, on devra conditionner l'émission à l'existence d'un consommateur : chaque noeud doit connaître toutes les souscriptions qui devront être publiées à chaque souscription.

Quand un participant rejoint le bus tardivement, il démarre avec une liste de topics qui ne contient que les siens, il doit donc être mis à jour par les autres participants qui reconnaissent cette situation en comparant leur liste à celle reçue et si cette dernière est plus complète, elle doit être émise.

### Version *basic* ###

Seule la publication non filtrée, c'est-à-dire systématique, est implémentée et il n'y a donc pas de publication de la liste des topics à la souscription. Des publications sans souscripteur transitent sur le réseau.

### Version *master* ###

Les souscriptions sont partagées. Afin d'éviter que tous les participants ne répondent bruyamment, l'un d'entre eux - le premier lancé - est désigné par une option de ligne de commande : `--master`. Ce comportement est déterministe mais présente toutefois l'inconvénient de violer la décentralisation, puisqu'un seul acteur possède un rôle unique, il s'agit d'un *SPOF*.

### Version *delayed* ###

Les souscriptions sont partagées. Sur réception de la liste des souscriptions et si celle-ci est différente de celle connue localement, chaque participant arme un réveil de durée **aléatoire**, faible (de 0 à 200 ms) dont l'expiration provoque la publication de toutes les souscriptions connues (action différée).

Sur réception d'une liste de souscriptions identique à celle connue localement, le participant annule son action différée.

Cette version conserve le caractère décentralisé, exempt de *SPOF* mais au prix d'une perte de déterminisme.

Une variante déterministe consiste à affecter à chaque participant une valeur fixe du réveil, par construction.
Ainsi, on garantit le déterminisme, y compris quand un noeud disparaît, c'est l'objet de l'argument en ligne de commande optionnel **--subs-share-delay nn**.
