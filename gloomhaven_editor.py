#!/usr/bin/env python3
"""Gloomhaven digital save file editor — manage owned card pools."""

import os
import platform
import shutil
import struct
import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog, messagebox, ttk

# ── Card data (source: ModdingExport/Global/AbilityCard/) ─────────────────

BRUTE_CARDS = [
    (1,  "Trample",                1),
    (2,  "Eye for an Eye",         1),
    (3,  "Sweeping Blow",          1),
    (4,  "Provoking Roar",         1),
    (5,  "Overwhelming Assault",   1),
    (6,  "Grab and Go",            1),
    (7,  "Warding Strength",       1),
    (8,  "Shield Bash",            1),
    (9,  "Leaping Cleave",         1),
    (10, "Spare Dagger",           1),
    (11, "Skewer",                "X"),
    (12, "Balanced Measure",      "X"),
    (13, "Wall of Doom",          "X"),
    (14, "Fatal Advance",          2),
    (15, "Juggernaut",             2),
    (16, "Hook and Chain",         3),
    (17, "Brute Force",            3),
    (18, "Unstoppable Charge",     4),
    (19, "Devastating Hack",       4),
    (20, "Whirlwind",              5),
    (21, "Skirmishing Maneuver",   5),
    (22, "Quietus",                6),
    (23, "Immovable Phalanx",      6),
    (24, "Defensive Tactics",      7),
    (25, "Crippling Offensive",    7),
    (26, "Frenzied Onslaught",     8),
    (27, "Selfish Retribution",    8),
    (28, "King of the Hill",       9),
    (29, "Face Your End",          9),
]

TINKERER_CARDS = [
    (30, "Proximity Mine",         1),
    (31, "Harmless Contraption",   1),
    (32, "Flamethrower",           1),
    (33, "Hook Gun",               1),
    (34, "Ink Bomb",               1),
    (35, "Net Shooter",            1),
    (36, "Stun Shot",              1),
    (37, "Reinvigorating Elixir",  1),
    (38, "Restorative Mist",       1),
    (39, "Energizing Tonic",       1),
    (40, "Enhancement Field",      1),
    (41, "Toxic Bolt",             1),
    (42, "Reviving Shock",        "X"),
    (43, "Volatile Concoction",   "X"),
    (44, "Potent Potables",       "X"),
    (45, "Stamina Booster",        2),
    (46, "Disorienting Flash",     2),
    (47, "Tinkerer's Tools",       3),
    (48, "Crank Bow",              3),
    (49, "Dangerous Contraption",  4),
    (50, "Micro Bots",             4),
    (51, "Noxious Vials",          5),
    (52, "Disintegration Beam",    5),
    (53, "Gas Canister",           6),
    (54, "Auto Turret",            6),
    (55, "Murderous Contraption",  7),
    (56, "Curative Aerosol",       7),
    (57, "Jet Propulsion",         8),
    (58, "Harsh Stimulants",       8),
    (59, "Lethal Injection",       9),
    (60, "Chimeric Formula",       9),
]

SPELLWEAVER_CARDS = [
    (61, "Fire Orbs",              1),
    (62, "Impaling Eruption",      1),
    (63, "Reviving Ether",         1),
    (64, "Freezing Nova",          1),
    (65, "Mana Bolt",              1),
    (66, "Frost Armor",            1),
    (67, "Flame Strike",           1),
    (68, "Ride the Wind",          1),
    (69, "Crackling Air",         "X"),
    (70, "Hardened Spikes",       "X"),
    (71, "Aid from the Aether",   "X"),
    (72, "Flashing Burst",         2),
    (73, "Icy Blast",              2),
    (74, "Cold Fire",              3),
    (75, "Elemental Aid",          3),
    (76, "Spirit of Doom",         4),
    (77, "Forked Beam",            4),
    (78, "Chromatic Explosion",    5),
    (79, "Engulfed in Flames",     5),
    (80, "Living Torch",           6),
    (81, "Frozen Night",           6),
    (82, "Twin Restoration",       7),
    (83, "Stone Fists",            7),
    (84, "Zephyr Wings",           8),
    (85, "Cold Front",             8),
    (86, "Black Hole",             9),
    (87, "Inferno",                9),
]

SCOUNDREL_CARDS = [
    (88,  "Single Out",                1),
    (89,  "Flanking Strike",           1),
    (90,  "Smoke Bomb",                1),
    (91,  "Backstab",                  1),
    (92,  "Thief's Knack",             1),
    (93,  "Venom Shiv",                1),
    (94,  "Throwing Knives",           1),
    (95,  "Quick Hands",               1),
    (96,  "Special Mixture",           1),
    (97,  "Sinister Opportunity",     "X"),
    (98,  "Trickster's Reversal",     "X"),
    (99,  "Swift Bow",                "X"),
    (100, "Open Wound",                2),
    (101, "Flintlock",                 2),
    (102, "Hidden Daggers",            3),
    (103, "Duelist's Advance",         3),
    (104, "Flurry of Blades",          4),
    (105, "Gruesome Advantage",        4),
    (106, "Cull the Weak",             5),
    (107, "Visage of the Inevitable",  5),
    (108, "Crippling Poison",          6),
    (109, "Burning Oil",               6),
    (110, "Stick to the Shadows",      7),
    (111, "Spring the Trap",           7),
    (112, "Stiletto Storm",            8),
    (113, "Pain's End",                8),
    (114, "Long Con",                  9),
    (115, "Watch It Burn",             9),
]

CRAGHEART_CARDS = [
    (116, "Opposing Strike",       1),
    (117, "Crushing Grasp",        1),
    (118, "Avalanche",             1),
    (119, "Rumbling Advance",      1),
    (120, "Massive Boulder",       1),
    (121, "Backup Ammunition",     1),
    (122, "Rock Tunnel",           1),
    (123, "Unstable Upheaval",     1),
    (124, "Crater",                1),
    (125, "Dirt Tornado",          1),
    (126, "Earthen Clod",          1),
    (127, "Heaving Swing",        "X"),
    (128, "Forceful Storm",       "X"),
    (129, "Nature's Lift",        "X"),
    (130, "Explosive Punch",       2),
    (131, "Sentient Growth",       2),
    (132, "Clear the Way",         3),
    (133, "Blunt Force",           3),
    (134, "Rock Slide",            4),
    (135, "Kinetic Assault",       4),
    (136, "Petrify",               5),
    (137, "Stone Pummel",          5),
    (138, "Dig Pit",               6),
    (139, "Cataclysm",             6),
    (140, "Meteor",                7),
    (141, "Brutal Momentum",       7),
    (142, "Rocky End",             8),
    (143, "Lumbering Bash",        8),
    (144, "Blind Destruction",     9),
    (145, "Pulverize",             9),
]

MINDTHIEF_CARDS = [
    (146, "Submissive Affliction",  1),
    (147, "Into the Night",         1),
    (148, "Fearsome Blade",         1),
    (149, "Feedback Loop",          1),
    (150, "Gnawing Horde",          1),
    (151, "The Mind's Weakness",    1),
    (152, "Parasitic Influence",    1),
    (153, "Scurry",                 1),
    (154, "Perverse Edge",          1),
    (155, "Empathetic Assault",     1),
    (156, "Withering Claw",        "X"),
    (157, "Possession",            "X"),
    (158, "Frigid Apparition",     "X"),
    (159, "Wretched Creature",      2),
    (160, "Hostile Takeover",       2),
    (161, "Brain Leech",            3),
    (162, "Silent Scream",          3),
    (163, "Pilfer",                 4),
    (164, "Cranium Overload",       4),
    (165, "Mass Hysteria",          5),
    (166, "Frozen Mind",            5),
    (167, "Corrupting Embrace",     6),
    (168, "Dark Frenzy",            6),
    (169, "Vicious Blood",          7),
    (170, "Psychic Projection",     7),
    (171, "Shared Nightmare",       8),
    (172, "Domination",             8),
    (173, "Many as One",            9),
    (174, "Phantasmal Killer",      9),
]

SUNKEEPER_CARDS = [
    (175, "Purifying Aura",         1),
    (176, "Cautious Advance",       1),
    (177, "Brilliant Prayer",       1),
    (178, "Empowering Command",     1),
    (179, "Protective Blessing",    1),
    (180, "Dazzling Charge",        1),
    (181, "Tactical Order",         1),
    (182, "Holy Strike",            1),
    (183, "Hammer Blow",            1),
    (184, "Defensive Stance",       1),
    (185, "Lay on Hands",           1),
    (186, "Daybreak",              "X"),
    (187, "Beacon of Light",       "X"),
    (188, "Glorious Bolt",         "X"),
    (189, "Practical Plans",        2),
    (190, "Unwavering Mandate",     2),
    (191, "Burning Flash",          3),
    (192, "Mobilizing Axiom",       3),
    (193, "Righteous Strength",     4),
    (194, "Engulfing Radiance",     4),
    (195, "Path of Glory",          5),
    (196, "Scales of Justice",      5),
    (197, "Supportive Chant",       6),
    (198, "Illuminate the Target",  6),
    (199, "Weapon of Purity",       7),
    (200, "Bright Aegis",           7),
    (201, "Cleansing Force",        8),
    (202, "Inspiring Sanctity",     8),
    (203, "Angelic Ascension",      9),
    (204, "Divine Intervention",    9),
]

QUARTERMASTER_CARDS = [
    (205, "Restock",                1),
    (206, "Oversized Pack",         1),
    (207, "Sharpening Kit",         1),
    (208, "Proficiency",            1),
    (209, "Iron Bulwark",           1),
    (210, "Hastened Step",          1),
    (211, "Cleaving Axe",           1),
    (212, "Impaling Spear",         1),
    (213, "Crippling Bow",          1),
    (214, "Crushing Hammer",       "X"),
    (215, "Scroll of Recall",      "X"),
    (216, "Reserved Energy",       "X"),
    (217, "Reforge",                2),
    (218, "Bladed Boomerang",       2),
    (219, "Continual Supply",       3),
    (220, "Scroll of Lightning",    3),
    (221, "Side Pouch",             4),
    (222, "Giant Club",             4),
    (223, "Reinforced Steel",       5),
    (224, "Scroll of Judgment",     5),
    (225, "Catastrophic Bomb",      6),
    (226, "Quiver of Arrows",       6),
    (227, "Scroll of Blizzards",    7),
    (228, "Refreshment",            7),
    (229, "Portable Ballista",      8),
    (230, "Fortified Position",     8),
    (231, "Scroll of Annihilation", 9),
    (232, "Bag of Holding",         9),
]

SUMMONER_CARDS = [
    (233, "Forged Ferocity",        1),
    (234, "Wild Animation",         1),
    (235, "Living Night",           1),
    (236, "Unending Dominance",     1),
    (237, "Unwavering Hand",        1),
    (238, "Mighty Bond",            1),
    (239, "Bonded Might",           1),
    (240, "Biting Wind",            1),
    (241, "Black Fire",             1),
    (242, "Leathery Wings",        "X"),
    (243, "Volatile Flame",        "X"),
    (244, "Ethereal Vines",        "X"),
    (245, "Earthen Steed",          2),
    (246, "Grasping the Void",      2),
    (247, "Tear the Fabric",        3),
    (248, "Oozing Manifestation",   3),
    (249, "Living Mountain",        4),
    (250, "Divided Mind",           4),
    (251, "Strength in Numbers",    5),
    (252, "Conjured Aid",           5),
    (253, "Endless Spikes",         6),
    (254, "Inexorable Momentum",    6),
    (255, "Negative Energy",        7),
    (256, "Staff of Visions",       7),
    (257, "Intervening Apparitions",8),
    (258, "Otherworldly Rage",      8),
    (259, "Interplanar Mastery",    9),
    (260, "Horned Majesty",         9),
]

NIGHTSHROUD_CARDS = [
    (261, "Black Knives",           1),
    (262, "Cloak of Shade",         1),
    (263, "Empowering Void",        1),
    (264, "Doomed Breeze",          1),
    (265, "Enervating Wound",       1),
    (266, "Spirit of the Night",    1),
    (267, "Dancing Shadows",        1),
    (268, "Silent Force",           1),
    (269, "Smoke Step",             1),
    (270, "Wings of the Night",    "X"),
    (271, "Concealed Dominance",   "X"),
    (272, "Dark Cloud",            "X"),
    (273, "Prepare for the Kill",   2),
    (274, "Soulfire",               2),
    (275, "Terror Blade",           3),
    (276, "Armor of the Night",     3),
    (277, "Nightfall",              4),
    (278, "Grim Sustenance",        4),
    (279, "Claws of the Night",     5),
    (280, "Black Arrow",            5),
    (281, "Unseen Dread",           6),
    (282, "Swallowed by Fear",      6),
    (283, "Eyes of the Night",      7),
    (284, "Quiet Frenzy",           7),
    (285, "Gloom Darts",            8),
    (286, "Lurking Ruin",           8),
    (287, "Angel of Death",         9),
    (288, "Voice of the Night",     9),
]

PLAGUEHERALD_CARDS = [
    (289, "Vile Pestilence",        1),
    (290, "Grasping Vermin",        1),
    (291, "Wretched Swarm",         1),
    (292, "Spread the Plague",      1),
    (293, "Biting Gnats",           1),
    (294, "Winged Congregation",    1),
    (295, "Creeping Curse",         1),
    (296, "Gathering Doom",         1),
    (297, "Paralyzing Bite",        1),
    (298, "Foul Wind",              1),
    (299, "Scattered Terror",       1),
    (300, "Epidemic",              "X"),
    (301, "Virulent Strain",       "X"),
    (302, "Blistering Vortex",     "X"),
    (303, "Under the Skin",         2),
    (304, "Rot Maggots",            2),
    (305, "Succumb to the Gift",    3),
    (306, "Fetid Flurry",           3),
    (307, "Storm of Wings",         4),
    (308, "Nightmarish Affliction", 4),
    (309, "Accelerated End",        5),
    (310, "Willing Sacrifice",      5),
    (311, "Stinging Cloud",         6),
    (312, "Black Tides",            6),
    (313, "Airborne Toxin",         7),
    (314, "Baneful Hex",            7),
    (315, "Spreading Scourge",      8),
    (316, "Grim Bargain",           8),
    (317, "Mass Extinction",        9),
    (318, "Convert the Flock",      9),
]

BERSERKER_CARDS = [
    (319, "Resolute Stand",             1),
    (320, "Growing Rage",               1),
    (321, "Strength in Agony",          1),
    (322, "Defiance of Death",          1),
    (323, "From the Brink",             1),
    (324, "Blood Pact",                 1),
    (325, "Cauterize",                  1),
    (326, "Dazing Wound",               1),
    (327, "Furious Aid",                1),
    (328, "Bounce Back",                1),
    (329, "Unbridled Power",           "X"),
    (330, "Glass Hammer",              "X"),
    (331, "Numb the Pain",             "X"),
    (332, "Reckless Offensive",         2),
    (333, "Break the Chains",           2),
    (334, "Spiked Armor",               3),
    (335, "Fatal Fury",                 3),
    (336, "Flurry of Axes",             4),
    (337, "Shiny Distraction",          4),
    (338, "Seeing Red",                 5),
    (339, "Final Fight",                5),
    (340, "Devil Horns",                6),
    (341, "Unstoppable Destruction",    6),
    (342, "Burning Hatred",             7),
    (343, "Careless Charge",            7),
    (344, "Bone Breaker",               8),
    (345, "Vengeful Barrage",           8),
    (346, "Immortality",                9),
    (347, "The Maw of Madness",         9),
]

SOOTHSINGER_CARDS = [
    (348, "Power Ballad",           1),
    (349, "Defensive Ditty",        1),
    (350, "Song of Speed",          1),
    (351, "Tuning the Outcome",     1),
    (352, "Call to Action",         1),
    (353, "Warding Dagger",         1),
    (354, "Throw Voice",            1),
    (355, "Singing Arrow",          1),
    (356, "Marching Beat",          1),
    (357, "Wistful Wounding",      "X"),
    (358, "Unending Chant",        "X"),
    (359, "Nimble Knife",          "X"),
    (360, "Soothing Lullaby",       2),
    (361, "Change Tempo",           2),
    (362, "Echoing Aria",           3),
    (363, "Crippling Chorus",       3),
    (364, "Disorienting Dirge",     4),
    (365, "Inspiring Anthem",       4),
    (366, "Melody and Harmony",     5),
    (367, "Mobilizing Measure",     5),
    (368, "Pull the Strings",       6),
    (369, "Provoke Terror",         6),
    (370, "Nightmare Serenade",     7),
    (371, "Booming Proclamation",   7),
    (372, "Tranquil Trill",         8),
    (373, "Commanding Presence",    8),
    (374, "Captivating Performance",9),
    (375, "Shadow Puppets",         9),
]

DOOMSTALKER_CARDS = [
    (376, "Rain of Arrows",         1),
    (377, "Crippling Noose",        1),
    (378, "Felling Swoop",          1),
    (379, "Vital Charge",           1),
    (380, "Race to the Grave",      1),
    (381, "Multi-Pronged Assault",  1),
    (382, "Detonation",             1),
    (383, "Frightening Curse",      1),
    (384, "Foot Snare",             1),
    (385, "Solid Bow",              1),
    (386, "A Moment's Peace",       1),
    (387, "Swift Trickery",         1),
    (388, "Sap Life",              "X"),
    (389, "The Hunt Begins",       "X"),
    (390, "Fresh Kill",            "X"),
    (391, "Expose",                 2),
    (392, "Relentless Offensive",   2),
    (393, "Darkened Skies",         3),
    (394, "Press the Attack",       3),
    (395, "Singular Focus",         4),
    (396, "Flight of Flame",        4),
    (397, "Inescapable Fate",       5),
    (398, "Wild Command",           5),
    (399, "Nature's Hunger",        6),
    (400, "Camouflage",             6),
    (401, "Impending End",          7),
    (402, "Crashing Wave",          7),
    (403, "Rising Momentum",        8),
    (404, "Feral Instincts",        8),
    (405, "Predator and Prey",      9),
    (406, "Lead to Slaughter",      9),
]

# Medical Pack (IDs 417-423) and Large Medical Pack (IDs 424-427) are
# consumable cards — each ID is a separate physical copy.
SAWBONES_CARDS = [
    (407, "First Aid",              1),
    (408, "Hand of the Surgeon",    1),
    (409, "Hold Back the Pain",     1),
    (410, "Booster Shot",           1),
    (411, "Bloody Saw",             1),
    (412, "Curative Mixture",       1),
    (413, "Syringe",                1),
    (414, "Battlefield Medicine",   1),
    (415, "Triage",                 1),
    (416, "Mobile Response",        1),
    (417, "Medical Pack",          "X"),
    (418, "Medical Pack",          "X"),
    (419, "Medical Pack",          "X"),
    (420, "Medical Pack",          "X"),
    (421, "Medical Pack",          "X"),
    (422, "Medical Pack",          "X"),
    (423, "Medical Pack",          "X"),
    (424, "Large Medical Pack",    "X"),
    (425, "Large Medical Pack",    "X"),
    (426, "Large Medical Pack",    "X"),
    (427, "Large Medical Pack",    "X"),
    (428, "Prevention is Key",     "X"),
    (429, "Teamwork",              "X"),
    (430, "Vaccine",               "X"),
    (431, "Hamstring",              2),
    (432, "Precaution",             2),
    (433, "Regenerative Tissue",    3),
    (434, "Vital Strike",           3),
    (435, "Blood Transfusion",      4),
    (436, "Do No Harm",             4),
    (437, "Research the Cure",      5),
    (438, "Amputate",               5),
    (439, "Euthanize",              6),
    (440, "Prescription",           6),
    (441, "Master Physician",       7),
    (442, "Surgeon's Satchel",      7),
    (443, "Bedside Manner",         8),
    (444, "Gentleman's Anger",      8),
    (445, "Prep for Surgery",       9),
    (446, "Grisly Trauma",          9),
]

ELEMENTALIST_CARDS = [
    (447, "Raw Enhancement",        1),
    (448, "Pure Augmentation",      1),
    (449, "Formless Power",         1),
    (450, "Shaping the Aether",     1),
    (451, "Stoking Hail",           1),
    (452, "Tremulant Cyclone",      1),
    (453, "Infernal Vortex",        1),
    (454, "Lava Eruption",          1),
    (455, "Ice Spikes",             1),
    (456, "Frigid Torrent",         1),
    (457, "Malleable Evocation",   "X"),
    (458, "Brilliant Flash",       "X"),
    (459, "Encompassing Shadow",   "X"),
    (460, "Boiling Arc",            2),
    (461, "Crystallizing Blast",    2),
    (462, "Burial",                 3),
    (463, "Chain Lightning",        3),
    (464, "Primal Duality",         4),
    (465, "Gravel Vortex",          4),
    (466, "Obsidian Shards",        5),
    (467, "Winter's Edge",          5),
    (468, "Eye of the Hurricane",   6),
    (469, "Simulacrum",             6),
    (470, "Vengeance",              7),
    (471, "Pragmatic Reinforcement",7),
    (472, "Volatile Consumption",   8),
    (473, "Elemental Aegis",        8),
    (474, "Ethereal Manifestation", 9),
    (475, "Eternal Equilibrium",    9),
]

BEASTTYRANT_CARDS = [
    (477, "Disorienting Roar",      1),
    (478, "Spirit Swap",            1),
    (479, "Venomous Ally",          1),
    (480, "Relentless Ally",        1),
    (481, "Concentrated Rage",      1),
    (482, "Disappearing Wounds",    1),
    (483, "Patch Fur",              1),
    (484, "Maul",                   1),
    (485, "Forceful Swipe",         1),
    (486, "Howling Bolts",          1),
    (487, "Soaring Ally",          "X"),
    (488, "Focused Aggression",    "X"),
    (489, "Borrowed Essence",      "X"),
    (490, "Energizing Strike",      2),
    (491, "Earthen Spikes",         2),
    (492, "Vicious Ally",           3),
    (493, "Unstoppable Beast",      3),
    (494, "Ancient Ward",           4),
    (495, "Punch Through",          4),
    (496, "Rampage",                5),
    (497, "Stone Sigil",            5),
    (498, "Primal Blessing",        6),
    (499, "Blood Hunger",           6),
    (500, "Storm Sigil",            7),
    (501, "Tyrannical Force",       7),
    (502, "Lash Out",               8),
    (503, "Natural Remedy",         8),
    (504, "Jaws of Death",          9),
    (505, "Tribal Sigil",           9),
]

# ── Class registry ─────────────────────────────────────────────────────────
# Maps CharacterID string (as stored in save) -> (display class name, card list)

CLASS_REGISTRY = {
    "BruteID":         ("Brute",         BRUTE_CARDS),
    "TinkererID":      ("Tinkerer",      TINKERER_CARDS),
    "SpellweaverID":   ("Spellweaver",   SPELLWEAVER_CARDS),
    "ScoundrelID":     ("Scoundrel",     SCOUNDREL_CARDS),
    "CragheartID":     ("Cragheart",     CRAGHEART_CARDS),
    "MindthiefID":     ("Mindthief",     MINDTHIEF_CARDS),
    "SunkeeperID":     ("Sunkeeper",     SUNKEEPER_CARDS),
    "QuartermasterID": ("Quartermaster", QUARTERMASTER_CARDS),
    "SummonerID":      ("Summoner",      SUMMONER_CARDS),
    "NightshroudID":   ("Nightshroud",   NIGHTSHROUD_CARDS),
    "PlagueheraldID":  ("Plagueherald",  PLAGUEHERALD_CARDS),
    "BerserkerID":     ("Berserker",     BERSERKER_CARDS),
    "SoothsingerID":   ("Soothsinger",   SOOTHSINGER_CARDS),
    "DoomstalkerID":   ("Doomstalker",   DOOMSTALKER_CARDS),
    "SawbonesID":      ("Sawbones",      SAWBONES_CARDS),
    "ElementalistID":  ("Elementalist",  ELEMENTALIST_CARDS),
    "BeastTyrantID":   ("Beast Tyrant",  BEASTTYRANT_CARDS),
}


def _candidate_save_dirs():
    """Return likely Gloomhaven save directories for the current platform."""
    home = os.path.expanduser("~")
    system = platform.system()

    if system == "Windows":
        local_low = os.path.join(
            os.environ.get("USERPROFILE", home),
            "AppData",
            "LocalLow",
            "FlamingFowlStudios",
            "Gloomhaven",
            "GloomSaves",
            "Campaign",
        )
        return [local_low]

    if system == "Darwin":
        return [
            os.path.join(
                home,
                "Library",
                "Application Support",
                "Steam",
                "steamapps",
                "compatdata",
                "780290",
                "pfx",
                "drive_c",
                "users",
                "steamuser",
                "AppData",
                "LocalLow",
                "FlamingFowlStudios",
                "Gloomhaven",
                "GloomSaves",
                "Campaign",
            ),
            os.path.join(
                home,
                "Library",
                "Application Support",
                "Steam",
                "steamapps",
                "common",
                "Gloomhaven",
            ),
        ]

    return [
        os.path.join(
            home,
            ".steam",
            "steam",
            "steamapps",
            "compatdata",
            "780290",
            "pfx",
            "drive_c",
            "users",
            "steamuser",
            "AppData",
            "LocalLow",
            "FlamingFowlStudios",
            "Gloomhaven",
            "GloomSaves",
            "Campaign",
        ),
        os.path.join(
            home,
            ".local",
            "share",
            "Steam",
            "steamapps",
            "compatdata",
            "780290",
            "pfx",
            "drive_c",
            "users",
            "steamuser",
            "AppData",
            "LocalLow",
            "FlamingFowlStudios",
            "Gloomhaven",
            "GloomSaves",
            "Campaign",
        ),
    ]


def _first_existing_dir(paths):
    """Return the first existing directory from paths, else an empty string."""
    for path in paths:
        if os.path.isdir(path):
            return path
    return ""


def _open_hint_message():
    """Build the platform-specific help text shown before opening a save."""
    system = platform.system()
    candidates = _candidate_save_dirs()
    existing = [path for path in candidates if os.path.isdir(path)]

    lines = ["Pick a Gloomhaven campaign `.dat` save file."]

    if system == "Windows":
        lines.append("Likely location on Windows:")
    elif system == "Darwin":
        lines.append("Likely location on macOS (Steam compatibility layer / Wine-based setup):")
    else:
        lines.append("Likely location on Linux / Steam Proton:")
        lines.append("Start from your Steam library's `steamapps` folder. This may be under your home directory or on another mounted drive.")
        lines.append("Example Steam library roots:")
        lines.append("~/SteamLibrary/steamapps")
        lines.append("/mnt/<drive>/SteamLibrary/steamapps")
        lines.append("/media/<user>/<drive>/SteamLibrary/steamapps")
        lines.append("")
        lines.append("Then go to:")
        lines.append("compatdata/780290/pfx/drive_c/users/steamuser/AppData/LocalLow/FlamingFowlStudios/Gloomhaven/GloomSaves/Campaign")
        return "\n".join(lines)

    lines.extend(existing or candidates)
    lines.append("")
    lines.append("Look for folders named `Campaign_<PartyName>_<ID>` and open the `.dat` file inside.")
    return "\n".join(lines)

# ── Binary parsing ─────────────────────────────────────────────────────────

def _find_string_obj_id(data, text):
    """Return the object ID of the BinaryObjectString (0x06) containing text."""
    encoded = text.encode("utf-8")
    length = len(encoded)
    assert length < 128, "String too long for single-byte length encoding"
    search = bytes([length]) + encoded
    idx = 0
    while True:
        idx = data.find(search, idx)
        if idx == -1:
            return None
        if idx >= 5 and data[idx - 5] == 0x06:
            return struct.unpack_from("<I", data, idx - 4)[0]
        idx += 1


def _read_string_by_obj_id(data, obj_id):
    """Read the string content of a BinaryObjectString by its object ID."""
    pat = bytes([0x06]) + struct.pack("<I", obj_id)
    idx = data.find(pat)
    if idx == -1:
        return None
    b = data[idx + 5]
    if b < 128:
        length, start = b, idx + 6
    else:
        b2 = data[idx + 6]
        length, start = (b & 0x7F) | (b2 << 7), idx + 7
    try:
        return data[start : start + length].decode("utf-8")
    except Exception:
        return None


def find_character_list_ids(data, char_id_string):
    """
    Locate OwnedAbilityCardIDs and HandAbilityCardIDs List<int> object IDs
    for a character by their CharacterID string (e.g. "BruteID").

    CharacterID is serialized INLINE as a BinaryObjectString (0x06) within the
    CMapCharacter record. Fixed offsets from the byte immediately after the string:

        str_end +  0 : int32   m_CharacterGold
        str_end +  4 : int32   EXP
        str_end +  8 : int32   Level
        str_end + 12 : 0x09    CharacterPersistentEnhancements ref marker
        str_end + 17 : 0x09    OwnedAbilityCardIDs ref marker
        str_end + 18 : int32   OwnedAbilityCardIDs obj_id
        str_end + 22 : 0x09    HandAbilityCardIDs ref marker
        str_end + 23 : int32   HandAbilityCardIDs obj_id

    Returns (owned_list_id, hand_list_id, char_display_name) or (None, None, None).
    """
    encoded = char_id_string.encode("utf-8")
    length  = len(encoded)
    assert length < 128

    # Match [length_byte][chars] and verify 0x06 five bytes prior
    search = bytes([length]) + encoded
    idx = 0
    while True:
        idx = data.find(search, idx)
        if idx == -1:
            return None, None, None
        if idx >= 5 and data[idx - 5] == 0x06:
            # idx = position of the length byte; string chars follow at idx+1
            str_end = idx + 1 + length  # first byte after the BinaryObjectString record
            if str_end + 27 > len(data):
                idx += 1
                continue
            if (data[str_end + 12] == 0x09 and
                    data[str_end + 17] == 0x09 and
                    data[str_end + 22] == 0x09):
                owned_list_id = struct.unpack_from("<I", data, str_end + 18)[0]
                hand_list_id  = struct.unpack_from("<I", data, str_end + 23)[0]
                # DisplayCharacterName is a MemberReference (0x09) immediately
                # before the CharacterID BinaryObjectString record
                str_rec_start = idx - 5  # position of 0x06 byte
                char_name = None
                if str_rec_start >= 5 and data[str_rec_start - 5] == 0x09:
                    name_obj_id = struct.unpack_from("<I", data, str_rec_start - 4)[0]
                    char_name   = _read_string_by_obj_id(data, name_obj_id)
                return owned_list_id, hand_list_id, char_name
        idx += 1


def _find_list_record(data, list_obj_id):
    """Return (items_array_obj_id, size, size_offset) for a List<int>."""
    pat = bytes([0x01]) + struct.pack("<I", list_obj_id)
    idx = data.find(pat)
    if idx == -1 or data[idx + 9] != 0x09:
        return None, 0, 0
    items_ref   = struct.unpack_from("<I", data, idx + 10)[0]
    size        = struct.unpack_from("<I", data, idx + 14)[0]
    size_offset = idx + 14
    return items_ref, size, size_offset


def _find_array_record(data, array_obj_id):
    """Return (offset, capacity) for an ArraySinglePrimitive."""
    pat = bytes([0x0F]) + struct.pack("<I", array_obj_id)
    idx = data.find(pat)
    if idx == -1:
        return None, 0
    capacity = struct.unpack_from("<I", data, idx + 5)[0]
    return idx, capacity


def read_list(data, list_obj_id):
    """Read all int values from a List<int>. Returns (ids, arr_offset, size_offset, capacity)."""
    items_ref, size, size_offset = _find_list_record(data, list_obj_id)
    if items_ref is None:
        return [], None, None, 0
    arr_offset, capacity = _find_array_record(data, items_ref)
    if arr_offset is None:
        return [], None, None, 0
    ids = [
        struct.unpack_from("<i", data, arr_offset + 10 + j * 4)[0]
        for j in range(size)
    ]
    return ids, arr_offset, size_offset, capacity


def write_list(data, list_obj_id, new_ids):
    """Write new_ids into a List<int> in-place. Returns error string or None."""
    items_ref, _size, size_offset = _find_list_record(data, list_obj_id)
    if items_ref is None:
        return "Could not locate list record in save data."
    arr_offset, capacity = _find_array_record(data, items_ref)
    if arr_offset is None:
        return "Could not locate array record in save data."
    if len(new_ids) > capacity:
        return (
            f"Cannot write {len(new_ids)} entries — "
            f"array capacity is only {capacity}."
        )
    for j, v in enumerate(new_ids):
        struct.pack_into("<i", data, arr_offset + 10 + j * 4, v)
    struct.pack_into("<i", data, size_offset, len(new_ids))
    return None


# ── Main application ───────────────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gloomhaven Card Editor")
        self.minsize(700, 420)
        self.filepath = None
        self.raw      = None   # bytearray of loaded file
        # tab_name -> {"owned": [int], "hand": [int], "owned_cap": int,
        #              "hand_list_id": int, "owned_list_id": int, "_not_owned_ids": []}
        self.state = {}
        self.tabs  = {}
        self._build_ui()

    # ── UI construction ────────────────────────────────────────────────────

    def _build_ui(self):
        bar = ttk.Frame(self, padding=(8, 6))
        bar.pack(fill=tk.X)

        ttk.Button(bar, text="Open .dat…", command=self._open).pack(side=tk.LEFT)
        self.lbl_file = ttk.Label(bar, text="No file loaded.", foreground="grey")
        self.lbl_file.pack(side=tk.LEFT, padx=10)
        ttk.Button(bar, text="Save",   command=self._save).pack(side=tk.RIGHT)
        ttk.Button(bar, text="Revert", command=self._revert).pack(side=tk.RIGHT, padx=(0, 6))

        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X)

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    def _show_open_hint(self):
        """Show a compact reference window explaining where save files usually live."""
        dlg = tk.Toplevel(self)
        dlg.title("Find Your Save File")
        dlg.transient(self)
        dlg.resizable(False, False)
        dlg.attributes("-topmost", True)

        outer = ttk.Frame(dlg, padding=14)
        outer.pack(fill=tk.BOTH, expand=True)

        body_font = tkfont.nametofont("TkDefaultFont").copy()
        body_font.configure(size=max(9, body_font.cget("size") - 1))

        ttk.Label(
            outer,
            text=_open_hint_message(),
            justify=tk.LEFT,
            wraplength=620,
            font=body_font,
        ).pack(fill=tk.BOTH, expand=True)

        btn_row = ttk.Frame(outer, padding=(0, 10, 0, 0))
        btn_row.pack(fill=tk.X)
        ttk.Button(btn_row, text="Close", command=dlg.destroy).pack(side=tk.RIGHT)

        dlg.update_idletasks()
        x = self.winfo_rootx() + max(20, (self.winfo_width() - dlg.winfo_width()) // 2)
        y = self.winfo_rooty() + max(20, (self.winfo_height() - dlg.winfo_height()) // 3)
        dlg.geometry(f"+{x}+{y}")
        return dlg

    def _build_tab(self, name, cards):
        """Dynamically add a character tab. `name` is the display name."""
        card_lookup = {c[0]: (c[1], c[2]) for c in cards}

        outer = ttk.Frame(self.nb, padding=8)
        self.nb.add(outer, text=name)

        # Not Owned column
        not_owned_lf = ttk.LabelFrame(outer, text="Not Owned", padding=6)
        not_owned_lf.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        not_owned_lb = tk.Listbox(
            not_owned_lf, selectmode=tk.EXTENDED, activestyle="none", width=30
        )
        sb1 = ttk.Scrollbar(not_owned_lf, orient=tk.VERTICAL, command=not_owned_lb.yview)
        not_owned_lb.configure(yscrollcommand=sb1.set)
        sb1.pack(side=tk.RIGHT, fill=tk.Y)
        not_owned_lb.pack(fill=tk.BOTH, expand=True)

        # Buttons
        btn_col = ttk.Frame(outer, padding=(6, 0))
        btn_col.pack(side=tk.LEFT, anchor=tk.CENTER)
        ttk.Button(
            btn_col, text="Own >>",
            command=lambda n=name: self._add_owned(n),
        ).pack(pady=6)
        ttk.Button(
            btn_col, text="<< Unown",
            command=lambda n=name: self._remove_owned(n),
        ).pack(pady=6)

        # Owned column
        owned_lf = ttk.LabelFrame(outer, text="Owned", padding=6)
        owned_lf.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        owned_lb = tk.Listbox(
            owned_lf, selectmode=tk.EXTENDED, activestyle="none", width=34
        )
        sb2 = ttk.Scrollbar(owned_lf, orient=tk.VERTICAL, command=owned_lb.yview)
        owned_lb.configure(yscrollcommand=sb2.set)
        sb2.pack(side=tk.RIGHT, fill=tk.Y)
        owned_lb.pack(fill=tk.BOTH, expand=True)

        status_var = tk.StringVar()
        ttk.Label(owned_lf, textvariable=status_var, foreground="grey").pack(
            anchor=tk.W, pady=(4, 0)
        )

        self.tabs[name] = {
            "card_lookup":  card_lookup,
            "not_owned_lb": not_owned_lb,
            "owned_lb":     owned_lb,
            "owned_lf":     owned_lf,
            "status_var":   status_var,
        }

    def _clear_tabs(self):
        for child in list(self.nb.winfo_children()):
            child.destroy()
        self.tabs.clear()
        self.state.clear()

    # ── State helpers ──────────────────────────────────────────────────────

    def _card_label(self, card_id, lookup):
        if card_id in lookup:
            cname, level = lookup[card_id]
            return f"[{level:>2}]  {cname}"
        return f"[ ?]  Unknown  (ID {card_id})"

    def _refresh_tab(self, name):
        tab = self.tabs[name]
        st  = self.state[name]
        lookup    = tab["card_lookup"]
        owned_set = set(st["owned"])
        hand_set  = set(st["hand"])

        not_owned = [cid for cid in sorted(lookup) if cid not in owned_set]
        tab["not_owned_lb"].delete(0, tk.END)
        for cid in not_owned:
            tab["not_owned_lb"].insert(tk.END, self._card_label(cid, lookup))
        st["_not_owned_ids"] = not_owned

        tab["owned_lb"].delete(0, tk.END)
        for cid in st["owned"]:
            label = self._card_label(cid, lookup)
            if cid in hand_set:
                label += "  *"
            tab["owned_lb"].insert(tk.END, label)

        in_hand   = sum(1 for cid in st["owned"] if cid in hand_set)
        cap       = st["owned_cap"]
        tab["status_var"].set(
            f"Owned: {len(st['owned'])} / {cap} slots  |  In hand loadout: {in_hand}"
        )
        tab["owned_lf"].config(text="Owned")

    def _add_owned(self, name):
        tab = self.tabs[name]
        st  = self.state[name]
        sel = tab["not_owned_lb"].curselection()
        if not sel:
            return
        to_add = [st["_not_owned_ids"][i] for i in sel]
        if len(st["owned"]) + len(to_add) > st["owned_cap"]:
            messagebox.showwarning(
                "Capacity Full",
                f"Cannot add {len(to_add)} card(s).\n"
                f"Array capacity: {st['owned_cap']}, used: {len(st['owned'])}.",
            )
            return
        st["owned"].extend(to_add)
        self._refresh_tab(name)

    def _remove_owned(self, name):
        tab = self.tabs[name]
        st  = self.state[name]
        sel = tab["owned_lb"].curselection()
        if not sel:
            return
        removing  = {st["owned"][i] for i in sel}
        purged    = [cid for cid in removing if cid in set(st["hand"])]
        st["owned"] = [cid for i, cid in enumerate(st["owned"]) if i not in set(sel)]
        st["hand"]  = [cid for cid in st["hand"] if cid not in removing]
        if purged:
            lookup = tab["card_lookup"]
            names  = ", ".join(
                lookup[c][0] if c in lookup else str(c) for c in purged
            )
            messagebox.showinfo(
                "Hand Updated",
                f"Also removed from hand loadout:\n{names}",
            )
        self._refresh_tab(name)

    # ── File I/O ───────────────────────────────────────────────────────────

    def _load_state(self):
        self._clear_tabs()
        errors = []

        for char_id_str, (class_name, cards) in CLASS_REGISTRY.items():
            owned_list_id, hand_list_id, char_name = find_character_list_ids(
                self.raw, char_id_str
            )
            if owned_list_id is None:
                continue  # class not present in this save

            # Keep tab labels consistent for all imported characters.
            display_name = char_name.strip() if char_name else class_name
            tab_name = f"{display_name} ({class_name})"

            self._build_tab(tab_name, cards)

            owned, _, _, owned_cap = read_list(self.raw, owned_list_id)
            hand,  _, _, _         = read_list(self.raw, hand_list_id)

            if owned_cap == 0:
                errors.append(f"{tab_name}: could not parse owned card list.")

            self.state[tab_name] = {
                "owned":         owned,
                "hand":          hand,
                "owned_cap":     owned_cap,
                "owned_list_id": owned_list_id,
                "hand_list_id":  hand_list_id,
                "_not_owned_ids": [],
            }
            self._refresh_tab(tab_name)

        if not self.tabs:
            messagebox.showwarning(
                "No Characters Found",
                "No recognised Gloomhaven characters were found in this save file.",
            )
        elif errors:
            messagebox.showwarning(
                "Parse Warning",
                "Some data could not be read:\n" + "\n".join(errors),
            )

    def _open(self):
        hint = self._show_open_hint()
        try:
            path = filedialog.askopenfilename(
                title="Open Gloomhaven Save File",
                filetypes=[("DAT files", "*.dat"), ("All files", "*.*")],
                initialdir=_first_existing_dir(_candidate_save_dirs()),
            )
        finally:
            if hint.winfo_exists():
                hint.destroy()
        if not path:
            return
        try:
            with open(path, "rb") as f:
                self.raw = bytearray(f.read())
        except OSError as e:
            messagebox.showerror("Open Failed", str(e))
            return
        self.filepath = path
        self.lbl_file.config(text=os.path.basename(path), foreground="black")
        self._load_state()

    def _revert(self):
        if self.raw is None:
            return
        if messagebox.askyesno("Revert", "Discard all unsaved changes and reload from file?"):
            self._load_state()

    def _save(self):
        if self.raw is None:
            return

        backup = self.filepath + ".bak"
        try:
            shutil.copy2(self.filepath, backup)
        except OSError as e:
            if not messagebox.askyesno(
                "Backup Failed",
                f"Could not create backup:\n{e}\n\nSave anyway?",
            ):
                return

        for tab_name, st in self.state.items():
            err = write_list(self.raw, st["owned_list_id"], st["owned"])
            if err:
                messagebox.showerror("Save Error", f"{tab_name} owned cards: {err}")
                return

            owned_set  = set(st["owned"])
            clean_hand = [cid for cid in st["hand"] if cid in owned_set]
            err = write_list(self.raw, st["hand_list_id"], clean_hand)
            if err:
                messagebox.showerror("Save Error", f"{tab_name} hand loadout: {err}")
                return
            st["hand"] = clean_hand

        try:
            with open(self.filepath, "wb") as f:
                f.write(self.raw)
        except OSError as e:
            messagebox.showerror("Save Failed", str(e))
            return

        messagebox.showinfo(
            "Saved",
            f"File saved successfully.\nBackup: {os.path.basename(backup)}",
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()
