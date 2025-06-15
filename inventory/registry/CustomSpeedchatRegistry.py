"""
This module contains the item data for custom speedchat phrases.
"""
from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.base.ItemDefinition import ItemDefinition
from typing import Dict, Optional
from enum import IntEnum

from toontown.inventory.enums.EquipSoundEnum import EquipSoundEnum
from toontown.inventory.enums.ItemEnums import CustomSpeedchatItemType
from toontown.toonbase import TTLocalizer as TTL


class CustomSpeedchatDefinition(ItemDefinition):
    """
    The definition structure for custom speedchat phrases.
    """

    def getText(self):
        return self.name

    def getItemTypeName(self):
        return 'Custom Speedchat Phrase'

    def getRewardName(self, item: Optional[InventoryItem] = None):
        return f'"{self.getName()}" Custom Speedchat Phrase'

    def getEquipSounds(self) -> EquipSoundEnum:
        return self.equipSounds or EquipSoundEnum.SpeedchatPhrase


# The registry dictionary for speedchat phrases.
# Dynamically assigns from TTLocalizer.CustomSCStrings
CustomSpeedchatRegistry: Dict[IntEnum, CustomSpeedchatDefinition] = {
    CustomSpeedchatItemType.OhWell: CustomSpeedchatDefinition(
        name="Oh, well.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WhyNot: CustomSpeedchatDefinition(
        name="Why not?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Naturally: CustomSpeedchatDefinition(
        name="Naturally!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsTheWayToDoIt: CustomSpeedchatDefinition(
        name="That's the way to do it.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.RightOn: CustomSpeedchatDefinition(
        name="Right on!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WhatUp: CustomSpeedchatDefinition(
        name="What up?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ButOfCourse: CustomSpeedchatDefinition(
        name="But of course!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Bingo: CustomSpeedchatDefinition(
        name="Bingo!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouveGotToBeKidding: CustomSpeedchatDefinition(
        name="You've got to be kidding...",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SoundsGoodToMe: CustomSpeedchatDefinition(
        name="Sounds good to me.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsKooky: CustomSpeedchatDefinition(
        name="That's kooky!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Awesome: CustomSpeedchatDefinition(
        name="Awesome!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ForCryingOutLoud: CustomSpeedchatDefinition(
        name="For crying out loud!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontWorry: CustomSpeedchatDefinition(
        name="Don't worry.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Grrrr: CustomSpeedchatDefinition(
        name="Grrrr!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WhatsNew: CustomSpeedchatDefinition(
        name="What's new?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HeyHeyHey: CustomSpeedchatDefinition(
        name="Hey, hey, hey!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SeeYouTomorrow: CustomSpeedchatDefinition(
        name="See you tomorrow.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SeeYouNextTime: CustomSpeedchatDefinition(
        name="See you next time.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SeeYaLaterAlligator: CustomSpeedchatDefinition(
        name="See ya later, alligator.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.AfterAWhileCrocodile: CustomSpeedchatDefinition(
        name="After a while, crocodile.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.INeedToGoSoon: CustomSpeedchatDefinition(
        name="I need to go soon.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IDontKnowAboutThis: CustomSpeedchatDefinition(
        name="I don't know about this!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YoureOuttaHere: CustomSpeedchatDefinition(
        name="You're outta here!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.OuchThatReallySmarts: CustomSpeedchatDefinition(
        name="Ouch, that really smarts!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Gotcha: CustomSpeedchatDefinition(
        name="Gotcha!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Please: CustomSpeedchatDefinition(
        name="Please!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThanksAMillion: CustomSpeedchatDefinition(
        name="Thanks a million!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouAreStylin: CustomSpeedchatDefinition(
        name="You are stylin'!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ExcuseMe: CustomSpeedchatDefinition(
        name="Excuse me!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.CanIHelpYou: CustomSpeedchatDefinition(
        name="Can I help you?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsWhatImTalkingAbout: CustomSpeedchatDefinition(
        name="That's what I'm talking about!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IfYouCantTakeTheHeatStayOutOfTheKitchen: CustomSpeedchatDefinition(
        name="If you can't take the heat, stay out of the kitchen.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WellShiverMeTimbers: CustomSpeedchatDefinition(
        name="Well shiver me timbers!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WellIsntThatSpecial: CustomSpeedchatDefinition(
        name="Well isn't that special!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.QuitHorsingAround: CustomSpeedchatDefinition(
        name="Quit horsing around!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.CatGotYourTongue: CustomSpeedchatDefinition(
        name="Cat got your tongue?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YoureInTheDogHouseNow: CustomSpeedchatDefinition(
        name="You're in the dog house now!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LookWhatTheCatDraggedIn: CustomSpeedchatDefinition(
        name="Look what the cat dragged in.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.INeedToGoSeeAToon: CustomSpeedchatDefinition(
        name="I need to go see a Toon.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontHaveACow: CustomSpeedchatDefinition(
        name="Don't have a cow!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontChickenOut: CustomSpeedchatDefinition(
        name="Don't chicken out!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YoureASittingDuck: CustomSpeedchatDefinition(
        name="You're a sitting duck.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Whatever: CustomSpeedchatDefinition(
        name="Whatever!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Totally: CustomSpeedchatDefinition(
        name="Totally!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Sweet: CustomSpeedchatDefinition(
        name="Sweet!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatRules: CustomSpeedchatDefinition(
        name="That rules!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YeahBaby: CustomSpeedchatDefinition(
        name="Yeah, baby!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.CatchMeIfYouCan: CustomSpeedchatDefinition(
        name="Catch me if you can!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouNeedToHealFirst: CustomSpeedchatDefinition(
        name="You need to heal first.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouNeedMoreLaffPoints: CustomSpeedchatDefinition(
        name="You need more Laff Points.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IllBeBackInAMinute: CustomSpeedchatDefinition(
        name="I'll be back in a minute.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImHungry: CustomSpeedchatDefinition(
        name="I'm hungry.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YeahRight: CustomSpeedchatDefinition(
        name="Yeah, right!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImSleepy: CustomSpeedchatDefinition(
        name="I'm sleepy.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImReady: CustomSpeedchatDefinition(
        name="I'm ready!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImBored: CustomSpeedchatDefinition(
        name="I'm bored.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ILoveIt: CustomSpeedchatDefinition(
        name="I love it!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatWasExciting: CustomSpeedchatDefinition(
        name="That was exciting!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Jump: CustomSpeedchatDefinition(
        name="Jump!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.GotGags: CustomSpeedchatDefinition(
        name="Got gags?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WhatsWrong: CustomSpeedchatDefinition(
        name="What's wrong?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.EasyDoesIt: CustomSpeedchatDefinition(
        name="Easy does it.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SlowAndSteadyWinsTheRace: CustomSpeedchatDefinition(
        name="Slow and steady wins the race.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Touchdown: CustomSpeedchatDefinition(
        name="Touchdown!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Ready: CustomSpeedchatDefinition(
        name="Ready?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Set: CustomSpeedchatDefinition(
        name="Set!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Go: CustomSpeedchatDefinition(
        name="Go!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LetsGoThisWay: CustomSpeedchatDefinition(
        name="Let's go this way!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouWon: CustomSpeedchatDefinition(
        name="You won!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IVoteYes: CustomSpeedchatDefinition(
        name="I vote yes.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IVoteNo: CustomSpeedchatDefinition(
        name="I vote no.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.CountMeIn: CustomSpeedchatDefinition(
        name="Count me in.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.CountMeOut: CustomSpeedchatDefinition(
        name="Count me out.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.StayHereIllBeBack: CustomSpeedchatDefinition(
        name="Stay here, I'll be back.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatWasQuick: CustomSpeedchatDefinition(
        name="That was quick!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DidYouSeeThat: CustomSpeedchatDefinition(
        name="Did you see that?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WhatsThatSmell: CustomSpeedchatDefinition(
        name="What's that smell?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatStinks: CustomSpeedchatDefinition(
        name="That stinks!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IDontCare: CustomSpeedchatDefinition(
        name="I don't care.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.JustWhatTheDoctorOrdered: CustomSpeedchatDefinition(
        name="Just what the doctor ordered.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LetsGetThisPartyStarted: CustomSpeedchatDefinition(
        name="Let's get this party started!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThisWayEverybody: CustomSpeedchatDefinition(
        name="This way everybody!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WhatInTheWorld: CustomSpeedchatDefinition(
        name="What in the world?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TheChecksInTheMail: CustomSpeedchatDefinition(
        name="The check's in the mail.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IHeardThat: CustomSpeedchatDefinition(
        name="I heard that!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.AreYouTalkingToMe: CustomSpeedchatDefinition(
        name="Are you talking to me?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThankYouIllBeHereAllWeek: CustomSpeedchatDefinition(
        name="Thank you, I'll be here all week.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Hmm: CustomSpeedchatDefinition(
        name="Hmm.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IllGetThisOne: CustomSpeedchatDefinition(
        name="I'll get this one.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IGotIt: CustomSpeedchatDefinition(
        name="I got it!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ItsMine: CustomSpeedchatDefinition(
        name="It's mine!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.PleaseTakeIt: CustomSpeedchatDefinition(
        name="Please, take it.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.StandBackThisCouldBeDangerous: CustomSpeedchatDefinition(
        name="Stand back, this could be dangerous.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.NoWorries: CustomSpeedchatDefinition(
        name="No worries!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.OhMy: CustomSpeedchatDefinition(
        name="Oh, my!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Whew: CustomSpeedchatDefinition(
        name="Whew!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Owoooo: CustomSpeedchatDefinition(
        name="Owoooo!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.AllAboard: CustomSpeedchatDefinition(
        name="All Aboard!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HotDiggityDog: CustomSpeedchatDefinition(
        name="Hot Diggity Dog!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.CuriosityKilledTheCat: CustomSpeedchatDefinition(
        name="Curiosity killed the cat.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TeamworkMakesTheDreamWork: CustomSpeedchatDefinition(
        name="Teamwork makes the dream work!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.EvenMiraclesTakeALittleTime: CustomSpeedchatDefinition(
        name="Even miracles take a little time.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SometimesTheRightPathIsNotTheEasiestOne: CustomSpeedchatDefinition(
        name="Sometimes the right path is not the easiest one.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TodayIsAGoodDayToTry: CustomSpeedchatDefinition(
        name="Today is a good day to try.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TodayIsMyLuckyDay: CustomSpeedchatDefinition(
        name="Today is my lucky day!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.GetYourActTogether: CustomSpeedchatDefinition(
        name="Get your act together!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WellPlayItByEar: CustomSpeedchatDefinition(
        name="We'll play it by ear.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.APieInTheHandIsWorthTwoInTheOven: CustomSpeedchatDefinition(
        name="A pie in the hand is worth two in the oven.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ItsRainingCatsAndDogs: CustomSpeedchatDefinition(
        name="It's raining cats and dogs!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IThinkIllCallItADay: CustomSpeedchatDefinition(
        name="I think I'll call it a day.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TakeThis: CustomSpeedchatDefinition(
        name="Take this!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TakeThat: CustomSpeedchatDefinition(
        name="Take that!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Electrifying: CustomSpeedchatDefinition(
        name="Electrifying!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.BeBackInAJiffy: CustomSpeedchatDefinition(
        name="Be back in a jiffy.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IDontSeeWhyNot: CustomSpeedchatDefinition(
        name="I don't see why not.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouNeverKnowUnlessYouTry: CustomSpeedchatDefinition(
        name="You never know unless you try.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SmartMove: CustomSpeedchatDefinition(
        name="Smart move!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatCantBeAGoodIdea: CustomSpeedchatDefinition(
        name="That can't be a good idea...",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImDownForTheCount: CustomSpeedchatDefinition(
        name="I'm down for the count.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IThinkYouShouldSleepOnIt: CustomSpeedchatDefinition(
        name="I think you should sleep on it.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Valid: CustomSpeedchatDefinition(
        name="Valid!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.EverybodyIsWelcome: CustomSpeedchatDefinition(
        name="Everybody is welcome!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TheresAlwaysASpaceForYou: CustomSpeedchatDefinition(
        name="There's always a space for you!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IConcur: CustomSpeedchatDefinition(
        name="I concur.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.KindnessIsTheBestPolicy: CustomSpeedchatDefinition(
        name="Kindness is the best policy.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HonestyIsTheBestPolicy: CustomSpeedchatDefinition(
        name="Honesty is the best policy.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ManyDifferentFlowersMakeABouquet: CustomSpeedchatDefinition(
        name="Many different flowers make a bouquet.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.GreatMindsThinkAlike: CustomSpeedchatDefinition(
        name="Great minds think alike.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IfYouWantToGoFarGoTogether: CustomSpeedchatDefinition(
        name="If you want to go far, go together.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IAmGoingToScream: CustomSpeedchatDefinition(
        name="I am going to scream.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.OhYoureApproachingMe: CustomSpeedchatDefinition(
        name="Oh? You're approaching me?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Yeah: CustomSpeedchatDefinition(
        name="Yeah?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ActYourAge: CustomSpeedchatDefinition(
        name="Act your age!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.AmIGladToSeeYou: CustomSpeedchatDefinition(
        name="Am I glad to see you!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.BeMyGuest: CustomSpeedchatDefinition(
        name="Be my guest.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.BeenKeepingOutOfTrouble: CustomSpeedchatDefinition(
        name="Been keeping out of trouble?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.BetterLateThanNever: CustomSpeedchatDefinition(
        name="Better late than never!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Bravo: CustomSpeedchatDefinition(
        name="Bravo!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ButSeriouslyFolks: CustomSpeedchatDefinition(
        name="But seriously, folks...",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.CareToJoinUs: CustomSpeedchatDefinition(
        name="Care to join us?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.CatchYouLater: CustomSpeedchatDefinition(
        name="Catch you later!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ChangedYourMind: CustomSpeedchatDefinition(
        name="Changed your mind?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ComeAndGetIt: CustomSpeedchatDefinition(
        name="Come and get it!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DearMe: CustomSpeedchatDefinition(
        name="Dear me!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DelightedToMakeYourAcquaintance: CustomSpeedchatDefinition(
        name="Delighted to make your acquaintance.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontDoAnythingIWouldntDo: CustomSpeedchatDefinition(
        name="Don't do anything I wouldn't do!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontEvenThinkAboutIt: CustomSpeedchatDefinition(
        name="Don't even think about it!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontGiveUpTheShip: CustomSpeedchatDefinition(
        name="Don't give up the ship!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontHoldYourBreath: CustomSpeedchatDefinition(
        name="Don't hold your breath.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontAsk: CustomSpeedchatDefinition(
        name="Don't ask.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.EasyForYouToSay: CustomSpeedchatDefinition(
        name="Easy for you to say.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.EnoughIsEnough: CustomSpeedchatDefinition(
        name="Enough is enough!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Excellent: CustomSpeedchatDefinition(
        name="Excellent!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.FancyMeetingYouHere: CustomSpeedchatDefinition(
        name="Fancy meeting you here!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.GiveMeABreak: CustomSpeedchatDefinition(
        name="Give me a break.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.GladToHearIt: CustomSpeedchatDefinition(
        name="Glad to hear it.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.GoAheadMakeMyDay: CustomSpeedchatDefinition(
        name="Go ahead, make my day!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.GoForIt: CustomSpeedchatDefinition(
        name="Go for it!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.GoodJob: CustomSpeedchatDefinition(
        name="Good job!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.GoodToSeeYou: CustomSpeedchatDefinition(
        name="Good to see you!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.GotToGetMoving: CustomSpeedchatDefinition(
        name="Got to get moving.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.GotToHitTheRoad: CustomSpeedchatDefinition(
        name="Got to hit the road.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HangInThere: CustomSpeedchatDefinition(
        name="Hang in there.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HangOnASecond: CustomSpeedchatDefinition(
        name="Hang on a second.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HaveABall: CustomSpeedchatDefinition(
        name="Have a ball!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HaveFun: CustomSpeedchatDefinition(
        name="Have fun!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HaventGotAllDay: CustomSpeedchatDefinition(
        name="Haven't got all day!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HoldYourHorses: CustomSpeedchatDefinition(
        name="Hold your horses!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Horsefeathers: CustomSpeedchatDefinition(
        name="Horsefeathers!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IDontBelieveThis: CustomSpeedchatDefinition(
        name="I don't believe this!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IDoubtIt: CustomSpeedchatDefinition(
        name="I doubt it.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IOweYouOne: CustomSpeedchatDefinition(
        name="I owe you one.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IReadYouLoudAndClear: CustomSpeedchatDefinition(
        name="I read you loud and clear.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IThinkSo: CustomSpeedchatDefinition(
        name="I think so.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IllPass: CustomSpeedchatDefinition(
        name="I'll pass.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IWishIdSaidThat: CustomSpeedchatDefinition(
        name="I wish I'd said that.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IWouldntIfIWereYou: CustomSpeedchatDefinition(
        name="I wouldn't if I were you.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IdBeHappyTo: CustomSpeedchatDefinition(
        name="I'd be happy to!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImHelpingMyFriend: CustomSpeedchatDefinition(
        name="I'm helping my friend.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImHereAllWeek: CustomSpeedchatDefinition(
        name="I'm here all week.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImagineThat: CustomSpeedchatDefinition(
        name="Imagine that!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.InTheNickOfTime: CustomSpeedchatDefinition(
        name="In the nick of time...",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ItsNotOverTilItsOver: CustomSpeedchatDefinition(
        name="It's not over 'til it's over.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.JustThinkingOutLoud: CustomSpeedchatDefinition(
        name="Just thinking out loud.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.KeepInTouch: CustomSpeedchatDefinition(
        name="Keep in touch.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LovelyWeatherForDucks: CustomSpeedchatDefinition(
        name="Lovely weather for ducks!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.MakeItSnappy: CustomSpeedchatDefinition(
        name="Make it snappy!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.MakeYourselfAtHome: CustomSpeedchatDefinition(
        name="Make yourself at home.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.MaybeSomeOtherTime: CustomSpeedchatDefinition(
        name="Maybe some other time.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.MindIfIJoinYou: CustomSpeedchatDefinition(
        name="Mind if I join you?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.NicePlaceYouHaveHere: CustomSpeedchatDefinition(
        name="Nice place you have here.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.NiceTalkingToYou: CustomSpeedchatDefinition(
        name="Nice talking to you.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.NoDoubtAboutIt: CustomSpeedchatDefinition(
        name="No doubt about it.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.NoKidding: CustomSpeedchatDefinition(
        name="No kidding!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.NotByALongShot: CustomSpeedchatDefinition(
        name="Not by a long shot.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.OfAllTheNerve: CustomSpeedchatDefinition(
        name="Of all the nerve!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.OkayByMe: CustomSpeedchatDefinition(
        name="Okay by me.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Righto: CustomSpeedchatDefinition(
        name="Righto.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SayCheese: CustomSpeedchatDefinition(
        name="Say cheese!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SayWhat: CustomSpeedchatDefinition(
        name="Say what?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TahDah: CustomSpeedchatDefinition(
        name="Tah-dah!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TakeItEasy: CustomSpeedchatDefinition(
        name="Take it easy.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TaTaForNow: CustomSpeedchatDefinition(
        name="Ta-ta for now!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThanksButNoThanks: CustomSpeedchatDefinition(
        name="Thanks, but no thanks.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatTakesTheCake: CustomSpeedchatDefinition(
        name="That takes the cake!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsFunny: CustomSpeedchatDefinition(
        name="That's funny.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsTheTicket: CustomSpeedchatDefinition(
        name="That's the ticket!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TheresACogInvasion: CustomSpeedchatDefinition(
        name="There's a Cog invasion!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Toodles: CustomSpeedchatDefinition(
        name="Toodles.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WatchOut: CustomSpeedchatDefinition(
        name="Watch out!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WellDone: CustomSpeedchatDefinition(
        name="Well done!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WhatsCooking: CustomSpeedchatDefinition(
        name="What's cooking?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WhatsHappening: CustomSpeedchatDefinition(
        name="What's happening?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WorksForMe: CustomSpeedchatDefinition(
        name="Works for me.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YesSirree: CustomSpeedchatDefinition(
        name="Yes sirree.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouBetcha: CustomSpeedchatDefinition(
        name="You betcha.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouDoTheMath: CustomSpeedchatDefinition(
        name="You do the math.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouLeavingSoSoon: CustomSpeedchatDefinition(
        name="You leaving so soon?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouMakeMeLaugh: CustomSpeedchatDefinition(
        name="You make me laugh!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouTakeRight: CustomSpeedchatDefinition(
        name="You take right.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YoureGoingDown: CustomSpeedchatDefinition(
        name="You're going down!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.AnythingThatCanGoWrongWillGoWrong: CustomSpeedchatDefinition(
        name="Anything that can go wrong will go wrong.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.NeverInAMillionYears: CustomSpeedchatDefinition(
        name="Never in a million years!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WouldYouLikeSomeJellybeansWithThat: CustomSpeedchatDefinition(
        name="Would you like some jellybeans with that?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LetTheSleepingDogLie: CustomSpeedchatDefinition(
        name="Let the sleeping dog lie.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Jinx: CustomSpeedchatDefinition(
        name="Jinx!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.XMarksTheSpot: CustomSpeedchatDefinition(
        name="X marks the spot!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IsThatLegal: CustomSpeedchatDefinition(
        name="Is that legal?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatIsIllegal: CustomSpeedchatDefinition(
        name="That is illegal.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IllBeTheJudgeOfThat: CustomSpeedchatDefinition(
        name="I'll be the judge of that.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouBeTheJudge: CustomSpeedchatDefinition(
        name="You be the judge.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HowIsThatEvenPossible: CustomSpeedchatDefinition(
        name="How is that even possible?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IDontThinkItMeansWhatYouThinkItMeans: CustomSpeedchatDefinition(
        name="I don't think it means what you think it means.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Wonderful: CustomSpeedchatDefinition(
        name="Wonderful!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Terrific: CustomSpeedchatDefinition(
        name="Terrific!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Really: CustomSpeedchatDefinition(
        name="Really?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Nope: CustomSpeedchatDefinition(
        name="Nope.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WithGreatPowerComesGreatResponsibility: CustomSpeedchatDefinition(
        name="With great power comes great responsibility.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ItsYourTurn: CustomSpeedchatDefinition(
        name="It's your turn.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IveMadeUpMyMind: CustomSpeedchatDefinition(
        name="I've made up my mind.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SpeakOfTheDevilRay: CustomSpeedchatDefinition(
        name="Speak of the devil ray!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThisIsAVrbys: CustomSpeedchatDefinition(
        name="This is a VRby's.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThisIsFine: CustomSpeedchatDefinition(
        name="This is fine.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.BringItOnTinCan: CustomSpeedchatDefinition(
        name="Bring it on, tin-can!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IBegYourPardon: CustomSpeedchatDefinition(
        name="I beg your pardon?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.AnythingYouSay: CustomSpeedchatDefinition(
        name="Anything you say.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.CareIfIJoinYou: CustomSpeedchatDefinition(
        name="Care if I join you?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.CheckPlease: CustomSpeedchatDefinition(
        name="Check, please.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontBeTooSure: CustomSpeedchatDefinition(
        name="Don't be too sure.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontMindIfIDo: CustomSpeedchatDefinition(
        name="Don't mind if I do.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontSweatIt: CustomSpeedchatDefinition(
        name="Don't sweat it!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontYouKnowIt: CustomSpeedchatDefinition(
        name="Don't you know it!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontMindMe: CustomSpeedchatDefinition(
        name="Don't mind me.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Eureka: CustomSpeedchatDefinition(
        name="Eureka!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.FancyThat: CustomSpeedchatDefinition(
        name="Fancy that!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ForgetAboutIt: CustomSpeedchatDefinition(
        name="Forget about it!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.GoingMyWay: CustomSpeedchatDefinition(
        name="Going my way?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.GoodForYou: CustomSpeedchatDefinition(
        name="Good for you!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.GoodGrief: CustomSpeedchatDefinition(
        name="Good grief.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HaveAGoodOne: CustomSpeedchatDefinition(
        name="Have a good one!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HeadsUp: CustomSpeedchatDefinition(
        name="Heads up!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HereWeGoAgain: CustomSpeedchatDefinition(
        name="Here we go again.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HowAboutThat: CustomSpeedchatDefinition(
        name="How about that!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HowDoYouLikeThat: CustomSpeedchatDefinition(
        name="How do you like that?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IBelieveSo: CustomSpeedchatDefinition(
        name="I believe so.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IThinkNot: CustomSpeedchatDefinition(
        name="I think not.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IllGetBackToYou: CustomSpeedchatDefinition(
        name="I'll get back to you.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImAllEars: CustomSpeedchatDefinition(
        name="I'm all ears.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImBusy: CustomSpeedchatDefinition(
        name="I'm busy.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImNotKidding: CustomSpeedchatDefinition(
        name="I'm not kidding!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImSpeechless: CustomSpeedchatDefinition(
        name="I'm speechless.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.KeepSmiling: CustomSpeedchatDefinition(
        name="Keep smiling.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LetMeKnow: CustomSpeedchatDefinition(
        name="Let me know!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LetThePieFly: CustomSpeedchatDefinition(
        name="Let the pie fly!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LikewiseImSure: CustomSpeedchatDefinition(
        name="Likewise, I'm sure.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LookAlive: CustomSpeedchatDefinition(
        name="Look alive!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.MyHowTimeFlies: CustomSpeedchatDefinition(
        name="My, how time flies.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.NoComment: CustomSpeedchatDefinition(
        name="No comment.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.NowYoureTalking: CustomSpeedchatDefinition(
        name="Now you're talking!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.OkayByMeDupe: CustomSpeedchatDefinition(
        name="Okay by me.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.PleasedToMeetYou: CustomSpeedchatDefinition(
        name="Pleased to meet you.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.RightoDupe: CustomSpeedchatDefinition(
        name="Righto.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SureThing: CustomSpeedchatDefinition(
        name="Sure thing.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThanksAMillionDupe: CustomSpeedchatDefinition(
        name="Thanks a million.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsMoreLikeIt: CustomSpeedchatDefinition(
        name="That's more like it.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsTheStuff: CustomSpeedchatDefinition(
        name="That's the stuff!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TimeForMeToHitTheHay: CustomSpeedchatDefinition(
        name="Time for me to hit the hay.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TrustMe: CustomSpeedchatDefinition(
        name="Trust me!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.UntilNextTime: CustomSpeedchatDefinition(
        name="Until next time.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WaitUp: CustomSpeedchatDefinition(
        name="Wait up!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WayToGo: CustomSpeedchatDefinition(
        name="Way to go!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WhatBringsYouHere: CustomSpeedchatDefinition(
        name="What brings you here?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WhatHappened: CustomSpeedchatDefinition(
        name="What happened?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WhatNow: CustomSpeedchatDefinition(
        name="What now?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouFirst: CustomSpeedchatDefinition(
        name="You first.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouTakeLeft: CustomSpeedchatDefinition(
        name="You take left.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouWish: CustomSpeedchatDefinition(
        name="You wish!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YoureToast: CustomSpeedchatDefinition(
        name="You're toast!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YoureTooMuch: CustomSpeedchatDefinition(
        name="You're too much!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontKeepMeWaiting: CustomSpeedchatDefinition(
        name="Don't keep me waiting!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontJudgeABookByItsCover: CustomSpeedchatDefinition(
        name="Don't judge a book by its cover.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LongTimeNoSee: CustomSpeedchatDefinition(
        name="Long time no see!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.PassTheSaltPlease: CustomSpeedchatDefinition(
        name="Pass the salt, please.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ItsTimeForTea: CustomSpeedchatDefinition(
        name="It's time for tea!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsAWrap: CustomSpeedchatDefinition(
        name="That's a wrap!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TryAgain: CustomSpeedchatDefinition(
        name="Try again.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.GetInLine: CustomSpeedchatDefinition(
        name="Get in line!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IsIt: CustomSpeedchatDefinition(
        name="Is it?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ProbablyNot: CustomSpeedchatDefinition(
        name="Probably not.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Ding: CustomSpeedchatDefinition(
        name="Ding!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IVolunteer: CustomSpeedchatDefinition(
        name="I volunteer!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.GoodToKnow: CustomSpeedchatDefinition(
        name="Good to know!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouHaveGoodTaste: CustomSpeedchatDefinition(
        name="You have good taste.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TheCogsAreNoMatchForUs: CustomSpeedchatDefinition(
        name="The Cogs are no match for us!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DohIMissed: CustomSpeedchatDefinition(
        name="Doh, I missed!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ICantBelieveYouveDoneThis: CustomSpeedchatDefinition(
        name="I can't believe you've done this!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ItsOver: CustomSpeedchatDefinition(
        name="It's OVER!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThisWasNotOurFinestMoment: CustomSpeedchatDefinition(
        name="This was not our finest moment.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YoureNotMyBoss: CustomSpeedchatDefinition(
        name="You're not my boss!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouCanNeverBeTooSafe: CustomSpeedchatDefinition(
        name="You can never be too 'safe'!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ToonsRule: CustomSpeedchatDefinition(
        name="Toons rule!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.CogsDrool: CustomSpeedchatDefinition(
        name="Cogs drool!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ToonsOfTheWorldUnite: CustomSpeedchatDefinition(
        name="Toons of the World, Unite!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HowdyPartner: CustomSpeedchatDefinition(
        name="Howdy, partner!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.MuchObliged: CustomSpeedchatDefinition(
        name="Much obliged.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.GetAlongLittleDoggie: CustomSpeedchatDefinition(
        name="Get along, little doggie.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImGoingToHitTheHay: CustomSpeedchatDefinition(
        name="I'm going to hit the hay.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImChompingAtTheBit: CustomSpeedchatDefinition(
        name="I'm chomping at the bit!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThisTownIsntBigEnoughForTheTwoOfUs: CustomSpeedchatDefinition(
        name="This town isn't big enough for the two of us!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SaddleUp: CustomSpeedchatDefinition(
        name="Saddle up!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Draw: CustomSpeedchatDefinition(
        name="Draw!!!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TheresGoldInThemThereHills: CustomSpeedchatDefinition(
        name="There's gold in them there hills!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HappyTrails: CustomSpeedchatDefinition(
        name="Happy trails!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThisIsWhereIRideOffIntoTheSunset: CustomSpeedchatDefinition(
        name="This is where I ride off into the sunset...",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LetsSkedaddle: CustomSpeedchatDefinition(
        name="Let's skedaddle!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouGotABeeInYourBonnet: CustomSpeedchatDefinition(
        name="You got a bee in your bonnet?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LandsSake: CustomSpeedchatDefinition(
        name="Lands sake!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.RightAsRain: CustomSpeedchatDefinition(
        name="Right as rain.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IReckonSo: CustomSpeedchatDefinition(
        name="I reckon so.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LetsRide: CustomSpeedchatDefinition(
        name="Let's ride!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WellGoFigure: CustomSpeedchatDefinition(
        name="Well, go figure!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImBackInTheSaddleAgain: CustomSpeedchatDefinition(
        name="I'm back in the saddle again!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.RoundUpTheUsualSuspects: CustomSpeedchatDefinition(
        name="Round up the usual suspects.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Giddyup: CustomSpeedchatDefinition(
        name="Giddyup!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ReachForTheSky: CustomSpeedchatDefinition(
        name="Reach for the sky.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImFixingTo: CustomSpeedchatDefinition(
        name="I'm fixing to.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HoldYourHorsesDupe: CustomSpeedchatDefinition(
        name="Hold your horses!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ICantHitTheBroadSideOfABarn: CustomSpeedchatDefinition(
        name="I can't hit the broad side of a barn.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YallComeBackNow: CustomSpeedchatDefinition(
        name="Y'all come back now.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ItsARealBarnBurner: CustomSpeedchatDefinition(
        name="It's a real barn burner!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontBeAYellowBelly: CustomSpeedchatDefinition(
        name="Don't be a yellow belly.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.FeelingLucky: CustomSpeedchatDefinition(
        name="Feeling lucky?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WhatInSamHillsGoinOnHere: CustomSpeedchatDefinition(
        name="What in Sam Hill's goin' on here?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ShakeYourTailFeathers: CustomSpeedchatDefinition(
        name="Shake your tail feathers!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WellDontThatTakeAll: CustomSpeedchatDefinition(
        name="Well, don't that take all.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsASightForSoreEyes: CustomSpeedchatDefinition(
        name="That's a sight for sore eyes!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.PickinsIsMightySlimAroundHere: CustomSpeedchatDefinition(
        name="Pickins is mighty slim around here.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TakeALoadOff: CustomSpeedchatDefinition(
        name="Take a load off.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ArentYouASight: CustomSpeedchatDefinition(
        name="Aren't you a sight!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatllLearnYa: CustomSpeedchatDefinition(
        name="That'll learn ya!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Unforgivable: CustomSpeedchatDefinition(
        name="Unforgivable.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IsThatIt: CustomSpeedchatDefinition(
        name="Is that it?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsIt: CustomSpeedchatDefinition(
        name="That's it!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsEnoughForMe: CustomSpeedchatDefinition(
        name="That's enough for me.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WeAreMintToBe: CustomSpeedchatDefinition(
        name="We are \"mint\" to be.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LettuceCelebrate: CustomSpeedchatDefinition(
        name="\"Lettuce\" celebrate!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LetsTacoAboutIt: CustomSpeedchatDefinition(
        name="Let's \"taco\" about it.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Glue: CustomSpeedchatDefinition(
        name="Glue!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.UnderstandableHaveANiceDay: CustomSpeedchatDefinition(
        name="Understandable, have a nice day.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LoveThatForYou: CustomSpeedchatDefinition(
        name="Love that for you!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ComeToThinkOfIt: CustomSpeedchatDefinition(
        name="Come to think of it...",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.AndFinally: CustomSpeedchatDefinition(
        name="And finally...",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IWantCandy: CustomSpeedchatDefinition(
        name="I want candy!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IveGotASweetTooth: CustomSpeedchatDefinition(
        name="I've got a sweet tooth.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsHalfBaked: CustomSpeedchatDefinition(
        name="That's half-baked.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.JustLikeTakingCandyFromABaby: CustomSpeedchatDefinition(
        name="Just like taking candy from a baby!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TheyreCheaperByTheDozen: CustomSpeedchatDefinition(
        name="They're cheaper by the dozen.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LetThemEatCake: CustomSpeedchatDefinition(
        name="Let them eat cake!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsTheIcingOnTheCake: CustomSpeedchatDefinition(
        name="That's the icing on the cake.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouCantHaveYourCakeAndEatItToo: CustomSpeedchatDefinition(
        name="You can't have your cake and eat it too.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IFeelLikeAKidInACandyStore: CustomSpeedchatDefinition(
        name="I feel like a kid in a candy store.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SixOfOneHalfADozenOfTheOther: CustomSpeedchatDefinition(
        name="Six of one, half a dozen of the other...",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LetsKeepItShortAndSweet: CustomSpeedchatDefinition(
        name="Let's keep it short and sweet.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DoughnutMindIfIDo: CustomSpeedchatDefinition(
        name="Doughnut mind if I do!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsPieInTheSky: CustomSpeedchatDefinition(
        name="That's pie in the sky.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ButItsWaferThin: CustomSpeedchatDefinition(
        name="But it's wafer thin.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LetsGumUpTheWorks: CustomSpeedchatDefinition(
        name="Let's gum up the works!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YoureOneToughCookie: CustomSpeedchatDefinition(
        name="You're one tough cookie!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsTheWayTheCookieCrumbles: CustomSpeedchatDefinition(
        name="That's the way the cookie crumbles.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LikeWaterForChocolate: CustomSpeedchatDefinition(
        name="Like water for chocolate.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.AreYouTryingToSweetTalkMe: CustomSpeedchatDefinition(
        name="Are you trying to sweet talk me?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ASpoonfulOfSugarHelpsTheMedicineGoDown: CustomSpeedchatDefinition(
        name="A spoonful of sugar helps the medicine go down.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouAreWhatYouEat: CustomSpeedchatDefinition(
        name="You are what you eat!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.EasyAsPie: CustomSpeedchatDefinition(
        name="Easy as pie!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontBeASucker: CustomSpeedchatDefinition(
        name="Don't be a sucker!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SugarAndSpiceAndEverythingNice: CustomSpeedchatDefinition(
        name="Sugar and spice and everything nice.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ItsLikeButter: CustomSpeedchatDefinition(
        name="It's like butter!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TheCandymanCan: CustomSpeedchatDefinition(
        name="The candyman can!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WeAllScreamForIceCream: CustomSpeedchatDefinition(
        name="We all scream for ice cream!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LetsNotSugarCoatIt: CustomSpeedchatDefinition(
        name="Let's not sugar coat it.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.KnockKnock: CustomSpeedchatDefinition(
        name="Knock knock...",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WhosThere: CustomSpeedchatDefinition(
        name="Who's there?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Lit: CustomSpeedchatDefinition(
        name="Lit!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IllSitThisOneOut: CustomSpeedchatDefinition(
        name="I'll sit this one out.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IfOnlyIHadAMillionJellybeans: CustomSpeedchatDefinition(
        name="If only I had a million jellybeans...",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Foreshadowing: CustomSpeedchatDefinition(
        name="Foreshadowing...",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YourePopular: CustomSpeedchatDefinition(
        name="You're popular!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.NotMe: CustomSpeedchatDefinition(
        name="Not me.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Kaboom: CustomSpeedchatDefinition(
        name="Kaboom!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.AsAMatterOfFact: CustomSpeedchatDefinition(
        name="As a matter of fact...",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IllComeBackToThatTomorrow: CustomSpeedchatDefinition(
        name="I'll come back to that tomorrow.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThisIsTooMuchForMe: CustomSpeedchatDefinition(
        name="This is too much for me.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WereGoingToBeSafeAndSound: CustomSpeedchatDefinition(
        name="We're going to be safe and sound!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HowArtThou: CustomSpeedchatDefinition(
        name="How art thou?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Howdyeth: CustomSpeedchatDefinition(
        name="Howdyeth!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontBurnethTheCandleAtBothEnds: CustomSpeedchatDefinition(
        name="Don't burneth the candle at both ends!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WhatDostThouNeedeth: CustomSpeedchatDefinition(
        name="What dost thou needeth?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.AsIf: CustomSpeedchatDefinition(
        name="As if!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Actually: CustomSpeedchatDefinition(
        name="Actually...",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.QuitMonkeyingAround: CustomSpeedchatDefinition(
        name="Quit monkeying around!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatReallyThrowsAMonkeyWrenchInThings: CustomSpeedchatDefinition(
        name="That really throws a monkey-wrench in things.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.MonkeySeeMonkeyDo: CustomSpeedchatDefinition(
        name="Monkey see, monkey do.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TheyMadeAMonkeyOutOfYou: CustomSpeedchatDefinition(
        name="They made a monkey out of you.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatSoundsLikeMonkeyBusiness: CustomSpeedchatDefinition(
        name="That sounds like monkey business.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImJustMonkeyingWithYou: CustomSpeedchatDefinition(
        name="I'm just monkeying with you.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WhosGonnaBeMonkeyInTheMiddle: CustomSpeedchatDefinition(
        name="Who's gonna be monkey in the middle?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsAMonkeyOffMyBack: CustomSpeedchatDefinition(
        name="That's a monkey off my back...",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThisIsMoreFunThanABarrelOfMonkeys: CustomSpeedchatDefinition(
        name="This is more fun than a barrel of monkeys!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WellIllBeAMonkeysUncle: CustomSpeedchatDefinition(
        name="Well I'll be a monkey's uncle.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IveGotMonkeysOnTheBrain: CustomSpeedchatDefinition(
        name="I've got monkeys on the brain.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WhatsWithTheMonkeySuit: CustomSpeedchatDefinition(
        name="What's with the monkey suit?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HearNoEvil: CustomSpeedchatDefinition(
        name="Hear no evil.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SeeNoEvil: CustomSpeedchatDefinition(
        name="See no evil.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SpeakNoEvil: CustomSpeedchatDefinition(
        name="Speak no evil.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LetsMakeLikeABananaAndSplit: CustomSpeedchatDefinition(
        name="Let's make like a banana and split.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ItsAJungleOutThere: CustomSpeedchatDefinition(
        name="It's a jungle out there.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YoureTheTopBanana: CustomSpeedchatDefinition(
        name="You're the top banana.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.CoolBananas: CustomSpeedchatDefinition(
        name="Cool bananas!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImGoingBananas: CustomSpeedchatDefinition(
        name="I'm going bananas!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LetsGetIntoTheSwingOfThings: CustomSpeedchatDefinition(
        name="Let's get into the swing of things!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThisPlaceIsSwinging: CustomSpeedchatDefinition(
        name="This place is swinging!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImDyingOnTheVine: CustomSpeedchatDefinition(
        name="I'm dying on the vine.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LetsMakeLikeATreeAndLeave: CustomSpeedchatDefinition(
        name="Let's make like a tree and leave.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThisWholeAffairHasMeUpATree: CustomSpeedchatDefinition(
        name="This whole affair has me up a tree.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.JellybeansDontGrowOnTrees: CustomSpeedchatDefinition(
        name="Jellybeans don't grow on trees!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsNotReal: CustomSpeedchatDefinition(
        name="That's not real!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YaLikeJazz: CustomSpeedchatDefinition(
        name="Ya like jazz?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LetThePiesFly: CustomSpeedchatDefinition(
        name="Let the pies fly!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WeDontSpeakOnThat: CustomSpeedchatDefinition(
        name="We don't speak on that.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.AMagicianShallNeverRevealTheirSecrets: CustomSpeedchatDefinition(
        name="A magician shall never reveal their secrets...",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.OoohWhatDoesThisButtonDo: CustomSpeedchatDefinition(
        name="Oooh, what does this button do?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.BuhBye: CustomSpeedchatDefinition(
        name="Buh-bye!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.MyFavoriteDayIsSundae: CustomSpeedchatDefinition(
        name="My favorite day is Sundae!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.FingersCrossed: CustomSpeedchatDefinition(
        name="Fingers crossed!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsCrazy: CustomSpeedchatDefinition(
        name="That's crazy!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Gadzooks: CustomSpeedchatDefinition(
        name="Gadzooks!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.AhoyMeHearties: CustomSpeedchatDefinition(
        name="Ahoy, me hearties!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontMissTheForestForTheTrees: CustomSpeedchatDefinition(
        name="Don't miss the forest for the trees.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IAgreeWithYourStatement: CustomSpeedchatDefinition(
        name="I agree with your statement.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IDisagreeWithYourStatement: CustomSpeedchatDefinition(
        name="I disagree with your statement.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TrueTrue: CustomSpeedchatDefinition(
        name="True, true.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThisPlaceIsAGhostTown: CustomSpeedchatDefinition(
        name="This place is a ghost town.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.NiceCostume: CustomSpeedchatDefinition(
        name="Nice costume!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IThinkThisPlaceIsHaunted: CustomSpeedchatDefinition(
        name="I think this place is haunted.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TrickOrTreat: CustomSpeedchatDefinition(
        name="Trick or Treat!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Boo: CustomSpeedchatDefinition(
        name="Boo!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HappyHaunting: CustomSpeedchatDefinition(
        name="Happy Haunting!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HappyHalloween: CustomSpeedchatDefinition(
        name="Happy Halloween!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ItsTimeForMeToTurnIntoAPumpkin: CustomSpeedchatDefinition(
        name="It's time for me to turn into a pumpkin.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Spooktastic: CustomSpeedchatDefinition(
        name="Spooktastic!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Spooky: CustomSpeedchatDefinition(
        name="Spooky!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsCreepy: CustomSpeedchatDefinition(
        name="That's creepy!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IHateSpiders: CustomSpeedchatDefinition(
        name="I hate spiders!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DidYouHearThat: CustomSpeedchatDefinition(
        name="Did you hear that?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouDontHaveAGhostOfAChance: CustomSpeedchatDefinition(
        name="You don't have a ghost of a chance!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouScaredMe: CustomSpeedchatDefinition(
        name="You scared me!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsSpooky: CustomSpeedchatDefinition(
        name="That's spooky!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsFreaky: CustomSpeedchatDefinition(
        name="That's freaky!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatWasStrange: CustomSpeedchatDefinition(
        name="That was strange....",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SkeletonsInYourCloset: CustomSpeedchatDefinition(
        name="Skeletons in your closet?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DidIScareYou: CustomSpeedchatDefinition(
        name="Did I scare you?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.FlippyNeedsYourHelp: CustomSpeedchatDefinition(
        name="Flippy needs your help!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HaveYouFoundTheScientistsYet: CustomSpeedchatDefinition(
        name="Have you found the scientists yet?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HaveYouSeenTheNewSpookyBuildingOnPolarPlace: CustomSpeedchatDefinition(
        name="Have you seen the new spooky building on Polar Place?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Spooktacular: CustomSpeedchatDefinition(
        name="Spooktacular!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatReallySendsAShiverDownMySpine: CustomSpeedchatDefinition(
        name="That really sends a shiver down my spine!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImTerrified: CustomSpeedchatDefinition(
        name="I'm terrified!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontBeAScaredyCat: CustomSpeedchatDefinition(
        name="Don't be a scaredy cat!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.PleaseParkAllYourBroomsAndPumpkinCartsAtTheDoor: CustomSpeedchatDefinition(
        name="Please park all your brooms and pumpkin carts at the door.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.EatDrinkAndBeScary: CustomSpeedchatDefinition(
        name="Eat, drink, and be scary!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WitchWayToTheTreats: CustomSpeedchatDefinition(
        name="Witch way to the treats?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.EnterIfYouDare: CustomSpeedchatDefinition(
        name="Enter if you dare...",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.BahHumbug: CustomSpeedchatDefinition(
        name="Bah! Humbug!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.BetterNotPout: CustomSpeedchatDefinition(
        name="Better not pout!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Brrr: CustomSpeedchatDefinition(
        name="Brrr!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ChillOut: CustomSpeedchatDefinition(
        name="Chill out!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ComeAndGetItDupe: CustomSpeedchatDefinition(
        name="Come and get it!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.DontBeATurkey: CustomSpeedchatDefinition(
        name="Don't be a turkey.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.GobbleGobble: CustomSpeedchatDefinition(
        name="Gobble gobble!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HappyHolidays: CustomSpeedchatDefinition(
        name="Happy holidays!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HappyNewYear: CustomSpeedchatDefinition(
        name="Happy New Year!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HappyThanksgiving: CustomSpeedchatDefinition(
        name="Happy Thanksgiving!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HappyTurkeyDay: CustomSpeedchatDefinition(
        name="Happy Turkey Day!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HoHoHo: CustomSpeedchatDefinition(
        name="Ho! Ho! Ho!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ItsSnowProblem: CustomSpeedchatDefinition(
        name="It's \"snow\" problem.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ItsSnowWonder: CustomSpeedchatDefinition(
        name="It's \"snow\" wonder.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LetItSnow: CustomSpeedchatDefinition(
        name="Let it snow!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.RakeEmIn: CustomSpeedchatDefinition(
        name="Rake 'em in.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SeasonsGreetings: CustomSpeedchatDefinition(
        name="Season's greetings!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SnowDoubtAboutIt: CustomSpeedchatDefinition(
        name="Snow doubt about it!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.SnowFarSnowGood: CustomSpeedchatDefinition(
        name="Snow far, snow good!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YuleBeSorry: CustomSpeedchatDefinition(
        name="Yule be sorry!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HaveAWonderfulWinter: CustomSpeedchatDefinition(
        name="Have a Wonderful Winter!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Festive: CustomSpeedchatDefinition(
        name="Festive!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IcyWhatYouDidThere: CustomSpeedchatDefinition(
        name="Icy what you did there.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.AllIWantForChristmasIsEwe: CustomSpeedchatDefinition(
        name="All I want for Christmas is ewe.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.BeMine: CustomSpeedchatDefinition(
        name="Be mine!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.BeMySweetie: CustomSpeedchatDefinition(
        name="Be my sweetie!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HappyValentoonsDay: CustomSpeedchatDefinition(
        name="Happy ValenToon's Day!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.AwwHowCute: CustomSpeedchatDefinition(
        name="Aww, how cute.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImSweetOnYou: CustomSpeedchatDefinition(
        name="I'm sweet on you.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ItsPuppyLove: CustomSpeedchatDefinition(
        name="It's puppy love.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.LoveYa: CustomSpeedchatDefinition(
        name="Love ya!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WillYouBeMyValentoon: CustomSpeedchatDefinition(
        name="Will you be my ValenToon?",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouAreASweetheart: CustomSpeedchatDefinition(
        name="You are a sweetheart.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouAreAsSweetAsPie: CustomSpeedchatDefinition(
        name="You are as sweet as pie.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouAreCute: CustomSpeedchatDefinition(
        name="You are cute.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouNeedAHug: CustomSpeedchatDefinition(
        name="You need a hug.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.Lovely: CustomSpeedchatDefinition(
        name="Lovely!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsDarling: CustomSpeedchatDefinition(
        name="That's darling!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.RosesAreRed: CustomSpeedchatDefinition(
        name="Roses are red...",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.VioletsAreBlue: CustomSpeedchatDefinition(
        name="Violets are blue...",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ThatsSweet: CustomSpeedchatDefinition(
        name="That's sweet!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ILoveYouMoreThanACogLovesOil: CustomSpeedchatDefinition(
        name="I love you more than a Cog loves oil!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YoureDynamite: CustomSpeedchatDefinition(
        name="You're dynamite!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.IOnlyHaveHypnoEyesForYou: CustomSpeedchatDefinition(
        name="I only have hypno-eyes for you!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YoureSweeterThanAJellybean: CustomSpeedchatDefinition(
        name="You're sweeter than a jellybean!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YoureValentoonTastic: CustomSpeedchatDefinition(
        name="You're ValenToon-tastic!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.AKissARooFromMeToYou: CustomSpeedchatDefinition(
        name="A kiss-a-roo from me to you!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.WeAreThePerfectPear: CustomSpeedchatDefinition(
        name="We are the perfect pear.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouArePurrFect: CustomSpeedchatDefinition(
        name="You are purr-fect.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImYourBiggestFan: CustomSpeedchatDefinition(
        name="I'm your biggest fan!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YoureTheIcingOnTheCake: CustomSpeedchatDefinition(
        name="You're the icing on the cake.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YoureTheAppleOfMyEye: CustomSpeedchatDefinition(
        name="You're the apple of my eye.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.TopOTheMorninToYou: CustomSpeedchatDefinition(
        name="Top o' the mornin' to you!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.HappyStPatricksDay: CustomSpeedchatDefinition(
        name="Happy St. Patrick's Day!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YoureNotWearingGreen: CustomSpeedchatDefinition(
        name="You're not wearing green!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ItsTheLuckOfTheIrish: CustomSpeedchatDefinition(
        name="It's the luck of the Irish.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.ImGreenWithEnvy: CustomSpeedchatDefinition(
        name="I'm green with envy.",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YouLuckyDog: CustomSpeedchatDefinition(
        name="You lucky dog!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YoureMyFourLeafClover: CustomSpeedchatDefinition(
        name="You're my four leaf clover!",
        description="A custom Speedchat phrase.",
    ),
    CustomSpeedchatItemType.YoureMyLuckyCharm: CustomSpeedchatDefinition(
        name="You're my lucky charm!",
        description="A custom Speedchat phrase.",
    ),
}

# Fill in the Localizer with all of these values
# This is for compatibility purposes with previous implementations of custom speedchat phrases
for itemEnum, itemDefinition in CustomSpeedchatRegistry.items():
    TTL.CustomSCStrings[itemEnum.value] = itemDefinition.getText()
