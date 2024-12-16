#!/bin/sh
# invoke-uki-profilify.sh: to be installed as a mkinitcpio post hook

# invoke `uki-profilify` in automatic mode after mkinitcpio generation
uki-profilify -a $1 $2
