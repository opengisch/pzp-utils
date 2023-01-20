from collections import OrderedDict

PROPAGATION_PROBABILITIES = OrderedDict(
    {
        1001: "Bassa",
        1002: "Media",
        1003: "Alta",
    }
)

EVENT_PROBABILITIES = OrderedDict(
    {
        1000: "Molto bassa",
        1001: "Bassa",
        1002: "Media",
        1003: "Alta",
    }
)


INTENSITIES = OrderedDict(
    {
        1000: "Nessun impatto",
        1001: "Impatto presente",
        1002: "Debole",
        1003: "Medio",
        1004: "Forte",
    }
)

DANGER_TYPES = OrderedDict(
    {
        1000: "Non in pericolo",
        1001: "Pericolo residuo",  # Light yellow
        1002: "Basso",  # Yellow
        1003: "Medio",  # Blue
        1004: "Elevato",  # Red
    }
)

DANGER_LEVELS = OrderedDict(
    {
        1000: 0,
        1001: 9,
        1002: 8,
        1003: 7,
        1004: 6,
        1005: 5,
        1006: 4,
        1007: 3,
        1008: 2,
        1009: 1,
        1010: -10,
    }
)

PROCESS_TYPES = OrderedDict(
    {
        1110: "Alluvionamento corso d'acqua minore",
        1120: "Alluvionamento corso d'acqua principale",
        1200: "Flusso detrito",
        1400: "Ruscellamento superficiale",
        2001: "Scivolamento spontaneo",
        2002: "Colata detritica di versante",
        3000: "Caduta sassi o blocchi",
        4100: "Valanga radente",
        4200: "Valanga polverosa",
    }
)

MATRICES = {
    1110: [  # Alluvionamento Corso d'acqua minore
        1002,  # Intensità
        30,  # Periodo di ritorno
        3,  # Valore nella matrice
        1003,  # Pericolo
        1002,
        100,
        2,
        1002,
        1002,
        300,
        1,
        1002,
        1002,
        99999,
        -10,
        1001,
        1003,
        30,
        6,
        1003,
        1003,
        100,
        5,
        1003,
        1003,
        300,
        4,
        1003,
        1003,
        99999,
        -10,
        1001,
        1004,
        30,
        9,
        1004,
        1004,
        100,
        8,
        1004,
        1004,
        300,
        7,
        1004,
        1004,
        99999,
        -10,
        1001,
        1000,
        99999,
        -10,
        1000,
    ],
    1120: [  # Alluvionamento Corso d'acqua principale
        1002,
        30,
        3,
        1003,
        1002,
        100,
        2,
        1002,
        1002,
        300,
        1,
        1002,
        1002,
        99999,
        -10,
        1001,
        1003,
        30,
        6,
        1003,
        1003,
        100,
        5,
        1003,
        1003,
        300,
        4,
        1003,
        1003,
        99999,
        -10,
        1001,
        1004,
        30,
        9,
        1004,
        1004,
        100,
        8,
        1004,
        1004,
        300,
        7,
        1004,
        1004,
        99999,
        -10,
        1001,
        1000,
        99999,
        -10,
        1000,
    ],
    1200: [  # Flusso detrito
        1002,
        30,
        3,
        1003,
        1002,
        100,
        2,
        1002,
        1002,
        300,
        1,
        1002,
        1002,
        99999,
        -10,
        1001,
        1003,
        30,
        6,
        1003,
        1003,
        100,
        5,
        1003,
        1003,
        300,
        4,
        1003,
        1003,
        99999,
        -10,
        1001,
        1004,
        30,
        9,
        1004,
        1004,
        100,
        8,
        1004,
        1004,
        300,
        7,
        1004,
        1004,
        99999,
        -10,
        1001,
        1000,
        99999,
        -10,
        1000,
    ],
    1400: [  # Ruscellamento superficiale
        1002,
        30,
        3,
        1003,
        1002,
        100,
        2,
        1002,
        1002,
        300,
        1,
        1002,
        1002,
        99999,
        -10,
        1001,
        1003,
        30,
        6,
        1003,
        1003,
        100,
        5,
        1003,
        1003,
        300,
        4,
        1003,
        1003,
        99999,
        -10,
        1001,
        1004,
        30,
        9,
        1004,
        1004,
        100,
        8,
        1004,
        1004,
        300,
        7,
        1004,
        1004,
        99999,
        -10,
        1001,
        1000,
        99999,
        -10,
        1000,
    ],
    2001: [  # Scivolamento spontaneo
        1002,
        30,
        3,
        1002,
        1002,
        100,
        2,
        1002,
        1002,
        300,
        1,
        1002,
        1002,
        99999,
        -10,
        1001,
        1003,
        30,
        6,
        1003,
        1003,
        100,
        5,
        1002,
        1003,
        300,
        4,
        1002,
        1003,
        99999,
        -10,
        1001,
        1004,
        30,
        9,
        1004,
        1004,
        100,
        8,
        1004,
        1004,
        300,
        7,
        1003,
        1004,
        99999,
        -10,
        1001,
        1000,
        99999,
        -10,
        1000,
    ],
    2002: [  # Colata detritica
        1002,
        30,
        3,
        1002,
        1002,
        100,
        2,
        1002,
        1002,
        300,
        1,
        1002,
        1002,
        99999,
        -10,
        1001,
        1003,
        30,
        6,
        1003,
        1003,
        100,
        5,
        1002,
        1003,
        300,
        4,
        1002,
        1003,
        99999,
        -10,
        1001,
        1004,
        30,
        9,
        1004,
        1004,
        100,
        8,
        1004,
        1004,
        300,
        7,
        1003,
        1004,
        99999,
        -10,
        1001,
        1000,
        99999,
        -10,
        1000,
    ],
    3000: [  # Caduta sassi
        1002,
        30,
        3,
        1003,
        1002,
        100,
        2,
        1002,
        1002,
        300,
        1,
        1002,
        1002,
        99999,
        -10,
        1001,
        1003,
        30,
        6,
        1003,
        1003,
        100,
        5,
        1003,
        1003,
        300,
        4,
        1002,
        1003,
        99999,
        -10,
        1001,
        1004,
        30,
        9,
        1004,
        1004,
        100,
        8,
        1004,
        1004,
        300,
        7,
        1004,
        1004,
        99999,
        -10,
        1001,
        1000,
        99999,
        -10,
        1000,
    ],
    4100: [  # Valanga radente
        1002,
        30,
        3,
        1004,
        1002,
        300,
        2,
        1003,
        1003,
        30,
        6,
        1004,
        1003,
        100,
        5,
        1003,
        1004,
        30,
        9,
        1004,
        1004,
        100,
        8,
        1004,
        1000,
        99999,
        -10,
        1000,
    ],
    4200: [  # Valanga polverosa
        1002,
        30,
        3,
        1003,
        1002,
        300,
        2,
        1002,
        1003,
        30,
        6,
        1004,
        1003,
        100,
        5,
        1003,
        1004,
        30,
        9,
        1004,
        1004,
        100,
        8,
        1004,
        1000,
        99999,
        -10,
        1000,
    ],
}
