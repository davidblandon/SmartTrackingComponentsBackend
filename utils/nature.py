from enum import Enum

class NatureEnum(str, Enum):
    BMS = "BMS"
    VCU = "VCU"
    DC_dc = "DC/dc"
    Chargeur = "Chargeur"
    Boite_de_jonction = "Boite de jonction"
    Module_de_batterie = "Module de batterie"
    Groupe_moteur_onduleur = "Groupe moteur-onduleur"
    moteur = "moteur"
    Onduleur = "Onduleur"

