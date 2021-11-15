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

### Version *basic* ###

Seule la publication non filtrée, c'est-à-dire systématique, est implémentée et il n'y a donc pas de publication de la liste des topics à la souscription.

### Version *optimized* ###

Si on souhaite optimiser l'activité réseau, on devra conditionner l'émission à l'existance d'un consommateur : chaque noeud doit connaître toutes les souscriptions.

La méthode `JSonBus.subscribe()` diffuse un message contenant la liste des souscriptions (*meta-données*).

Quand un participant rejoint le bus tardivement, il démarre avec une liste de topics qui ne contient que les siens, il doit donc être mis à jour par les autres participants qui reconnaissent cette situation en comparant leur liste à celle reçue, si elle est plus complète, elle doit être émise.

Afin d'éviter que tous les participants ne répondent bruyamment, l'un d'entre eux - le premier lancé - est désigné par une option de ligne de commande : `--master`.