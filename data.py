import math, random

armor_adjectives = [
    "durable",
    "sturdy",
    "resilient",
    "heavy",
    "lightweight",
    "reinforced",
    "imposing",
    "gleaming",
    "shiny",
    "polished",
    "ornate",
    "simple",
    "intricate",
    "decorative",
    "protective",
    "indestructible",
    "formidable",
    "battle-worn",
    "spiked",
    "hardened",
    "plate",
    "leather",
    "flexible",
    "heavy-duty",
    "glimmering",
    "enchanted",
    "runic",
    "sacred",
    "ethereal",
    "resistant",
    "insulated",
    "thick",
    "layered",
    "armored",
    "reinforced",
    "fortified",
    "resplendent",
    "tough",
    "sleek",
    "metallic",
    "riveted",
    "chiseled",
    "scarred",
    "adaptable",
    "immaculate",
    "battle-ready",
    "weathered",
    "custom",
    "magicked",
    "ancient",
    "mythic",
    "unyielding",
    "combat-ready",
    "heavy-duty",
    "sharp-edged",
    "bladed",
    "scaled",
    "enigmatic",
    "fireproof",
    "shockproof",
    "cute",
    "repaired"
]

class Spell:
    def __init__(self, name: str, cost: int, procs: int, dmgStat: str, hitStat: str, damageRecoil: float = 0, ignoreEnemyDEF: bool = False, victimEffect: str = "pass", selfEffect: str = "pass", description: str = "This is a spell.", tags: list = []):
        self.name = name
        # spell's MP cost
        self.cost = cost
        # number of times the spell hits
        self.procs = procs
        # the stat that the spell will use to calculate damage
        self.dmgStat = dmgStat
        # the stat that the spell will use to calculate hit chance
        self.hitStat = hitStat
        # multiplier of the damage that the player will take when compared to you the damage you deal
        self.damageRecoil = damageRecoil
        # if the attack should ignore the enemy's defense when calculating damage
        self.ignoreEnemyDEF = ignoreEnemyDEF
        # code to execute if the victim was hit by the spell
        self.victimEffect = victimEffect
        # code to execute after casting the spell (regardless of hitting)
        self.selfEffect = selfEffect
        # spell description, duh
        self.description = description
        # list of tags for future use
        self.tags = tags

class Item:
    def __init__(self, name:str, code:str, minLevel:int, usableOutsideCombat:bool = False):
        self.name = name
        self.code = code
        self.minLevel = minLevel
        self.usableOutsideCombat = usableOutsideCombat

class Modifier:
    def __init__ (self, name:str, code:str):
        self.name = name
        self.code = code

class Equipment:
    def __init__(self, name:str, slot: str, BonusHP: int, BonusMP: int, BonusSTR: int, BonusDEX: int, BonusDEF: int, BonusAGI: int, onTurnStart: list, onAttack: list, onCast: list, onHit: list, onHurt: list):
        self.name = name
        self.slot = slot
        self.HP = BonusHP
        self.MP = BonusMP
        self.STR = BonusSTR
        self.DEX = BonusDEX
        self.DEF = BonusDEF
        self.AGI = BonusAGI
        
        self.onTurnStart = onTurnStart
        self.onAttack = onAttack
        self.onCast = onCast
        self.onHit = onHit
        self.onHurt = onHurt

class Blessing:
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code

class Status:
    def __init__(self, name: str, fadeChance: float, affectOnApply: bool, effect: str, reverseEffect: str):
        # status effect's name
        self.name = name
        # chance for the status effect to disappear from the entity at the end of their turn
        self.fadeChance = fadeChance
        # if the status should proc when applied, and nothing afterwards
        self.affectOnApply = affectOnApply 
        self.effect = effect # to be exec()'d
        self.reverseEffect = reverseEffect  # to be exec()'d

class Entity:
    def __init__(self, name: str, HP: int, MP: int, STR: int, DEX: int, DEF: int, AGI: int, spells: list,
     inventory: dict = {}, gold: int = 0, blessings: list = [], onTurnStart: list = [], onAttack: list = [], 
     onCast: list = [], onHit: list = [], onHurt: list = []
     ):
        self.level = 1
        # experience points
        self.XP = 0
        self.MaxXP = 10
        # entity's name ("you" if player)
        self.name = name
        # health points
        self.HP = HP
        self.MaxHP = HP
        # mana points
        self.MP = MP
        self.MaxMP = MP
        # strength, dexterity, defense, agility
        self.STR = STR
        self.DEX = DEX
        self.DEF = DEF
        self.AGI = AGI
        # spells the entity has
        self.spells = spells
        # status effects currently applied to the entity
        self.status = [ ]
        # passive effects
        self.blessings = blessings
        # items held by the entity
        self.inventory = inventory
        # MONEYYYYY
        self.gold = gold
        # armor held by the entity
        self.heldarmors = {}
        # equipped items
        self.equipped = {
            "weapon": None,
            "helmet": None,
            "chestplate": None,
            "boots": None,
            "charm": None
        }
        # combat conditionals, default blank, all will be exec()'d
        self.onTurnStart = onTurnStart
        self.onAttack = onAttack
            # for enemies, onCast is NEVER used, use onAttack instead
        self.onCast = onCast
            # note: onHit and onHurt are executed in castSpell, when about the other target use "victim" and for self, use "caster"
        self.onHit = onHit
        self.onHurt = onHurt
    
    def equip(self, armor:Equipment, slot:str):
        subtract = lambda x, y: x - y
        def diff(input1, input2):
            return str(subtract(input1, input2))
        
        savedMaxHP = self.MaxHP
        savedMaxMP = self.MaxMP
        savedSTR = self.STR
        savedDEX = self.DEX
        savedDEF = self.DEF
        savedAGI = self.AGI

        self.equipped[slot] = armor

        self.HP += armor.HP
        self.MaxHP += armor.HP
        self.HP += armor.MP
        self.MaxMP += armor.MP
        self.STR += armor.STR
        self.DEX += armor.DEX
        self.DEF += armor.DEF
        self.DEF += armor.AGI

        self.onTurnStart += armor.onTurnStart
        self.onAttack += armor.onAttack
        self.onCast += armor.onCast
        self.onHit += armor.onHit
        self.onHurt += armor.onHurt

        print("\nHP: " + diff(self.MaxHP, savedMaxHP))
        print("MP: " + diff(self.MaxMP, savedMaxMP))
        print("STR: " + diff(self.STR,savedSTR))
        print("DEX: " + diff(self.DEX,savedDEX))
        print("DEF: " + diff(self.DEF,savedDEF))
        print("AGI: " + diff(self.AGI,savedAGI))

        if self.HP > self.MaxHP: self.HP = self.MaxHP
        if self.MaxHP < 0: print("warning: your max hp is less than 0! increase your max hp and heal, or you'll die after your next turn")
        if self.HP < 0: print("warning: your hp is less than 0! heal before you go into your next fight, or you'll die after your next turn")

    def unequip(self, slot:str):
        subtract = lambda x, y: x - y
        def diff(input1, input2):
            return str(subtract(input1, input2))

        savedMaxHP = self.MaxHP
        savedMaxMP = self.MaxMP
        savedSTR = self.STR
        savedDEX = self.DEX
        savedDEF = self.DEF
        savedAGI = self.AGI

        armor = self.equipped[slot]

        self.MaxHP -= armor.HP
        if self.HP > self.MaxHP: self.HP = self.MaxHP
        self.MaxMP -= armor.MP
        if self.MP > self.MaxMP: self.MP = self.MaxMP
        self.STR -= armor.STR
        self.DEX -= armor.DEX
        self.DEF -= armor.DEF
        self.DEF -= armor.AGI

        for code in armor.onTurnStart:
            self.onTurnStart.remove(code)
        for code in armor.onAttack:
            self.onAttack.remove(code)
        for code in armor.onTurnStart:
            self.onCast.remove(code)
        for code in armor.onHit:
            self.onHit.remove(code)
        for code in armor.onHurt:
            self.onHurt.remove(code)

        print("\nHP: " + diff(self.MaxHP, savedMaxHP))
        print("MP: " + diff(self.MaxMP, savedMaxMP))
        print("STR: " + diff(self.STR,savedSTR))
        print("DEX: " + diff(self.DEX,savedDEX))
        print("DEF: " + diff(self.DEF,savedDEF))
        print("AGI: " + diff(self.AGI,savedAGI))

        if self.HP > self.MaxHP: self.HP = self.MaxHP
        if self.MaxHP < 0: print("warning: your max hp is less than 0! you will die after your next turn if you don't increase your max hp and rest")
        if self.HP < 0: print("warning: your hp is less than 0! heal before you go into your next fight, or you'll die after your next turn")

    def generateEquip(self, player, perks:int = 0, quirks:int = 0, slot:str = 'random'):
        statups = round((self.STR + self.DEX + self.DEF + self.AGI)/3)
        if slot == 'random':
            slot = random.choice(['weapon','helmet','chestplate','boots','charm'])
        name = random.choice(armor_adjectives) + " " + slot + " of the " + self.name
        while (name in self.inventory.keys() or name in self.equipped.values()):
            name = random.choice(armor_adjectives) + slot + " of the " + self.name
        # bonusHP = statups/max(math.ceil(baseHealth/(10-(2*perks)+(2*quirks))), 1)
        # if bonusHP < 0:
        #     override = bonusHP
        #     bonusHP = 1
        # else:
        #     override = 0
        # bonusHP = round(log(bonusHP) + override)
        bonusHP = math.ceil(math.log(self.MaxHP, 2) * player.level * random.normalvariate(0.65,0.2))
        list_of_things = [0, 0, 0, 0, 0]
        for _ in range(statups):
            index = -1
            a = random.randint(0,4)
            for _ in list_of_things:
                index += 1
                if a == index: 
                    list_of_things[index] += random.randint(1,2) 
        bonusMP = list_of_things[0]
        bonusSTR = list_of_things[1]
        bonusDEX = list_of_things[2]
        bonusDEF = list_of_things[3]
        bonusAGI = list_of_things[4]

        onTurnStart = []
        onAttack = []
        onHit = []
        onCast = []
        onHurt = []
        for _ in list(range(perks)):
            onWhat = random.choice("onTurnStart", "onAttack", "onCast", "onHit", "onHurt")
            doWhat = random.choice(
                "hurt = math.ceil(enemy.MaxHP / 30)\nenemy.HP -= hurt\nprint('the' + enemy.name + 'took ' + str(heal) + ' damage')",
                "heal = math.ceil(player.MaxHP / 25)\nplayer.HP += heal\nprint('you healed ' + str(heal) + ' hp')\nif(player.HP > player.MaxHP): player.HP = player.MaxHP",
                "player.HP -= 2\nenemy.HP -= 10\nprint('you took 2 damage')\nprint('the ' + enemy.name + ' took 10 damage)",
                "applyEffect('STR down', enemy)",
                "applyEffect('DEX down', enemy)",
                "applyEffect('DEF down', enemy)",
                "applyEffect('AGI down', enemy)",
                "applyEffect('STR up', player)",
                "applyEffect('DEX up', player)",
                "applyEffect('DEF up', player)",
                "applyEffect('AGI up', player)",
                "if randint(1,10) == 1: applyEffect('poison', enemy)",
                "if randint(1,10) == 1: applyEffect('burn', enemy)"
            )
            exec(onWhat + ".append(" + doWhat +")")
        for _ in list(range(quirks)):
            onWhat = random.choice("onTurnStart", "onAttack", "onCast", "onHit", "onHurt")
            doWhat = random.choice(
                "hurt = math.ceil(player.MaxHP / 25)\nplayer.HP -= hurt\nprint('you took ' + str(hurt) + ' damage')\nif(player.HP > player.maxHP): player.HP = player.MaxHP", 
                "heal = math.ceil(enemy.MaxHP / 25)\nenemy.HP += heal\nprint('the' + enemy.name + 'healed ' + str(heal) + ' hp')\nif(enemy.HP > enemy.maxHP): enemy.HP = enemy.MaxHP"
                "applyEffect('STR up', enemy)",
                "applyEffect('DEX up', enemy)",
                "applyEffect('DEF up', enemy)",
                "applyEffect('AGI up', enemy)",
                "applyEffect('STR down', player)",
                "applyEffect('DEX down', player)",
                "applyEffect('DEF down', player)",
                "applyEffect('AGI down', player)",
                "if randint(1,10) == 1: applyEffect('poison', player)",
                "if randint(1,10) == 1: applyEffect('burn', player)"
            )
            exec(onWhat + ".append(" + doWhat +")")
        return Equipment(name, slot, round(bonusHP), round(bonusMP), round(bonusSTR), round(bonusDEX), round(bonusDEF), round(bonusAGI), onTurnStart, onAttack, onCast, onHit, onHurt)
    
    # gives a status effect to an entity
    def applyStatus(self, status: str, silent:bool = False):
        status = statuses[status]
        if silent == False:
            if self.name == "you":
                print("you now have " + status.name)
            else:
                print(self.name + " now has " + status.name)
        self.status += [status]
        if status.affectOnApply:
            exec(status.effect)

    # removes a status effect from an entity
    def removeStatus(self, status: Status, silent:bool = False):
        if status in self.status: 
            statusIndex = self.status.index(status)
            if len(self.status) > 1: firstHalf = self.status[:statusIndex]
            else: firstHalf = []
            secondHalf = self.status[statusIndex:]
            secondHalf.reverse()
            for each in secondHalf: exec(each.reverseEffect)
            secondHalf.reverse()    
            removed = secondHalf.pop(0)
            exec(removed.reverseEffect)
            if silent == False:
                if self.name == "you":
                    print("you no longer have " + status.name)
                else:
                    print(status.name + " faded from the " + self.name)
            for each in secondHalf:
                self.applyStatus(each.name, True)
                firstHalf.append(each)
            self.status = firstHalf

    # causes a status effect to execute it's effect
    def tickStatus(self, status: Status, doFadeChance:bool = True):
        if status.affectOnApply == False:
            exec(status.effect)
            if doFadeChance and status.fadeChance >= random.uniform(0,1):
                self.removeStatus(status)

    def addBlessing(self, blessing: Blessing):
        self.blessings += [blessing]
        exec(blessing.code)

spells = {
    # melee attacks
    "attack": Spell("attack", 0, 1, "caster.STR", "caster.DEX", 0, False, "pass", "pass", "A basic attack, known by most.", ["melee", "basic"]),
    "doublecut": Spell("doublecut", 5, 2, "caster.STR", "caster.DEX", 0, False, "pass", "pass", "The caster attacks twice in quick succession.", ['melee']),
    "tricut": Spell("tricut", 8, 3, "caster.STR", "caster.DEX", 0, False, "pass", "pass", "The caster attacks thrice in quick succession.", ['melee']),
    "swift strike": Spell("swift strike", 5, 1, "caster.AGI", "caster.AGI", 0, False, "pass", "pass", "The user strikes quickly at their opponent, dealing damage proportional to AGI.", ['melee']),
    "bite": Spell("bite", 2, 1, "caster.STR * .5", "caster.STR", 0, False, "victim.applyStatus('poison')", "pass", "The user bites down on their opponent, inflicting poison.", ['melee', 'debuff']),
    
    # spells
    "bolt": Spell("bolt", 5, 1, "caster.MP", "caster.AGI", 0, False, "pass", "pass", "Cast a small bolt of mana at the user's foe, dealing damage equal to their current MP, before MP deduction.", ['spell']),
    "bolt volley": Spell("bolt volley", 15, 5, "caster.MP", "caster.AGI / 1.5", 0, False, "pass", "pass", "The user casts 'bolt' five times in quick succession with reduced accuracy.", ['spell']),
    "flame": Spell("flame", 5, 1, "caster.DEF", "caster.DEX", 0, False, "victim.applyStatus('burn')", "pass", "Fire a small flame at the user's foe, dealing damage and burning them.", ['spell', 'debuff']),
    "fireball": Spell("fireball", 15, 1, "caster.DEF * 3", "caster.DEX", .25, False, "victim.applyStatus('burn')", "pass", "Summon a large fireball, dealing damage equal to 3 times the caster's DEF and burning the user's foe, but hurts the caster in the process.", ['spell', 'debuff', 'recoil']),
    "nuke": Spell("nuke", 100784, 999, "caster.MaxHP * 99999", math.inf, 0, True, "pass", "pass", "An ancient magic, long lost to time. Requires a unfeasible amount of mana to cast, but is sure to obliterate any foe that opposes its user.", ['spell']),
    "doom": Spell("doom", 100, 1, "0", "math.inf", 0, False, "victim.applyStatus('impending doom')", "pass", "...", ['spell', 'debuff']),

    # buffs
    "warcry": Spell("warcry", 6, 1, "0", "math.inf", 0, True, "pass", "caster.applyStatus('STR up')", "The caster makes a loud battle cry, increasing the their STR by 20%.", ['buff']),
    "foresee": Spell("foresee", 6, 1, "0", "math.inf", 0, True, "pass", "caster.applyStatus('DEX up')", "Focuses the caster's mind on their opponent's movements, increasing the user's DEX by 20%.", ['buff']),
    "protection": Spell("protection", 6, 1, "0", "math.inf", 0, True, "pass", "caster.applyStatus('DEF up')", "The caster puts their guard up, increasing their DEF by 20%.", ['buff']),
    "evasion": Spell("evasion", 6, 1, "0", "math.inf", 0, True, "pass", "caster.applyStatus('AGI up')", "Become ready to dodge at a moment's notice, increasing the caster's AGI by 20%.", ['buff']),
    "bunny": Spell("bunny", 9, 1, "0", "math.inf", 0, True, "pass", "caster.applyStatus('bunny')", f"Magically transforms the user into a bunny, cutting their STR by 87.5% in exchange for 4 times the AGI.", ['buff']),

    # debuffs
    "threaten": Spell("threaten", 6, 1, "0", "math.inf", 0, True, "victim.applyStatus('STR down')", "pass", "The caster threatens their opponent, decreasing the victim's STR by 20%.", ['debuff']),
    "slow": Spell("slow", 6, 1, "0", "math.inf", 0, True, "victim.applyStatus('DEX down')", "pass", "Slows down the caster's foe, decreasing their DEX by 20%.", ['debuff']),
    "exploit": Spell("exploit", 6, 1, "0", "math.inf", 0, True, "victim.applyStatus('DEF down')", "pass", "Finds a weakness in the caster's foe, decreasing their DEF by 20%.", ['debuff']),
    "trip": Spell("trip", 6, 1, "0", "math.inf", 0, True, "victim.applyStatus('AGI down')", "pass", "Trips up the user's foe, lowering their AGI by 20%.", ['debuff']),

    # healing & other
    "bravery": Spell("bravery", 5, 1, "caster.DEF", "math.inf", -1, True, "pass", "pass", "Grants the caster a surge of determination, restoring health equal to the caster's DEF.", ['heal']),
    "courage": Spell("courage", 15, 2, "caster.DEF", "math.inf", -1.5, True, "pass", "pass", "Channels the caster's resolve into healing their wounds, restoring HP equal to 1.5 times the caster's DEF.", ['heal']),
    "valor": Spell("valor", 45, 3, "caster.DEF", "math.inf", -2, True, "pass", "if(random.randint(1,2) == 1): caster.applyStatus('DEF up')", "The caster steels themself with unwavering valor, healing HP equal to 2 times the caster's DEF.", ['heal']),
    "cleanse": Spell("cleanse", 8, 1, "0", "math.inf", 0, True, "pass", "print('you have been cleansed of all statuses')\nfor each in caster.status: caster.removeStatus(each, True)", "Cleanses the user of all status effects, including buffs.")
}

items = {
    # healing
    "small heal": Item("small heal", "print('you sip the small healing potion')\nplayer.HP += 10\nprint('you heal 10 HP')", 1, True),
    "medium heal": Item("medium heal", "print('you drink the medium healing potion')\nplayer.HP += 50\nprint('you heal 50 HP')", 4, True),
    "large heal": Item("large heal", "print('you chug the large healing potion')\nplayer.HP += 100\nprint('you heal 100 HP')", 10, True),
    "massive heal": Item("massive heal", "print('you reluctantly gulp down the massive healing potion...')\nplayer.HP += 200\nprint('you heal 200 HP')", 20, True),
    "panacea": Item("panacea", """
print('you savor the panacea')
for each in player.status:
    removeStatus(each, player, True)
print('you are cured of all statuses')""", 2, True),

    # mana regen
    "small mana": Item("small mana", "print('you sip the small mana potion')\nplayer.MP += 5\nprint('you gain 5 MP')", 1, True),
    "medium mana": Item("medium mana", "print('you drink the medium mana potion')\nplayer.MP += 20\nprint('you gain 20 MP')", 5, True),
    "large mana": Item("large mana", "print('you chug the large mana potion')\nplayer.MP += 50\nprint('you gain 50 MP')", 10, True),
    "massive mana": Item("massive mana", "print('you reluctantly gulp down the massive mana potion...')\nplayer.MP += 100\nprint('you gain 100 MP')", 20, True),
    
    # tonics
    "pepper tonic": Item("pepper tonic", "print('you drink the pepper tonic... spicy!')\napplyStatus('STR up', player, False)", 1),
    "carrot tonic": Item("carrot tonic", "print('you drink the carrot tonic... tastes like carrots.')\napplyStatus('DEX up', player, False)", 1),
    "ginger tonic": Item("ginger tonic", "print('you drink the ginger tonic... so bitter!')\napplyStatus('DEF up', player, False)", 1),
    "wind tonic": Item("wind tonic", """print("you drink the wind tonic... it's empty..?")\napplyStatus('AGI up', player, False)""", 1),

    # weapons
    "throwing knife": Item("throwing knife", "ouch = max(round((player.STR+player.DEX)/2), 1)\nenemy.HP -= ouch\nprint(f'you huck the throwing knife at the {enemy.name} for {ouch} damage')",2)
}

perks = {

}

quirks = {

}

blessings = {
    # on turn start
    "enraged": Blessing("enraged", """self.onTurnStart.append("applyStatus('STR up')")""", ), # "player." / "enemy." will be concat. with string before execution
    "focused": Blessing("focused", """self.onTurnStart.append("applyStatus('DEX up')")"""),
    "fortified": Blessing("fortified", """self.onTurnStart.append("applyStatus('DEF up')")"""),
    "nimble": Blessing("nimble", """self.onTurnStart.append("applyStatus('AGI up')")"""),
}

statuses = {
    # stat buffs
    "STR up": Status("STR up", 0, True, "self.STR *= 6/5\nself.STR = math.ceil(self.STR)", "self.STR /= 6/5\nself.STR = math.floor(self.STR)"),
    "DEX up": Status("DEX up", 0, True, "self.DEX *= 6/5\nself.DEX = math.ceil(self.DEX)", "self.DEX /= 6/5\nself.DEX = math.floor(self.DEX)"),
    "DEF up": Status("DEF up", 0, True, "self.DEF *= 6/5\nself.DEF = math.ceil(self.DEF)", "self.DEF /= 6/5\nself.DEF = math.floor(self.DEF)"),
    "AGI up": Status("AGI up", 0, True, "self.AGI *= 6/5\nself.AGI = math.ceil(self.AGI)", "self.AGI /= 6/5\nself.AGI = math.floor(self.AGI)"),
    "bunny": Status("bunny", .10, True, "self.AGI *= 4\nself.AGI = math.ceil(self.AGI)\nself.STR /= 8\nself.STR = math.floor(self.STR)", "self.AGI /= 4\nself.AGI = math.floor(self.AGI)\nself.STR *= 8\nself.STR = math.ceil(self.STR)"),

    "STR up 1": Status("STR up 1", 0, True, "self.STR += 1", "self.STR -= 1"),
    "DEX up 1": Status("DEX up 1", 0, True, "self.DEX += 1", "self.DEX -= 1"),
    "DEF up 1": Status("DEF up 1", 0, True, "self.DEF += 1", "self.DEF -= 1"),
    "AGI up 1": Status("AGI up 1", 0, True, "self.AGI += 1", "self.AGI -= 1"),

    # stat debuffs
    "STR down": Status("STR down", 0, True, "self.STR /= 6/5\nself.STR = math.floor(self.STR)", "self.STR *= 6/5\nself.STR = math.ceil(self.STR)"),
    "DEX down": Status("DEX down", 0, True, "self.DEX /= 6/5\nself.DEX = math.floor(self.DEX)", "self.DEX *= 6/5\nself.DEX = math.ceil(self.DEX)"),
    "DEF down": Status("DEF down", 0, True, "self.DEF /= 6/5\nself.DEF = math.floor(self.DEF)", "self.DEF *= 6/5\nself.DEF = math.ceil(self.DEF)"),
    "AGI down": Status("AGI down", 0, True, "self.AGI /= 6/5\nself.AGI = math.floor(self.AGI)", "self.AGI *= 6/5\nself.AGI = math.ceil(self.AGI)"),

    "STR down 1": Status("STR down 1", 0, True, "self.STR -= 1", "self.STR += 1"),
    "DEX down 1": Status("DEX down 1", 0, True, "self.DEX -= 1", "self.DEX += 1"),
    "DEF down 1": Status("DEF down 1", 0, True, "self.DEF -= 1", "self.DEF += 1"),
    "AGI down 1": Status("AGI down 1", 0, True, "self.AGI -= 1", "self.AGI += 1"),

    # DOT effects
    "burn": Status("burn", .25, False, """
burndmg = math.ceil(self.MaxHP / 18)
if self.name == "you":
    print('you took ' + str(burndmg) + ' damage from burn')
else:
    print('the ' + self.name + ' took ' + str(burndmg) + ' damage from burn')
self.HP -= burndmg
del burndmg""", "pass"),

    "poison": Status("poison", .1, False, """
burndmg = math.ceil(self.MaxHP / 20)
if self.name == "you":
    print('you took ' + str(burndmg) + ' damage from poison')
else:
    print('the ' + self.name + ' took ' + str(burndmg) + ' damage from poison')
self.HP -= burndmg
del burndmg""", "pass"),

    # other
    "impending doom": Status("impending doom", .05, False, "pass", "self.applyStatus('doom')\nself.stauses.remove('impending doom')"),
    "doom": Status("doom", 0, False, "print('death calls.')\nprint('your HP drops to 0')\nself.HP = 0", "pass"),
}

monsters = {
    # forest
    "rat": Entity("rat", 3, math.inf, 1, 0, 0, 5, ["bite"]),
    "wolf": Entity("wolf", 15, math.inf, 2, 3, 1, 1, ["attack"]),
    "spirit": Entity("spirit", 25, math.inf, 4, 5, 0, 4, ["attack", "flame"]),

    # infernal wastes
    "imp": Entity('imp', 70, math.inf, 10, 15, -5, 20, ["evasion", "attack", "flame", "threaten"]),
    "demon": Entity('demon', 100, math.inf, 20, 10, 3, 10, ["attack", "flame", "warcry", "foresee"]),
    "warg": Entity('warg', 150, math.inf, 10, 20, 10, 10, ["bite", "tricut"], {}, [], [blessings["enraged"]]),

    # what the hell
    "reaper": Entity("reaper", 666, math.inf, 100, 200, 50, 100, ["doom", "bunny", "evasion", "trip"]),
    "minor deity": Entity("minor deity", 7777, math.inf, 100, 1000, 50, 50, ["evasion"]),

    # other
    "test dummy": Entity('test dummy', 99999, math.inf, 0, 99999, 0, 0, ['bite'])
}

player = Entity("you", 20, 8, 3, 5, 0, 0, ["doublecut", "bolt", "warcry", "protection", "bravery"], { }, 30)

# data.player = Entity("you", 999999, 999999, 3, 5, 0, 0, ["doublecut", "bolt", "warcry", "protection", "bravery", "bite", "nuke"], { }, 999999999, [], ["data.player.MP = data.player.MaxMP\nprint('your MP was refilled')"])
