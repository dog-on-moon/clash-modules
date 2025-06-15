import random

from toontown.battle.BattleProps import globalPropPool
from toontown.cutscene.editor import CSEditorUtil
from toontown.cutscene.repository.CutsceneKeyEnum import CutsceneKeyEnum
from toontown.cutscene.repository.CutsceneLoader import cutsceneSetup, CutsceneLoader
from toontown.toonbase import TTLocalizer


class CutsceneSetupException(BaseException):
    pass


# region Street Mercs
# region Duck Shuffler
@cutsceneSetup(CutsceneKeyEnum.DuckShuffler_Wager_Base)
def __duckShufflerWagerSetup(editor: bool, **kwargs) -> CutsceneLoader:
    cutsceneLoader = CutsceneLoader()
    if editor:
        # Load environment and actors
        toons = CSEditorUtil.makeToons(4)
        suits = CSEditorUtil.makeSuits('duckshfl', 'duckshfl', 'duckshfl', 'duckshfl', 'duckshfl', 'duckshfl')
        room = loader.loadModel('phase_3.5/models/schoolhouse/schoolhouse_interior_basement')
        room.reparentTo(render)
        battle = render.attachNewNode('battle')
        CSEditorUtil.moveActorsToBattlePositions(toons=toons, suits=suits, newParent=battle)

        invoker = suits[0]
        eyeLandIndex = random.randint(0, 4)
        dialogue = 'TIME TO SPIN!!! (PLACEHOLDER)'
        resultSound = 'phase_5/audio/sfx/SA_wager_spin.ogg'
    else:
        invoker, battle, eyeLandIndex, dialogue, resultSound = CSEditorUtil.getKwargs(kwargs, 'invoker', 'battle', 'eyeLandIndex', 'dialogue', 'resultSound')

    # Populate cutscene loader.
    cutsceneLoader.addSuitsToCutscene([invoker])
    cutsceneLoader.addActorsToCutscene([invoker])
    cutsceneLoader.addNodesToCutscene(
        [battle, invoker, invoker.specialHead]
    )
    cutsceneLoader.addDialogueToCutscene([dialogue])
    cutsceneLoader.addSoundsToCutscene([
        'phase_5/audio/sfx/SA_wager_spin.ogg',
        resultSound
    ])
    cutsceneLoader.addArgumentsToCutscene([eyeLandIndex])
    return cutsceneLoader


@cutsceneSetup(CutsceneKeyEnum.DuckShuffler_Wager_Bar)
def __duckShufflerBarSetup(editor: bool, **kwargs) -> CutsceneLoader:
    cutsceneLoader = CutsceneLoader()
    if editor:
        # Load environment and actors
        toons = CSEditorUtil.makeToons(4)
        suits = CSEditorUtil.makeSuits('duckshfl', 'duckshfl', 'duckshfl', 'duckshfl', 'duckshfl', 'duckshfl')
        room = loader.loadModel('phase_3.5/models/schoolhouse/schoolhouse_interior_basement')
        room.reparentTo(render)
        battle = render.attachNewNode('battle')
        CSEditorUtil.moveActorsToBattlePositions(toons=toons, suits=suits, newParent=battle)
    else:
        toons, suits, battle = CSEditorUtil.getKwargs(kwargs, 'toons', 'suits', 'battle')

    # Get props for the cutscene.
    bar_a = globalPropPool.getProp("goldbar")
    bar_a.reparentTo(battle)
    bar_a.hide()
    bar_b = globalPropPool.getProp("goldbar")
    bar_b.reparentTo(battle)
    bar_b.hide()
    shadow_a = loader.loadModel("phase_3/models/props/square_drop_shadow")
    shadow_a.reparentTo(battle)
    shadow_a.hide()
    shadow_b = loader.loadModel("phase_3/models/props/square_drop_shadow")
    shadow_b.reparentTo(battle)
    shadow_b.hide()

    def cleanup():
        if editor:
            return
        bar_a.removeNode()
        bar_b.removeNode()
        shadow_a.removeNode()
        shadow_b.removeNode()

    # Populate cutscene loader.
    cutsceneLoader.addToonsToCutscene(toons, maxToonCount=4)
    cutsceneLoader.addSuitsToCutscene(suits, maxSuitCount=6)
    cutsceneLoader.addNodesToCutscene(
        [battle, bar_a, bar_b, shadow_a, shadow_b]
    )
    cutsceneLoader.addFunctionsToCutscene([cleanup])
    return cutsceneLoader


@cutsceneSetup(CutsceneKeyEnum.DuckShuffler_Wager_Beans)
def __duckShufflerBeansSetup(editor: bool, **kwargs) -> CutsceneLoader:
    cutsceneLoader = CutsceneLoader()
    if editor:
        # Load environment and actors
        toons = CSEditorUtil.makeToons(4)
        suits = CSEditorUtil.makeSuits('duckshfl', 'duckshfl', 'duckshfl', 'duckshfl', 'duckshfl', 'duckshfl')
        room = loader.loadModel('phase_3.5/models/schoolhouse/schoolhouse_interior_basement')
        room.reparentTo(render)
        battle = render.attachNewNode('battle')
        CSEditorUtil.moveActorsToBattlePositions(toons=toons, suits=suits, newParent=battle)

        toon = toons[0]
    else:
        toon, *_ = CSEditorUtil.getKwargs(kwargs, 'toon')

    # Populate cutscene loader.
    cutsceneLoader.addToonsToCutscene([toon])
    cutsceneLoader.addNodesToCutscene([toon])
    cutsceneLoader.addParticleSystemsToCutscene(["jellybeanRainFall", "jellybeanRainLand"])
    return cutsceneLoader
# endregion


@cutsceneSetup(CutsceneKeyEnum.Rainmaker_Tornado)
def __rainmakerTornadoSetup(editor: bool, **kwargs) -> CutsceneLoader:
    cutsceneLoader = CutsceneLoader()
    if editor:
        from toontown.instances.mercs.DistributedInstanceRainmaker import DistributedInstanceRainmaker
        instance = DistributedInstanceRainmaker(base.cr)
        instance.doId = -420
        instance.loadEnvironment()

        toons = CSEditorUtil.makeToons(4)
        rainmaker, *_ = CSEditorUtil.makeSuits('rainmake')
        battle = instance.battleNode
        CSEditorUtil.moveActorsToBattlePositions(toons=toons, suits=[rainmaker], newParent=battle)
    else:
        toons, rainmaker, battle = CSEditorUtil.getKwargs(kwargs, 'toons', 'rainmaker', 'battle')

    tornadoNode = battle.attachNewNode('tornadoNode')
    tornadoNode.setPos(0, -35, 0)

    tornadoNodeDeluxe = battle.attachNewNode('tornadoNodeDeluxe')
    tornadoNodeDeluxe.setPos(0, -97, 24)

    playerFunnyNode = battle.attachNewNode('playerFunnyNode')
    playerFunnyNode.setPos(0, -6, 0)

    # some stormclouds
    CSEditorUtil.populateList(toons)
    clouds = []
    dropshadows = []
    for toon in toons:
        if toon is None:
            clouds.append(None)
            dropshadows.append(None)
            continue
        cloud = loader.loadModel('phase_5.5/models/estate/bumper_cloud')
        cloud.setColorScale(0.95, 0.95, 0.95, 1.0)
        clouds.append(cloud)
        dropshadows.append(toon.dropShadow)

    # Populate cutscene loader.
    cutsceneLoader.addToonsToCutscene(toons, maxToonCount=4)
    cutsceneLoader.addSuitsToCutscene([rainmaker])
    cutsceneLoader.addActorsToCutscene([rainmaker])
    cutsceneLoader.addNodesToCutscene([rainmaker, battle, tornadoNode, playerFunnyNode] + toons + dropshadows + [
        tornadoNodeDeluxe] + clouds)
    cutsceneLoader.addParticleSystemsToCutscene(['rainmakerTornado', 'rainmakerTornado'])
    return cutsceneLoader


@cutsceneSetup(CutsceneKeyEnum.Rainmaker_ToonsComeHome)
def __rainmakerToonsComeHomeSetup(editor: bool, **kwargs) -> CutsceneLoader:
    cutsceneLoader = CutsceneLoader()
    if editor:
        from toontown.instances.mercs.DistributedInstanceRainmaker import DistributedInstanceRainmaker
        instance = DistributedInstanceRainmaker(base.cr)
        instance.doId = -420
        instance.loadEnvironment()

        toons = CSEditorUtil.makeToons(4)
        rainmaker, *_ = CSEditorUtil.makeSuits('rainmake')
        battle = instance.battleNode
        CSEditorUtil.moveActorsToBattlePositions(toons=toons, suits=[rainmaker], newParent=battle)
    else:
        toons, battle = CSEditorUtil.getKwargs(kwargs, 'toons', 'battle')
    # Populate cutscene loader.
    cutsceneLoader.addToonsToCutscene(toons, maxToonCount=4)
    cutsceneLoader.addNodesToCutscene([battle])
    return cutsceneLoader


@cutsceneSetup(CutsceneKeyEnum.Rainmaker_Ending_1)
def __rainmakerEnding1Setup(editor: bool, **kwargs) -> CutsceneLoader:
    cutsceneLoader = CutsceneLoader()
    if editor:
        from toontown.instances.mercs.DistributedInstanceRainmaker import DistributedInstanceRainmaker
        instance = DistributedInstanceRainmaker(base.cr)
        instance.doId = -420
        instance.loadEnvironment()

        toons = CSEditorUtil.makeToons(4)
        rainmaker, *_ = CSEditorUtil.makeSuits('rainmake')
        battle = instance.battleNode
        CSEditorUtil.moveActorsToBattlePositions(toons=toons, suits=[rainmaker], newParent=battle)
    else:
        rainmaker, battle, instance = CSEditorUtil.getKwargs(kwargs, 'rainmaker', 'battle', 'instance')

    # Populate cutscene loader.
    cutsceneLoader.addSuitsToCutscene([rainmaker])
    cutsceneLoader.addNodesToCutscene([battle, rainmaker])
    cutsceneLoader.addActorsToCutscene([rainmaker])
    cutsceneLoader.addDialogueToCutscene([
        "I don't get it.",
        "Even when I stayed out of everyone's way...",
        "...you still tried to hurt me.",
    ])
    return cutsceneLoader


@cutsceneSetup(CutsceneKeyEnum.Rainmaker_Ending_2)
def __rainmakerEnding2Setup(editor: bool, **kwargs) -> CutsceneLoader:
    cutsceneLoader = CutsceneLoader()
    if editor:
        from toontown.instances.mercs.DistributedInstanceRainmaker import DistributedInstanceRainmaker
        instance = DistributedInstanceRainmaker(base.cr)
        instance.doId = -420
        instance.loadEnvironment()

        toons = CSEditorUtil.makeToons(4)
        rainmaker, *_ = CSEditorUtil.makeSuits('rainmake')
        battle = instance.battleNode
        CSEditorUtil.moveActorsToBattlePositions(toons=toons, suits=[rainmaker], newParent=battle)
    else:
        rainmaker, battle, instance = CSEditorUtil.getKwargs(kwargs, 'rainmaker', 'battle', 'instance')

    def setEnvironment():
        instance.environment.request('OilRain')
        rainmaker.specialHead.setHairState(rainmaker.specialHead.OIL)

    # Populate cutscene loader.
    cutsceneLoader.addSuitsToCutscene([rainmaker])
    cutsceneLoader.addNodesToCutscene([battle, rainmaker, rainmaker.specialHead])
    cutsceneLoader.addActorsToCutscene([rainmaker])
    cutsceneLoader.addDialogueToCutscene([
        "Oh, don't play dumb with me!",
        "Lying only makes it worse.",
        "You knew what you came here to do.",
    ])
    cutsceneLoader.addFunctionsToCutscene([setEnvironment])
    return cutsceneLoader


@cutsceneSetup(CutsceneKeyEnum.Rainmaker_Ending_3)
def __rainmakerEnding3Setup(editor: bool, **kwargs) -> CutsceneLoader:
    cutsceneLoader = CutsceneLoader()
    if editor:
        from toontown.instances.mercs.DistributedInstanceRainmaker import DistributedInstanceRainmaker
        instance = DistributedInstanceRainmaker(base.cr)
        instance.doId = -420
        instance.loadEnvironment()

        toons = CSEditorUtil.makeToons(4)
        rainmaker, *_ = CSEditorUtil.makeSuits('rainmake')
        battle = instance.battleNode
        CSEditorUtil.moveActorsToBattlePositions(toons=toons, suits=[rainmaker], newParent=battle)

        instance.environment.request('OilRain')
        rainmaker.specialHead.setHairState(rainmaker.specialHead.OIL)
    else:
        rainmaker, battle, instance = CSEditorUtil.getKwargs(kwargs, 'rainmaker', 'battle', 'instance')

    def setEnvironmentA():
        instance.environment.request('HeavyRain')
        rainmaker.specialHead.setHairState(rainmaker.specialHead.HEAVY)

    def setEnvironmentB():
        instance.environment.request('StormCell')
        rainmaker.specialHead.setHairState(rainmaker.specialHead.STORM)

    startNode = rainmaker.attachNewNode('startNode')
    startNode.wrtReparentTo(battle)

    # Populate cutscene loader.
    cutsceneLoader.addSuitsToCutscene([rainmaker])
    cutsceneLoader.addNodesToCutscene([battle, rainmaker, rainmaker.specialHead, startNode])
    cutsceneLoader.addActorsToCutscene([rainmaker])
    cutsceneLoader.addDialogueToCutscene([
        "I want to be friends with you Toons.",
        "I don't see why it can't happen.",
        "But every time I try, you're mean to me!",
        "I remember I went up to this Toon named Bessie.",
        "I asked her if we could play tic-tac-toe.",
        "She tried to drop a piano on me!",
        "Why did she do that?! There was no reason!",
    ])
    cutsceneLoader.addFunctionsToCutscene([setEnvironmentA, setEnvironmentB])
    return cutsceneLoader


@cutsceneSetup(CutsceneKeyEnum.Rainmaker_Ending_4)
def __rainmakerEnding4Setup(editor: bool, **kwargs) -> CutsceneLoader:
    cutsceneLoader = CutsceneLoader()
    if editor:
        from toontown.instances.mercs.DistributedInstanceRainmaker import DistributedInstanceRainmaker
        instance = DistributedInstanceRainmaker(base.cr)
        instance.doId = -420
        instance.loadEnvironment()

        toons = CSEditorUtil.makeToons(4)
        rainmaker, *_ = CSEditorUtil.makeSuits('rainmake')
        battle = instance.battleNode
        CSEditorUtil.moveActorsToBattlePositions(toons=toons, suits=[rainmaker], newParent=battle)

        instance.environment.request('StormCell')
        rainmaker.specialHead.setHairState(rainmaker.specialHead.STORM)
    else:
        rainmaker, battle, instance = CSEditorUtil.getKwargs(kwargs, 'rainmaker', 'battle', 'instance')

    def setEnvironmentA():
        instance.environment.request('OilRain')
        rainmaker.specialHead.setHairState(rainmaker.specialHead.OIL)

    def setEnvironmentB():
        instance.environment.request('Fog')
        rainmaker.specialHead.setHairState(rainmaker.specialHead.FOG)

    def setEnvironmentC():
        instance.environment.request('Default')

    startNode = rainmaker.attachNewNode('startNode')
    startNode.wrtReparentTo(battle)

    # Populate cutscene loader.
    cutsceneLoader.addSuitsToCutscene([rainmaker])
    cutsceneLoader.addNodesToCutscene([battle, rainmaker, rainmaker.specialHead, startNode])
    cutsceneLoader.addActorsToCutscene([rainmaker])
    cutsceneLoader.addDialogueToCutscene([
        "It's really easy, from where you are, to judge me.",
        "I know you do. Bessie wasn't the only one I talked to.",
        "But the shame of it is, you're not even the worst.",
        "Those other Suits have hurt me too.",
        "They've hurt me in ways that you wouldn’t understand.",
        "Maybe someday, I’ll share some of that pain with someone like you.",
    ])
    cutsceneLoader.addFunctionsToCutscene([setEnvironmentA, setEnvironmentB, setEnvironmentC])
    return cutsceneLoader
# endregion


@cutsceneSetup(CutsceneKeyEnum.MajorPlayer_Revive)
def __majorplayerReviveSetup(editor: bool, **kwargs) -> CutsceneLoader:
    cutsceneLoader = CutsceneLoader()
    if editor:
        toons = CSEditorUtil.makeToons(4)
        mplayer, *suits = CSEditorUtil.makeSuits('mplayer', 'mh', 'mh', 'mh')
        battle = render.attachNewNode('battle')
        battle.setPosHpr(0, 125, 5.351, 0, 0, 0)
        CSEditorUtil.moveActorsToBattlePositions(toons=toons, suits=[mplayer] + suits, newParent=battle)

        from toontown.instances.mercs.DistributedInstanceMajorplayer import DistributedInstanceMajorplayer
        instance = DistributedInstanceMajorplayer(base.cr)
        instance.doId = -420
        instance.loadEnvironment()
    else:
        toons, mplayer, suits, instance = CSEditorUtil.getKwargs(kwargs, 'toons', 'mplayer', 'suits', 'instance')

    # Populate cutscene loader.
    toonNodes = [None] * 4
    for i, toon in enumerate(toons):
        toonNodes[i] = toon
    allSuits = [mplayer, suits[2], suits[1], suits[0]]
    cutsceneLoader.addToonsToCutscene(toons, maxToonCount=4)
    cutsceneLoader.addSuitsToCutscene(allSuits)
    cutsceneLoader.addActorsToCutscene(toonNodes + allSuits)
    cutsceneLoader.addNodesToCutscene([instance.battleNode, toonNodes[0],
                                       mplayer, mplayer.nametag3d,
                                       instance.geom, instance.battleRoom.discoballs[0],
                                       toonNodes[1], toonNodes[2], toonNodes[3],
                                       allSuits[1], allSuits[2], allSuits[3]])
    cutsceneLoader.addDialogueToCutscene([
        "Boo!-booyodididdlyyodoo!",
        "Where are you going babe? It's only the second act!",
        "Hit the floor babe, disco ain't dead, and neither am I!",
        "Let's see if you can handle these greatest hits!",
    ])
    cutsceneLoader.addElevatorsToCutscene([instance.elevatorModel])
    return cutsceneLoader


@cutsceneSetup(CutsceneKeyEnum.MajorPlayer_Death)
def __majorplayerDeathSetup(editor: bool, **kwargs) -> CutsceneLoader:
    cutsceneLoader = CutsceneLoader()
    if editor:
        toons = CSEditorUtil.makeToons(4)
        mplayer, *otherSuits = CSEditorUtil.makeSuits('mplayer', 'mh', 'mh', 'mh', 'mh', 'mh')
        battle = render.attachNewNode('battle')
        battle.setPosHpr(0, 125, 5.351, 180, 0, 0)
        CSEditorUtil.moveActorsToBattlePositions(toons=toons, suits=[mplayer, *otherSuits], newParent=battle)

        from toontown.instances.mercs.DistributedInstanceMajorplayer import DistributedInstanceMajorplayer
        instance = DistributedInstanceMajorplayer(base.cr)
        instance.doId = -420
        instance.loadEnvironment()
    else:
        toons, mplayer, otherSuits, battle, instance = CSEditorUtil.getKwargs(kwargs, 'toons', 'mplayer', 'otherSuits', 'battle', 'instance')

    CLONE, *_ = CSEditorUtil.makeSuits('mplayer')
    CLONE.hideNametag2d()
    CLONE.hide()
    CLONE.reparentTo(instance.geom)

    rose = loader.loadModel('phase_6/models/miniboss/majorplayer_rose')
    rose.hide()
    rose.reparentTo(battle)

    rose_shadow = loader.loadModel('phase_3/models/props/drop_shadow')
    rose_shadow.flattenMedium()
    rose_shadow.setColorScale(1, 1, 1, 0.65)
    rose_shadow.reparentTo(battle)
    rose_shadow.hide()

    audience = instance.battleRoom.getNextAudienceSuit()

    def showAllAudience():
        for member in instance.battleRoom.suitList + [audience]:
            if member:
                member.show()

    def hideAllAudience():
        for member in instance.battleRoom.suitList + [audience]:
            if member:
                member.hide()

    CSEditorUtil.populateList(toons, n=4)
    CSEditorUtil.populateList(otherSuits, n=5)
    if base.localAvatar in toons:
        toons.remove(base.localAvatar)
        toons.insert(0, base.localAvatar)
    cutsceneLoader.addToonsToCutscene(toons)
    cutsceneLoader.addSuitsToCutscene([mplayer] + otherSuits + [audience, CLONE])
    cutsceneLoader.addActorsToCutscene([mplayer] + otherSuits + [audience, CLONE])
    cutsceneLoader.addNodesToCutscene([battle, mplayer] + otherSuits + toons +
                                      [audience.specialHead if audience.specialHead else audience.getHeadParts()[0],
                                       toons[0].find('**/__Actor_head'), mplayer.specialHead, CLONE, CLONE.getGeomNode(),
                                       audience, rose, rose_shadow])
    cutsceneLoader.addFunctionsToCutscene([showAllAudience, hideAllAudience])

    # this stupid guys dialogue
    rng = random.Random(x=mplayer.doId if hasattr(mplayer, 'doId') else random.random())
    line1 = rng.choice([
        "Ring-ding-ding! Now that's a kick in the head if I ever seen one!",
        "Oooh hoo hoo, now that was a fun toe tap!",
    ])
    line3 = rng.choice([
        "I'm tellin ya babe, ya got some shining star cuts to dance with the sun I am!",
        "This night poked a hole in the sky, and I think there's a new star I do, I do!",
    ])
    line4 = rng.choice([
        "I played it my way and babe, your way only made it beeedeepidee-better!",
        "Tap a new tune babe, find that rhythm find that swing; find what I found in you before you play your last bar.",
    ])
    line5, line6 = rng.sample([
        "The bababadapadaaa - bands gotta stop playing eventually, and the night, and the music stop with them...",
        "I know you'll miss these nights but babe, you never miss those steps.",
        "There may be teardrops to shed, but babe, whatever song plays next, I know you can dance to whatever is ahead.",
        "Don't catch those bidddlydoopdoo-blues just cause the moon is over the hill, babe.",
        "I'm tellin' ya now: keep this song in your head, don't lose that tempo that soul. You got pep; a master step!",
        "Subito sempre simile that swingin' shuffle song sung sweetly this night.",
        "Poco a poco, I played loco, and the people went coco!",
    ], k=2)

    cutsceneLoader.addDialogueToCutscene([
        line1,
        "This congregating concert crowd's clapping concerto concentrated concussive chords of congratulations, babe!",
        line3, line4, line5, line6,
        "I can't believe it...",
        "That's all folks!",
        "These perfect prestissimo plays have been played and presented by the powerful proprietor of prowess!",
        "Dave BruBot!",
        "Wink!",
        "You can always find me baby, beyond the sea.",
        "But like any good song, it's time for this one man big band to fade out!",
        "Skibidiba-ta-ta!",
    ])
    return cutsceneLoader


# region Clash Meta
@cutsceneSetup(CutsceneKeyEnum.Trailer_HiresAndHeroesOpeningA)
def __trailerHiresAndHeroesOpeningASetup(editor: bool, **kwargs) -> CutsceneLoader:
    cutsceneLoader = CutsceneLoader()
    if not editor:
        raise CutsceneSetupException

    # Get the NPCs!
    names = TTLocalizer.NPCToonNames
    from toontown.toon.npc.NPCToons import NPCToon
    toons = CSEditorUtil.makeToonsFromNPCToons(
        NPCToon(6818, names[6301], 'mls', 'ms', 's', 'm', (0.325, 0.407, 0.601, 1.0), (0.325, 0.407, 0.601, 1.0), (0.325, 0.407, 0.601, 1.0), 122, 57, 109, 57, 51, 57, hat=14),
        NPCToon(6816, names[6302], 'dll', 'ls', 's', 'f', (0.242, 0.742, 0.516, 1.0), (0.242, 0.742, 0.516, 1.0), (0.242, 0.742, 0.516, 1.0), 7, 7, 7, 7, 9, 22),
        NPCToon(6817, names[6303], 'xls', 'md', 's', 'm', (0.576, 0.439, 0.859, 1.0), (0.576, 0.439, 0.859, 1.0), (0.576, 0.439, 0.859, 1.0), 15, 5, 11, 5, 166, 9),
        NPCToon(6819, names[6304], 'fll', 'sd', 'l', 'm', (0.804, 0.498, 0.196, 1.0), (0.804, 0.498, 0.196, 1.0), (0.804, 0.498, 0.196, 1.0), 9, 6, 9, 6, 8, 3),
        NPCToon(6821, names[6305], 'dss', 'ls', 'l', 'm', (0.996, 0.255, 0.392, 1.0), (0.996, 0.255, 0.392, 1.0), (0.996, 0.255, 0.392, 1.0), 6, 2, 6, 2, 161, 22),
        NPCToon(6836, names[6306], 'fll', 'ms', 'm', 'f', (0.968, 0.749, 0.349, 1.0), (0.968, 0.749, 0.349, 1.0), (0.968, 0.749, 0.349, 1.0), 17, 7, 0, 7, 2, 18),
        NPCToon(6835, names[6307], 'rsl', 'ss', 'l', 'm', (0.641, 0.355, 0.27, 1.0), (0.641, 0.355, 0.27, 1.0), (0.641, 0.355, 0.27, 1.0), 7, 12, 7, 12, 160, 9),
        NPCToon(6823, names[6308], 'dsl', 'ms', 'l', 'm', (0.749, 1.0, 0.847, 1.0), (0.749, 1.0, 0.847, 1.0), (0.749, 1.0, 0.847, 1.0), 19, 3, 13, 3, 160, 1),
        NPCToon(6824, names[6309], 'mss', 'ss', 'm', 'f', (0.996, 0.957, 0.598, 1.0), (0.996, 0.957, 0.598, 1.0), (0.996, 0.957, 0.598, 1.0), 9, 9, 9, 9, 1, 20),
        NPCToon(6825, names[6310], 'mls', 'ls', 'm', 'm', (0.749, 1.0, 0.847, 1.0), (0.749, 1.0, 0.847, 1.0), (0.749, 1.0, 0.847, 1.0), 10, 27, 0, 27, 159, 0),
        NPCToon(6826, names[6311], 'csl', 'ls', 'l', 'm', (0.984, 0.537, 0.396, 1.0), (0.984, 0.537, 0.396, 1.0), (0.984, 0.537, 0.396, 1.0), 5, 9, 5, 9, 159, 10),
        NPCToon(6827, names[6312], 'rsl', 'md', 'l', 'f', (0.89, 0.812, 0.341, 1.0), (0.89, 0.812, 0.341, 1.0), (0.89, 0.812, 0.341, 1.0), 13, 11, 11, 11, 0, 7),
        NPCToon(6828, names[6313], 'rll', 'ls', 'm', 'm', (0.855, 0.934, 0.492, 1.0), (0.855, 0.934, 0.492, 1.0), (0.855, 0.934, 0.492, 1.0), 19, 9, 13, 9, 5, 14),
        NPCToon(6829, names[6314], 'mls', 'ss', 's', 'm', (0.968, 0.749, 0.349, 1.0), (0.968, 0.749, 0.349, 1.0), (0.968, 0.749, 0.349, 1.0), 5, 8, 5, 8, 162, 11),
        NPCToon(6831, names[6315], 'cll', 'ss', 's', 'm', (1.0, 1.0, 0.941, 1.0), (1.0, 1.0, 0.941, 1.0), (1.0, 1.0, 0.941, 1.0), 5, 3, 5, 3, 158, 11),
        NPCToon(6832, names[6316], 'hls', 'ss', 'l', 'm', (0.996, 0.695, 0.512, 1.0), (0.996, 0.695, 0.512, 1.0), (0.996, 0.695, 0.512, 1.0), 11, 10, 0, 10, 162, 14),
        NPCToon(6833, names[6317], 'fls', 'ss', 'l', 'm', (0.285, 0.328, 0.727, 1.0), (0.285, 0.328, 0.727, 1.0), (0.285, 0.328, 0.727, 1.0), 8, 1, 8, 1, 160, 12),
        NPCToon(6834, names[6318], 'dll', 'ss', 'm', 'f', (0.434, 0.906, 0.836, 1.0), (0.434, 0.906, 0.836, 1.0), (0.434, 0.906, 0.836, 1.0), 22, 11, 0, 11, 9, 2),
        NPCToon(6315, names[2421], 'ess', 'ms', 'm', 'f', 12, 12, 12, 203, 27, 187, 27, 289, 27),
    )

    # Load the cutscene.
    from toontown.dna.DNAStorage import DNAStorage
    from toontown.dna.DNAParser import DNABulkLoader
    safeZoneStorageDNAFile = 'phase_6/dna/storage_OZ_sz.pdna'
    storageDNAFile = 'phase_6/dna/storage_OZ.pdna'
    dnaFile = 'phase_6/dna/outdoor_zone_6300.pdna'
    dnaStore = DNAStorage()
    files = ('phase_4/dna/storage.pdna',
             'phase_3.5/dna/storage_interior.pdna',
             storageDNAFile,
             safeZoneStorageDNAFile,
             'phase_5/dna/storage_town.pdna', 'phase_6/dna/storage_OZ_town.pdna')
    dnaBulk = DNABulkLoader(dnaStore, files)
    dnaBulk.loadDNAFiles()
    node = loader.loadDNAFile(dnaStore, dnaFile)
    scene = render.attachNewNode(node)
    scene.show()

    cameraStart = render.attachNewNode('cameraStart')
    toonBase = render.attachNewNode('toonBase')
    for toon in toons:
        toon.reparentTo(toonBase)
        toon.show()

    # Add sky
    sky = loader.loadModel('phase_3.5/models/props/TT_sky')
    sky.reparentTo(render)
    sky.show()
    from toontown.hood import SkyUtil
    SkyUtil.startCloudSky(hood=None, parent=cameraStart, sky=sky)

    # Populate cutscene loader.
    cutsceneLoader.addToonsToCutscene(toons)
    cutsceneLoader.addActorsToCutscene(toons)
    cutsceneLoader.addNodesToCutscene([cameraStart, toonBase] + toons + [])
    cutsceneLoader.addDialogueToCutscene([
        "I LOVE TOONTOWN"
    ])
    return cutsceneLoader


@cutsceneSetup(CutsceneKeyEnum.Trailer_HiresAndHeroesOpeningB)
def __trailerHiresAndHeroesOpeningBSetup(editor: bool, **kwargs) -> CutsceneLoader:
    cutsceneLoader = CutsceneLoader()
    if not editor:
        raise CutsceneSetupException

    names = TTLocalizer.NPCToonNames
    from toontown.toon.npc.NPCToons import NPCToon
    toons = CSEditorUtil.makeToonsFromNPCToons(
        NPCToon(2643, names[2123], 'cls', 'md', 'l', 'f', 4, 4, 4, 0, 5, 0, 5, 14, 27, hat=40),
        NPCToon(2644, names[2124], 'dll', 'sd', 'l', 'f', 21, 21, 21, 0, 5, 0, 5, 8, 21, hat=115, glasses=23),
        NPCToon(2649, names[2125], 'dss', 'ss', 'l', 'm', 12, 12, 12, 254, 27, 227, 27, 159, 10, hat=83, glasses=3),
        NPCToon(2654, names[2126], 'dls', 'ld', 'l', 'f', 4, 4, 4, 167, 27, 153, 27, 44, 27, hat=12, glasses=13, backpack=23),
        NPCToon(2655, names[2127], 'fsl', 'ms', 'l', 'm', 19, 19, 19, 82, 36, 71, 35, 209, 40, hat=24, glasses=17, shoes=1, shoesTex=31),
        NPCToon(2656, names[2128], 'fss', 'ss', 'l', 'm', 12, 12, 12, 65, 27, 54, 27, 200, 27, hat=47, glasses=3, backpack=66, shoes=3, shoesTex=40),
        NPCToon(2657, names[2129], 'rll', 'ss', 'l', 'm', 4, 4, 4, 1, 5, 1, 5, 156, 9, hat=103, glasses=1),
        NPCToon(2659, names[2130], 'rss', 'md', 'l', 'f', 19, 19, 19, 17, 15, 0, 15, 8, 37, glasses=14, backpack=71),
        NPCToon(2660, names[2131], 'rls', 'ls', 'l', 'f', 12, 12, 12, 1, 8, 1, 8, 1, 26, hat=27, glasses=12, backpack=7, shoes=1, shoesTex=10),
        NPCToon(2661, names[2132], 'mls', 'ss', 'l', 'm', 4, 4, 4, 206, 27, 190, 27, 5, 17, hat=25, glasses=1, backpack=30, shoes=3, shoesTex=26),  # Daffy Don
        NPCToon(2662, names[2133], 'hll', 'ls', 'l', 'm', 18, 18, 18, 99, 26, 126, 26, 155, 39, hat=96, hatColor=35, glasses=13, shoes=2, shoesTex=18),  # Dr. Euphoric
        NPCToon(2664, names[2134], 'zss', 'ms', 'm', 'f', (0.996, 0.255, 0.392, 1.0), (0.996, 0.255, 0.392, 1.0), (0.996, 0.255, 0.392, 1.0), 207, 27, 191, 27, 271, 27, hat=99),
        NPCToon(2665, names[2135], 'hls', 'ms', 'l', 'f', 3, 3, 3, 0, 12, 0, 12, 2, 26, hat=17, glasses=7, backpack=15, shoes=2, shoesTex=14),
        NPCToon(2666, names[2136], 'csl', 'ls', 'l', 'm', 18, 18, 18, 118, 27, 105, 27, 162, 15, hat=45, shoes=2, shoesTex=8),
        NPCToon(2667, names[2137], 'css', 'sd', 'l', 'f', 11, 11, 11, 0, 21, 0, 21, 24, 27),
        NPCToon(2669, names[2138], 'dll', 'ss', 'l', 'm', 3, 3, 3, 0, 39, 0, 39, 156, 39, hat=51, glasses=7, shoes=2, shoesTex=21),
        NPCToon(2670, names[2139], 'fsl', 'ms', 'l', 'm', (0.898, 0.617, 0.906, 1.0), (0.898, 0.617, 0.906, 1.0), (0.898, 0.617, 0.906, 1.0), 149, 27, 136, 27, 63, 27, hat=13, backpack=80, shoes=1, shoesTex=10),
        NPCToon(2156, names[2140], 'dls', 'ls', 'l', 'm', 10, 10, 10, 1, 9, 1, 9, 156, 10, hat=18),
    )
    suits = CSEditorUtil.makeSuits('duckshfl')
    ducky = suits[0]
    ducky.reparentTo(render)
    ducky.specialHead.setEyePos(0.27)

    # Load the cutscene.
    from toontown.dna.DNAStorage import DNAStorage
    from toontown.dna.DNAParser import DNABulkLoader
    safeZoneStorageDNAFile = 'phase_4/dna/storage_TT_sz.pdna'
    storageDNAFile = 'phase_4/dna/storage_TT.pdna'
    dnaFile = 'phase_5/dna/toontown_central_2100.pdna'
    dnaStore = DNAStorage()
    files = (
        'phase_4/dna/storage.pdna',
        'phase_3.5/dna/storage_interior.pdna',
        storageDNAFile,
        safeZoneStorageDNAFile,
        'phase_5/dna/storage_town.pdna',
        'phase_5/dna/storage_TT_town.pdna',
    )
    dnaBulk = DNABulkLoader(dnaStore, files)
    dnaBulk.loadDNAFiles()
    node = loader.loadDNAFile(dnaStore, dnaFile)
    scene = render.attachNewNode(node)
    scene.show()

    cameraStart = render.attachNewNode('cameraStart')
    cameraShake = render.attachNewNode('cameraShake')
    toonBase = render.attachNewNode('toonBase')
    toonBase2 = render.attachNewNode('toonBase2')
    for toon in toons:
        toon.reparentTo(toonBase)
        toon.show()
    toons[9].reparentTo(toonBase2)
    toons[12].reparentTo(toonBase2)
    toons[17].reparentTo(toonBase2)
    daffy = toons[9]

    # Add sky
    sky = loader.loadModel('phase_3.5/models/props/TT_sky')
    sky.reparentTo(render)
    sky.show()
    from toontown.hood import SkyUtil
    SkyUtil.startCloudSky(hood=None, parent=cameraStart, sky=sky)

    # Populate cutscene loader.
    cutsceneLoader.addToonsToCutscene(toons)
    cutsceneLoader.addSuitsToCutscene(suits)
    cutsceneLoader.addActorsToCutscene(toons)
    cutsceneLoader.addNodesToCutscene([cameraStart, toonBase, toonBase2] + toons + [cameraShake, ducky, daffy.toonGlasses.accessoryGeom])
    cutsceneLoader.addDialogueToCutscene([
        "I LOVE TOONTOWN"
    ])
    cutsceneLoader.addArgumentsToCutscene([0])
    return cutsceneLoader


@cutsceneSetup(CutsceneKeyEnum.Trailer_MajorPlayer)
def __majorplayerTrailerSetup(editor: bool, **kwargs) -> CutsceneLoader:
    cutsceneLoader = CutsceneLoader()
    if not editor:
        raise CutsceneSetupException

    from toontown.instances.mercs.DistributedInstanceMajorplayer import DistributedInstanceMajorplayer
    instance = DistributedInstanceMajorplayer(base.cr)
    instance.doId = -420
    instance.loadEnvironment(overrideSuitCount=24)
    suits = CSEditorUtil.makeSuits(
        'duckshfl', 'ddiver', 'gatekeep', 'bellring', 'mouthp', 'fires', 'treek', 'fbed',
        'prethink', 'rainmake', 'whunter', 'mslacker', 'mplayer', 'pcrat', 'chainsaw', 'psetter',
        'charon', 'nix', 'hydra', 'styx', 'kerberos', 'ptjockey', 'ptjockey'
    )
    fbed = suits[7]
    fires = suits[5]
    psetter = suits[15]
    ddiver = suits[1]
    gatekeep = suits[2]

    for suit in suits:
        suit.reparentTo(render)
        suit.makeExecutive()

    def init():
        def overrideClearScaleFunc(suit):
            suit.setColorScale(1, 1, 1, 1)
        for suit in suits:
            suit.setColorScale(0, 0, 0, 1)
            setattr(suit, 'overrideClearScaleFunc', overrideClearScaleFunc)

    # Populate cutscene loader.
    cutsceneLoader.addToonsToCutscene([], maxToonCount=4)
    cutsceneLoader.addSuitsToCutscene(suits)
    cutsceneLoader.addActorsToCutscene(suits)
    cutsceneLoader.addNodesToCutscene(suits + [instance.geom, instance.battleRoom.discoballs[1],
                                               fbed.specialHead,
                                               fires.specialHead,
                                               psetter.specialHead,
                                               ddiver.nametag3d,
                                               gatekeep.nametag3d,
                                               psetter.nametag3d,])
    cutsceneLoader.addDialogueToCutscene([
        "\1white\1\5bossbot\5 \2Major Player\n\1TextSmaller\1Medley Monstrosity\2",
        "\1white\1\5cashbot\5 \2Duck Shuffler\n\1TextSmaller\1Roulette Rigmarole\2",
        "\1white\1\5sellbot\5 \2Prethinker\n\1TextSmaller\1Boastful Brainiac\2",
        "\1white\1\5lawbot\5 \2Rainmaker\n\1TextSmaller\1Sorrowful Sympathist\2",
        "\1white\1\5sellbot\5 \2Bellringer\n\1TextSmaller\1Eavesdropping Earpopper\2",
        "\1white\1\5boardbot\5 \2Deep Diver\n\1TextSmaller\1Sidewalk Swimmer\2",
        "\1white\1\5cashbot\5 \2Treekiller\n\1TextSmaller\1Wretched Woodsplitter\2",
        "\1white\1\5bossbot\5 \2Chainsaw Consultant\n\1TextSmaller\1Temperamental Terminator\2",
        "\1white\1\5sellbot\5 \2Multislacker\n\1TextSmaller\1Professional Procrastinator\2",
        "\1white\1\5lawbot\5 \2Mouthpiece\n\1TextSmaller\1Rusty Ringleader\2",
        "\1white\1\5lawbot\5 \2Witch Hunter\n\1TextSmaller\1Mob Master\2",
        "\1white\1\5bossbot\5 \2Featherbedder\n\1TextSmaller\1Soundless Sleeper\2",
        "\1white\1\5boardbot\5 \2Gatekeeper\n\1TextSmaller\1Vainglorious Vanguard\2",
        "\1white\1\5cashbot\5 \2Plutocrat\n\1TextSmaller\1Galactic Godfather\2",
        "\1white\1\5bossbot\5 \2Firestarter\n\1TextSmaller\1Apprehensive Arsonist\2",
        "\1white\1\5sellbot\5 \2Pacesetter\n\1TextSmaller\1Expeditious Egotist\2",
        "\1white\1\5cashbot\5 \2Charon\n",
        "\1white\1\5cashbot\5 \2Nix\n",
        "\1white\1\5cashbot\5 \2Hydra\n",
        "\1white\1\5cashbot\5 \2Styx\n",
        "\1white\1\5cashbot\5 \2Kerberos\n",
    ])
    cutsceneLoader.addElevatorsToCutscene([instance.elevatorModel])
    cutsceneLoader.addFunctionsToCutscene([init])
    cutsceneLoader.addArgumentsToCutscene([0])
    return cutsceneLoader
# endregion
