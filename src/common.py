import enum

class Server:
    class Order(enum.IntEnum):
        RESET       = 0
        ACTION      = 1
        GAME_SETUP  = 2

class GameSetup:
    class MainMenu(enum.IntEnum):
        SINGLE_PLAYER   = 0
        MULTIPLAYER     = 1
        ONLINE_PLAY     = 2
        WIRELESS_PLAY   = 3

    class GameMode(enum.IntEnum):
        GRAND_PRIX  = 0
        TIME_TRIALS = 1
        VS_RACE     = 2
        BATTLE      = 3

    class RaceRule:
        class Mode(enum.IntEnum):
            CC_50   = 0
            CC_100  = 1
            CC_150  = 2
            MIRROR  = 3
            CC_200  = 4
        class Teams(enum.IntEnum):
            NO_TEAMS    = 1
            TEAM_GAME   = 2
        class Items(enum.IntEnum):
            NORMAL_ITEMS        = 1
            SHELLS_ONLY         = 2
            BANANAS_ONLY        = 3
            MUSHROOMS_ONLY      = 4
            BOBOMBS_ONLY        = 5
            NO_ITEMS            = 6
            NO_ITEMS_OR_COINS   = 7
            FRANTIC_ITEMS       = 8
        class COM(enum.IntEnum):
            EASY    = 1
            NORMAL  = 2
            HARD    = 3
        class COMVehicles(enum.IntEnum):
            ALL         = 1
            KARTS_ONLY  = 2
            BIKES_ONLY  = 3
        class Courses(enum.IntEnum):
            CHOOSE      = 0
            IN_ORDER    = 1
            RANDOM      = 2
        class RaceCount(enum.IntEnum):
            FOUR        = 0
            SIX         = 1
            EIGHT       = 2
            TWELVE      = 3
            SIXTEEN     = 4
            TWENTY_FOUR = 5
            THIRTY_TWO  = 6
            FORTY_EIGHT = 7

    class Course:
        class Cup:
            class Mushroom(enum.IntEnum):
                MARIO_KART_STADIUM  = 12
                WATER_PARK          = 13
                SWEET_SWEET_CANYON  = 14
                THWOMP_RUINS        = 15
            class Flower(enum.IntEnum):
                MARIO_CIRCUIT   = 12
                TOAD_HARBOR     = 13
                TWISTED_MANSION = 14
                SHY_GUY_FALLS   = 15
            class Star(enum.IntEnum):
                SUNSHINE_AIRPORT    = 12
                DOLPHIN_SHOALS      = 13
                ELECTRODOME         = 14
                MOUNT_WARIO         = 15
            class Special(enum.IntEnum):
                CLOUDTOP_CRUISE = 12
                BONEDRY_DUNES   = 13
                BOWSERS_CASTLE  = 14
                RAINBOW_ROAD    = 15
            class Egg(enum.IntEnum):
                YOSHI_CIRCUIT       = 12
                EXCITEBIKE_ARENA    = 13
                DRAGON_DRIFTWAY     = 14
                MUTE_CITY           = 15
            class Crossing(enum.IntEnum):
                BABY_PARK       = 12
                CHEESE_LAND     = 13
                WILD_WOODS      = 14
                ANIMAL_CROSSING = 15
            class Shell(enum.IntEnum):
                MOO_MOO_MEADOWS     = 12
                MARIO_CIRCUIT       = 13
                CHEEP_CHEEP_BEACH   = 14
                TOADS_TURNPIKE      = 15
            class Banana(enum.IntEnum):
                DRY_DRY_DESERT  = 12
                DONUT_PLAINS_3  = 13
                ROYAL_RACEWAY   = 14
                DK_JUNGLE       = 15
            class Leaf(enum.IntEnum):
                WARIO_STADUIM   = 12
                SHERBET_LAND    = 13
                MUSIC_PARK      = 14
                YOSHI_VALLEY    = 15
            class Lightning(enum.IntEnum):
                TICKTOCK_CLOCK      = 12
                PIRANHA_PLANT_SLIDE = 13
                GRUMBLE_VOLCANO     = 14
                RAINBOW_ROAD        = 15
            class Triforce(enum.IntEnum):
                WARIOS_GOLD_MINE    = 12
                RAINBOW_ROAD        = 13
                ICE_ICE_OUTPOST     = 14
                HYRULE_CIRCUIT      = 15
            class Bell(enum.IntEnum):
                NEO_BOWSER_CITY     = 12
                RIBBON_ROAD         = 13
                SUPER_BELL_SUBWAY   = 14
                BIG_BLUE            = 15
            MUSHROOM    = 0
            FLOWER      = 1
            STAR        = 2
            SPECIAL     = 3
            EGG         = 4
            CROSSING    = 5
            SHELL       = 6
            BANANA      = 7
            LEAF        = 8
            LIGHTNING   = 9
            TRIFORCE    = 10
            BELL        = 11

    class Player:
        class YoshiVariant(enum.IntEnum):
            DEFAULT     = 0
            LIGHT_BLUE  = 1
            BLACK       = 2
            RED         = 3
            YELLOW      = 4
            WHITE       = 5
            BLUE        = 6
            PINK        = 7
            ORANGE      = 8
        class MaskassVariant(enum.IntEnum):
            DEFAULT     = 0
            LIGHT_BLUE  = 1
            BLACK       = 2
            GREEN       = 3
            YELLOW      = 4
            WHITE       = 5
            BLUE        = 6
            PINK        = 7
            ORANGE      = 8
        class InklingGirlVariant(enum.IntEnum):
            DEFAULT     = 0
            VARIANT_1   = 1
            VARIANT_2   = 2
        class InklingBoyVariant(enum.IntEnum):
            DEFAULT     = 0
            VARIANT_1   = 1
            VARIANT_2   = 2
        class LinkVariant(enum.IntEnum):
            DEFAULT     = 0
            VARIANT_1   = 1
        MARIO           = 0
        LUIGI           = 1
        PEACH           = 2
        DAISY           = 3
        ROSALINA        = 4
        TANOOKI_MARIO   = 5
        CAT_PEACH       = 6
        YOSHI           = 7
        TOAD            = 8
        KOOPA_TROOPA    = 9
        MASKASS         = 10
        LAKITU          = 11
        TOADETTE        = 12
        KING_BOO        = 13
        BABY_MARIO      = 14
        BABY_LUIGI      = 15
        BABY_PEACH      = 16
        BABY_DAISY      = 17
        BABY_ROSALINA   = 18
        METAL_MARIO     = 19
        PINK_GOLD_PEACH = 20
        WARIO           = 21
        WALUIGI         = 22
        DONKEY_KONG     = 23
        BOWSER          = 24
        DRY_BONES       = 25
        BOWSER_JR       = 26
        DRY_BOWSER      = 27
        LEMMY           = 28
        LARRY           = 29
        WENDY           = 30
        LUDWIG          = 31
        IGGY            = 32
        ROY             = 33
        MORTON          = 34
        INKLING_GIRL    = 35
        INKLING_BOY     = 36
        LINK            = 37
        VILLAGER        = 38
        VILLAGER_ALT    = 39
        ISABELLE        = 40

    class Car:
        class Body(enum.IntEnum):
            STANDARD_KART       = 0
            PIPE_FRAME          = 1
            MACH_8              = 2
            STEEL_DRIVER        = 3
            CAT_CRUISER         = 4
            CIRCUIT_SPECIAL     = 5
            TRISPEEDER          = 6
            BADWAGON            = 7
            PRANCER             = 8
            BIDDYBUGGY          = 9
            LANDSHIP            = 10
            SNEEKER             = 11
            SPORT_COUPE         = 12
            GOLD_STANDARD       = 13
            AD_GLA              = 14
            AD_SILVER_ARROW     = 15
            AD_ROADSTER         = 16
            BLUE_FALCON         = 17
            TANOOKI_KART        = 18
            B_DASHER            = 19
            STREETLE            = 20
            P_WING              = 21
            KOOPA_CLOWN         = 22
            STANDARD_BIKE       = 23
            COMET               = 24
            SPORT_BIKE          = 25
            THE_DUKE            = 26
            FLAME_RIDER         = 27
            VARMINT             = 28
            MR_SCOOTER          = 29
            JET_BIKE            = 30
            YOSHI_BIKE          = 31
            MASTER_CYCLE        = 32
            MASTER_CYCLE_ZERO   = 33
            CITY_TRIPPER        = 34
            STANDARD_ATV        = 35
            WILD_WIGGLER        = 36
            TEDDY_BUGGY         = 37
            BONE_RATTLER        = 38
            SPLAT_BUGGY         = 39
            INKSTRIKER          = 40
        class Wheel(enum.IntEnum):
            STANDARD        = 0
            MONSTER         = 1
            ROLLER          = 2
            SLIM            = 3
            SLICK           = 4
            METAL           = 5
            BUTTON          = 6
            OFF_ROAD        = 7
            SPONGE          = 8
            WOOD            = 9
            CUSHION         = 10
            BLUE_STANDARD   = 11
            HOT_MONSTER     = 12
            AZURE_ROLLER    = 13
            CRIMSON_SLIM    = 14
            CYBER_SLICK     = 15
            RETRO_OFFROAD   = 16
            AD_GLA_TIRES    = 17
            TRIFORCE_TIRES  = 18
            ANCIENT_TIRES   = 19
            LEAF_TIRES      = 20
        class Wing(enum.IntEnum):
            SUPER_GLIDER    = 0
            CLOUD_GLIDER    = 1
            WARIO_WING      = 2
            WADDLE_WING     = 3
            PEACH_PARASOL   = 4
            PARACHUTE       = 5
            PARAFOIL        = 6
            FLOWER_GLIDER   = 7
            BOWSER_KITE     = 8
            PLANE_GLIDER    = 9
            MKTV_PARAFOIL   = 10
            HYLIAN_KITE     = 11
            PARAGILDER      = 12
            PAPER_GLIDER    = 13

class Track(enum.Enum):
    Mushroom_MARIO_KART_STADIUM = enum.auto()
    Mushroom_WATER_PARK = enum.auto()
    Mushroom_SWEET_SWEET_CANYON = enum.auto()
    Mushroom_THWOMP_RUINS = enum.auto()
    Flower_MARIO_CIRCUIT = enum.auto()
    Flower_TOAD_HARBOR = enum.auto()
    Flower_TWISTED_MANSION = enum.auto()
    Flower_SHY_GUY_FALLS = enum.auto()
    Star_SUNSHINE_AIRPORT = enum.auto()
    Star_DOLPHIN_SHOALS = enum.auto()
    Star_ELECTRODOME = enum.auto()
    Star_MOUNT_WARIO = enum.auto()
    Special_CLOUDTOP_CRUISE = enum.auto()
    Special_BONEDRY_DUNES = enum.auto()
    Special_BOWSERS_CASTLE = enum.auto()
    Special_RAINBOW_ROAD = enum.auto()
    Egg_YOSHI_CIRCUIT = enum.auto()
    Egg_EXCITEBIKE_ARENA = enum.auto()
    Egg_DRAGON_DRIFTWAY = enum.auto()
    Egg_MUTE_CITY = enum.auto()
    Crossing_BABY_PARK = enum.auto()
    Crossing_CHEESE_LAND = enum.auto()
    Crossing_WILD_WOODS = enum.auto()
    Crossing_ANIMAL_CROSSING = enum.auto()
    Shell_MOO_MOO_MEADOWS = enum.auto()
    Shell_MARIO_CIRCUIT = enum.auto()
    Shell_CHEEP_CHEEP_BEACH = enum.auto()
    Shell_TOADS_TURNPIKE = enum.auto()
    Banana_DRY_DRY_DESERT = enum.auto()
    Banana_DONUT_PLAINS_3 = enum.auto()
    Banana_ROYAL_RACEWAY = enum.auto()
    Banana_DK_JUNGLE = enum.auto()
    Leaf_WARIO_STADUIM = enum.auto()
    Leaf_SHERBET_LAND = enum.auto()
    Leaf_MUSIC_PARK = enum.auto()
    Leaf_YOSHI_VALLEY = enum.auto()
    Lightning_TICKTOCK_CLOCK = enum.auto()
    Lightning_PIRANHA_PLANT_SLIDE = enum.auto()
    Lightning_GRUMBLE_VOLCANO = enum.auto()
    Lightning_RAINBOW_ROAD = enum.auto()
    Triforce_WARIOS_GOLD_MINE = enum.auto()
    Triforce_RAINBOW_ROAD = enum.auto()
    Triforce_ICE_ICE_OUTPOST = enum.auto()
    Triforce_HYRULE_CIRCUIT = enum.auto()
    Bell_NEO_BOWSER_CITY = enum.auto()
    Bell_RIBBON_ROAD = enum.auto()
    Bell_SUPER_BELL_SUBWAY = enum.auto()
    Bell_BIG_BLUE = enum.auto()


INTERNAL_TRACK_TO_ENUM = {
    1401: Track.Mushroom_MARIO_KART_STADIUM,
    1402: Track.Mushroom_WATER_PARK,
    1403: Track.Mushroom_SWEET_SWEET_CANYON,
    1404: Track.Mushroom_THWOMP_RUINS,
    1406: Track.Flower_MARIO_CIRCUIT,
    1405: Track.Flower_TOAD_HARBOR,
    1408: Track.Flower_TWISTED_MANSION,
    1411: Track.Flower_SHY_GUY_FALLS,
    1409: Track.Star_SUNSHINE_AIRPORT,
    1410: Track.Star_DOLPHIN_SHOALS,
    1407: Track.Star_ELECTRODOME,
    1412: Track.Star_MOUNT_WARIO,
    1414: Track.Special_CLOUDTOP_CRUISE,
    1413: Track.Special_BONEDRY_DUNES,
    1415: Track.Special_BOWSERS_CASTLE,
    1416: Track.Special_RAINBOW_ROAD,
    1485: Track.Egg_YOSHI_CIRCUIT,
    1482: Track.Egg_EXCITEBIKE_ARENA,
    1483: Track.Egg_DRAGON_DRIFTWAY,
    1484: Track.Egg_MUTE_CITY,
    1490: Track.Crossing_BABY_PARK,
    1489: Track.Crossing_CHEESE_LAND,
    1491: Track.Crossing_WILD_WOODS,
    1492: Track.Crossing_ANIMAL_CROSSING,
    1441: Track.Shell_MOO_MOO_MEADOWS,
    1442: Track.Shell_MARIO_CIRCUIT,
    1443: Track.Shell_CHEEP_CHEEP_BEACH,
    1445: Track.Shell_TOADS_TURNPIKE,
    1447: Track.Banana_DRY_DRY_DESERT,
    1446: Track.Banana_DONUT_PLAINS_3,
    1451: Track.Banana_ROYAL_RACEWAY,
    1448: Track.Banana_DK_JUNGLE,
    1454: Track.Leaf_WARIO_STADUIM,
    1449: Track.Leaf_SHERBET_LAND,
    1452: Track.Leaf_MUSIC_PARK,
    1453: Track.Leaf_YOSHI_VALLEY,
    1450: Track.Lightning_TICKTOCK_CLOCK,
    1444: Track.Lightning_PIRANHA_PLANT_SLIDE,
    1455: Track.Lightning_GRUMBLE_VOLCANO,
    1456: Track.Lightning_RAINBOW_ROAD,
    1481: Track.Triforce_WARIOS_GOLD_MINE,
    1486: Track.Triforce_RAINBOW_ROAD,
    1487: Track.Triforce_ICE_ICE_OUTPOST,
    1488: Track.Triforce_HYRULE_CIRCUIT,
    1493: Track.Bell_NEO_BOWSER_CITY,
    1494: Track.Bell_RIBBON_ROAD,
    1495: Track.Bell_SUPER_BELL_SUBWAY,
    1496: Track.Bell_BIG_BLUE,
}

INTERNAL_TRACK_TO_CUP = {
    Track.Mushroom_MARIO_KART_STADIUM: GameSetup.Course.Cup.MUSHROOM,
    Track.Mushroom_WATER_PARK: GameSetup.Course.Cup.MUSHROOM,
    Track.Mushroom_SWEET_SWEET_CANYON: GameSetup.Course.Cup.MUSHROOM,
    Track.Mushroom_THWOMP_RUINS: GameSetup.Course.Cup.MUSHROOM,
    Track.Flower_MARIO_CIRCUIT: GameSetup.Course.Cup.FLOWER,
    Track.Flower_TOAD_HARBOR: GameSetup.Course.Cup.FLOWER,
    Track.Flower_TWISTED_MANSION: GameSetup.Course.Cup.FLOWER,
    Track.Flower_SHY_GUY_FALLS: GameSetup.Course.Cup.FLOWER,
    Track.Star_SUNSHINE_AIRPORT: GameSetup.Course.Cup.STAR,
    Track.Star_DOLPHIN_SHOALS: GameSetup.Course.Cup.STAR,
    Track.Star_ELECTRODOME: GameSetup.Course.Cup.STAR,
    Track.Star_MOUNT_WARIO: GameSetup.Course.Cup.STAR,
    Track.Special_CLOUDTOP_CRUISE: GameSetup.Course.Cup.SPECIAL,
    Track.Special_BONEDRY_DUNES: GameSetup.Course.Cup.SPECIAL,
    Track.Special_BOWSERS_CASTLE: GameSetup.Course.Cup.SPECIAL,
    Track.Special_RAINBOW_ROAD: GameSetup.Course.Cup.SPECIAL,
    Track.Egg_YOSHI_CIRCUIT: GameSetup.Course.Cup.EGG,
    Track.Egg_EXCITEBIKE_ARENA: GameSetup.Course.Cup.EGG,
    Track.Egg_DRAGON_DRIFTWAY: GameSetup.Course.Cup.EGG,
    Track.Egg_MUTE_CITY: GameSetup.Course.Cup.EGG,
    Track.Crossing_BABY_PARK: GameSetup.Course.Cup.CROSSING,
    Track.Crossing_CHEESE_LAND: GameSetup.Course.Cup.CROSSING,
    Track.Crossing_WILD_WOODS: GameSetup.Course.Cup.CROSSING,
    Track.Crossing_ANIMAL_CROSSING: GameSetup.Course.Cup.CROSSING,
    Track.Shell_MOO_MOO_MEADOWS: GameSetup.Course.Cup.SHELL,
    Track.Shell_MARIO_CIRCUIT: GameSetup.Course.Cup.SHELL,
    Track.Shell_CHEEP_CHEEP_BEACH: GameSetup.Course.Cup.SHELL,
    Track.Shell_TOADS_TURNPIKE: GameSetup.Course.Cup.SHELL,
    Track.Banana_DRY_DRY_DESERT: GameSetup.Course.Cup.BANANA,
    Track.Banana_DONUT_PLAINS_3: GameSetup.Course.Cup.BANANA,
    Track.Banana_ROYAL_RACEWAY: GameSetup.Course.Cup.BANANA,
    Track.Banana_DK_JUNGLE: GameSetup.Course.Cup.BANANA,
    Track.Leaf_WARIO_STADUIM: GameSetup.Course.Cup.LEAF,
    Track.Leaf_SHERBET_LAND: GameSetup.Course.Cup.LEAF,
    Track.Leaf_MUSIC_PARK: GameSetup.Course.Cup.LEAF,
    Track.Leaf_YOSHI_VALLEY: GameSetup.Course.Cup.LEAF,
    Track.Lightning_TICKTOCK_CLOCK: GameSetup.Course.Cup.LIGHTNING,
    Track.Lightning_PIRANHA_PLANT_SLIDE: GameSetup.Course.Cup.LIGHTNING,
    Track.Lightning_GRUMBLE_VOLCANO: GameSetup.Course.Cup.LIGHTNING,
    Track.Lightning_RAINBOW_ROAD: GameSetup.Course.Cup.LIGHTNING,
    Track.Triforce_WARIOS_GOLD_MINE: GameSetup.Course.Cup.TRIFORCE,
    Track.Triforce_RAINBOW_ROAD: GameSetup.Course.Cup.TRIFORCE,
    Track.Triforce_ICE_ICE_OUTPOST: GameSetup.Course.Cup.TRIFORCE,
    Track.Triforce_HYRULE_CIRCUIT: GameSetup.Course.Cup.TRIFORCE,
    Track.Bell_NEO_BOWSER_CITY: GameSetup.Course.Cup.BELL,
    Track.Bell_RIBBON_ROAD: GameSetup.Course.Cup.BELL,
    Track.Bell_SUPER_BELL_SUBWAY: GameSetup.Course.Cup.BELL,
    Track.Bell_BIG_BLUE: GameSetup.Course.Cup.BELL
}

INTERNAL_TRACK_TO_TRACK = {
    Track.Mushroom_MARIO_KART_STADIUM: GameSetup.Course.Cup.Mushroom.MARIO_KART_STADIUM,
    Track.Mushroom_WATER_PARK: GameSetup.Course.Cup.Mushroom.WATER_PARK,
    Track.Mushroom_SWEET_SWEET_CANYON: GameSetup.Course.Cup.Mushroom.SWEET_SWEET_CANYON,
    Track.Mushroom_THWOMP_RUINS: GameSetup.Course.Cup.Mushroom.THWOMP_RUINS,
    Track.Flower_MARIO_CIRCUIT: GameSetup.Course.Cup.Flower.MARIO_CIRCUIT,
    Track.Flower_TOAD_HARBOR: GameSetup.Course.Cup.Flower.TOAD_HARBOR,
    Track.Flower_TWISTED_MANSION: GameSetup.Course.Cup.Flower.TWISTED_MANSION,
    Track.Flower_SHY_GUY_FALLS: GameSetup.Course.Cup.Flower.SHY_GUY_FALLS,
    Track.Star_SUNSHINE_AIRPORT: GameSetup.Course.Cup.Star.SUNSHINE_AIRPORT,
    Track.Star_DOLPHIN_SHOALS: GameSetup.Course.Cup.Star.DOLPHIN_SHOALS,
    Track.Star_ELECTRODOME: GameSetup.Course.Cup.Star.ELECTRODOME,
    Track.Star_MOUNT_WARIO: GameSetup.Course.Cup.Star.MOUNT_WARIO,
    Track.Special_CLOUDTOP_CRUISE: GameSetup.Course.Cup.Special.CLOUDTOP_CRUISE,
    Track.Special_BONEDRY_DUNES: GameSetup.Course.Cup.Special.BONEDRY_DUNES,
    Track.Special_BOWSERS_CASTLE: GameSetup.Course.Cup.Special.BOWSERS_CASTLE,
    Track.Special_RAINBOW_ROAD: GameSetup.Course.Cup.Special.RAINBOW_ROAD,
    Track.Egg_YOSHI_CIRCUIT: GameSetup.Course.Cup.Egg.YOSHI_CIRCUIT,
    Track.Egg_EXCITEBIKE_ARENA: GameSetup.Course.Cup.Egg.EXCITEBIKE_ARENA,
    Track.Egg_DRAGON_DRIFTWAY: GameSetup.Course.Cup.Egg.DRAGON_DRIFTWAY,
    Track.Egg_MUTE_CITY: GameSetup.Course.Cup.Egg.MUTE_CITY,
    Track.Crossing_BABY_PARK: GameSetup.Course.Cup.Crossing.BABY_PARK,
    Track.Crossing_CHEESE_LAND: GameSetup.Course.Cup.Crossing.CHEESE_LAND,
    Track.Crossing_WILD_WOODS: GameSetup.Course.Cup.Crossing.WILD_WOODS,
    Track.Crossing_ANIMAL_CROSSING: GameSetup.Course.Cup.Crossing.ANIMAL_CROSSING,
    Track.Shell_MOO_MOO_MEADOWS: GameSetup.Course.Cup.Shell.MOO_MOO_MEADOWS,
    Track.Shell_MARIO_CIRCUIT: GameSetup.Course.Cup.Shell.MARIO_CIRCUIT,
    Track.Shell_CHEEP_CHEEP_BEACH: GameSetup.Course.Cup.Shell.CHEEP_CHEEP_BEACH,
    Track.Shell_TOADS_TURNPIKE: GameSetup.Course.Cup.Shell.TOADS_TURNPIKE,
    Track.Banana_DRY_DRY_DESERT: GameSetup.Course.Cup.Banana.DRY_DRY_DESERT,
    Track.Banana_DONUT_PLAINS_3: GameSetup.Course.Cup.Banana.DONUT_PLAINS_3,
    Track.Banana_ROYAL_RACEWAY: GameSetup.Course.Cup.Banana.ROYAL_RACEWAY,
    Track.Banana_DK_JUNGLE: GameSetup.Course.Cup.Banana.DK_JUNGLE,
    Track.Leaf_WARIO_STADUIM: GameSetup.Course.Cup.Leaf.WARIO_STADUIM,
    Track.Leaf_SHERBET_LAND: GameSetup.Course.Cup.Leaf.SHERBET_LAND,
    Track.Leaf_MUSIC_PARK: GameSetup.Course.Cup.Leaf.MUSIC_PARK,
    Track.Leaf_YOSHI_VALLEY: GameSetup.Course.Cup.Leaf.YOSHI_VALLEY,
    Track.Lightning_TICKTOCK_CLOCK: GameSetup.Course.Cup.Lightning.TICKTOCK_CLOCK,
    Track.Lightning_PIRANHA_PLANT_SLIDE: GameSetup.Course.Cup.Lightning.PIRANHA_PLANT_SLIDE,
    Track.Lightning_GRUMBLE_VOLCANO: GameSetup.Course.Cup.Lightning.GRUMBLE_VOLCANO,
    Track.Lightning_RAINBOW_ROAD: GameSetup.Course.Cup.Lightning.RAINBOW_ROAD,
    Track.Triforce_WARIOS_GOLD_MINE: GameSetup.Course.Cup.Triforce.WARIOS_GOLD_MINE,
    Track.Triforce_RAINBOW_ROAD: GameSetup.Course.Cup.Triforce.RAINBOW_ROAD,
    Track.Triforce_ICE_ICE_OUTPOST: GameSetup.Course.Cup.Triforce.ICE_ICE_OUTPOST,
    Track.Triforce_HYRULE_CIRCUIT: GameSetup.Course.Cup.Triforce.HYRULE_CIRCUIT,
    Track.Bell_NEO_BOWSER_CITY: GameSetup.Course.Cup.Bell.NEO_BOWSER_CITY,
    Track.Bell_RIBBON_ROAD: GameSetup.Course.Cup.Bell.RIBBON_ROAD,
    Track.Bell_SUPER_BELL_SUBWAY: GameSetup.Course.Cup.Bell.SUPER_BELL_SUBWAY,
    Track.Bell_BIG_BLUE: GameSetup.Course.Cup.Bell.BIG_BLUE
}

INTERNAL_TRACK_TO_FULL_LENGHT = {
    Track.Mushroom_MARIO_KART_STADIUM: 57207.78609144819,
    Track.Mushroom_WATER_PARK: 57533.41172566771,
    Track.Mushroom_SWEET_SWEET_CANYON: 73291.65908953053,
    Track.Mushroom_THWOMP_RUINS: 64900.99340198662,
    Track.Flower_MARIO_CIRCUIT: 63449.01660780873,
    Track.Flower_TOAD_HARBOR: 73850.66070996685,
    Track.Flower_TWISTED_MANSION: 67167.3361297428,
    Track.Flower_SHY_GUY_FALLS: 69610.82177464121,
    Track.Star_SUNSHINE_AIRPORT: 75398.37600194197,
    Track.Star_DOLPHIN_SHOALS: 66164.24180831146,
    Track.Star_ELECTRODOME: 71626.11181616246,
    Track.Star_MOUNT_WARIO: 61313.708663963036,
    Track.Special_CLOUDTOP_CRUISE: 77498.90569798792,
    Track.Special_BONEDRY_DUNES: 63943.27253723345,
    Track.Special_BOWSERS_CASTLE: 71431.97657489427,
    Track.Special_RAINBOW_ROAD: 77339.74689745405,
    Track.Egg_YOSHI_CIRCUIT: 66992.93407537621,
    Track.Egg_EXCITEBIKE_ARENA: 59207.45716377259,
    Track.Egg_DRAGON_DRIFTWAY: 63896.81625184043,
    Track.Egg_MUTE_CITY: 70404.81347975711,
    Track.Crossing_BABY_PARK: 41001.30021970484,
    Track.Crossing_CHEESE_LAND: 62788.815122158514,
    Track.Crossing_WILD_WOODS: 64000.739480983306,
    Track.Crossing_ANIMAL_CROSSING: 57400.40495264532,
    Track.Shell_MOO_MOO_MEADOWS: 48010.61532594241,
    Track.Shell_MARIO_CIRCUIT: 53964.52574815716,
    Track.Shell_CHEEP_CHEEP_BEACH: 61079.9958800555,
    Track.Shell_TOADS_TURNPIKE: 59931.53505396388,
    Track.Banana_DRY_DRY_DESERT: 67970.7008676574,
    Track.Banana_DONUT_PLAINS_3: 47889.95935650939,
    Track.Banana_ROYAL_RACEWAY: 69165.03817009072,
    Track.Banana_DK_JUNGLE: 72232.19171896401,
    Track.Leaf_WARIO_STADUIM: 66845.16479501835,
    Track.Leaf_SHERBET_LAND: 65273.66322921902,
    Track.Leaf_MUSIC_PARK: 67447.98248312775,
    Track.Leaf_YOSHI_VALLEY: 71742.32566469804,
    Track.Lightning_TICKTOCK_CLOCK: 62063.11056942507,
    Track.Lightning_PIRANHA_PLANT_SLIDE: 70571.07385669077,
    Track.Lightning_GRUMBLE_VOLCANO: 65289.22283698683,
    Track.Lightning_RAINBOW_ROAD: 45515.98138947499,
    Track.Triforce_WARIOS_GOLD_MINE: 67506.76362940011,
    Track.Triforce_RAINBOW_ROAD: 50621.73041941352,
    Track.Triforce_ICE_ICE_OUTPOST: 61953.594832580195,
    Track.Triforce_HYRULE_CIRCUIT: 64460.55922092189,
    Track.Bell_NEO_BOWSER_CITY: 62851.54936981612,
    Track.Bell_RIBBON_ROAD: 64420.19056365571,
    Track.Bell_SUPER_BELL_SUBWAY: 61057.68322300436,
    Track.Bell_BIG_BLUE: 55588.35927152202
}

INTERNAL_TRACK_TO_LAP_LENGHT = {
    Track.Mushroom_MARIO_KART_STADIUM: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Mushroom_MARIO_KART_STADIUM] / 3.0,
    Track.Mushroom_WATER_PARK: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Mushroom_WATER_PARK] / 3.0,
    Track.Mushroom_SWEET_SWEET_CANYON: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Mushroom_SWEET_SWEET_CANYON] / 3.0,
    Track.Mushroom_THWOMP_RUINS: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Mushroom_THWOMP_RUINS] / 3.0,
    Track.Flower_MARIO_CIRCUIT: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Flower_MARIO_CIRCUIT] / 3.0,
    Track.Flower_TOAD_HARBOR: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Flower_TOAD_HARBOR] / 3.0,
    Track.Flower_TWISTED_MANSION: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Flower_TWISTED_MANSION] / 3.0,
    Track.Flower_SHY_GUY_FALLS: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Flower_SHY_GUY_FALLS] / 3.0,
    Track.Star_SUNSHINE_AIRPORT: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Star_SUNSHINE_AIRPORT] / 3.0,
    Track.Star_DOLPHIN_SHOALS: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Star_DOLPHIN_SHOALS] / 3.0,
    Track.Star_ELECTRODOME: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Star_ELECTRODOME] / 3.0,
    Track.Star_MOUNT_WARIO: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Star_MOUNT_WARIO] / 3.0,
    Track.Special_CLOUDTOP_CRUISE: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Special_CLOUDTOP_CRUISE] / 3.0,
    Track.Special_BONEDRY_DUNES: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Special_BONEDRY_DUNES] / 3.0,
    Track.Special_BOWSERS_CASTLE: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Special_BOWSERS_CASTLE] / 3.0,
    Track.Special_RAINBOW_ROAD: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Special_RAINBOW_ROAD] / 3.0,
    Track.Egg_YOSHI_CIRCUIT: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Egg_YOSHI_CIRCUIT] / 3.0,
    Track.Egg_EXCITEBIKE_ARENA: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Egg_EXCITEBIKE_ARENA] / 3.0,
    Track.Egg_DRAGON_DRIFTWAY: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Egg_DRAGON_DRIFTWAY] / 3.0,
    Track.Egg_MUTE_CITY: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Egg_MUTE_CITY] / 3.0,
    Track.Crossing_BABY_PARK: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Crossing_BABY_PARK] / 7.0,
    Track.Crossing_CHEESE_LAND: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Crossing_CHEESE_LAND] / 3.0,
    Track.Crossing_WILD_WOODS: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Crossing_WILD_WOODS] / 3.0,
    Track.Crossing_ANIMAL_CROSSING: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Crossing_ANIMAL_CROSSING] / 3.0,
    Track.Shell_MOO_MOO_MEADOWS: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Shell_MOO_MOO_MEADOWS] / 3.0,
    Track.Shell_MARIO_CIRCUIT: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Shell_MARIO_CIRCUIT] / 3.0,
    Track.Shell_CHEEP_CHEEP_BEACH: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Shell_CHEEP_CHEEP_BEACH] / 3.0,
    Track.Shell_TOADS_TURNPIKE: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Shell_TOADS_TURNPIKE] / 3.0,
    Track.Banana_DRY_DRY_DESERT: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Banana_DRY_DRY_DESERT] / 3.0,
    Track.Banana_DONUT_PLAINS_3: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Banana_DONUT_PLAINS_3] / 3.0,
    Track.Banana_ROYAL_RACEWAY: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Banana_ROYAL_RACEWAY] / 3.0,
    Track.Banana_DK_JUNGLE: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Banana_DK_JUNGLE] / 3.0,
    Track.Leaf_WARIO_STADUIM: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Leaf_WARIO_STADUIM] / 3.0,
    Track.Leaf_SHERBET_LAND: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Leaf_SHERBET_LAND] / 3.0,
    Track.Leaf_MUSIC_PARK: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Leaf_MUSIC_PARK] / 3.0,
    Track.Leaf_YOSHI_VALLEY: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Leaf_YOSHI_VALLEY] / 3.0,
    Track.Lightning_TICKTOCK_CLOCK: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Lightning_TICKTOCK_CLOCK] / 3.0,
    Track.Lightning_PIRANHA_PLANT_SLIDE: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Lightning_PIRANHA_PLANT_SLIDE] / 3.0,
    Track.Lightning_GRUMBLE_VOLCANO: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Lightning_GRUMBLE_VOLCANO] / 3.0,
    Track.Lightning_RAINBOW_ROAD: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Lightning_RAINBOW_ROAD] / 3.0,
    Track.Triforce_WARIOS_GOLD_MINE: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Triforce_WARIOS_GOLD_MINE] / 3.0,
    Track.Triforce_RAINBOW_ROAD: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Triforce_RAINBOW_ROAD] / 3.0,
    Track.Triforce_ICE_ICE_OUTPOST: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Triforce_ICE_ICE_OUTPOST] / 3.0,
    Track.Triforce_HYRULE_CIRCUIT: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Triforce_HYRULE_CIRCUIT] / 3.0,
    Track.Bell_NEO_BOWSER_CITY: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Bell_NEO_BOWSER_CITY] / 3.0,
    Track.Bell_RIBBON_ROAD: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Bell_RIBBON_ROAD] / 3.0,
    Track.Bell_SUPER_BELL_SUBWAY: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Bell_SUPER_BELL_SUBWAY] / 3.0,
    Track.Bell_BIG_BLUE: INTERNAL_TRACK_TO_FULL_LENGHT[Track.Bell_BIG_BLUE] / 3.0
}
