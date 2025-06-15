"""
A slightly extended Toon for the BMP.
"""
import random
from toontown.battle.BattleAvatar import BattleAvatar
from toontown.effects import DustCloud
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.toon import TTEmote
from toontown.toon.Toon import Toon, loadDialog
from panda3d.core import TextNode, Point3, Vec4, ConfigVariableBool
from direct.interval.IntervalGlobal import *


loadDialog()


class BMPToon(Toon, BattleAvatar):
    HpTextGenerator = TextNode('HpTextGenerator')

    def __init__(self):
        Toon.__init__(self)
        BattleAvatar.__init__(self)
        self.hp = 1000
        self.maxHp = 1000
        self.hpText = None
        self.hpTextInterval = None
        self.immortalMode = 0
        self.soundSequenceList = []

    def showHpString(self, text, duration = 0.85, scale = 0.7, color = (1, 0, 0, 1)):
        if text != '':
            if self.hpText:
                self.hideHpText()
            self.HpTextGenerator.setFont(ToontownGlobals.getSignFont())
            self.HpTextGenerator.setText(text)
            self.HpTextGenerator.clearShadow()
            self.HpTextGenerator.setAlign(TextNode.ACenter)
            self.HpTextGenerator.setTextColor(color)
            self.hpTextNode = self.HpTextGenerator.generate()
            self.hpText = self.attachNewNode(self.hpTextNode)
            self.hpText.setScale(scale)
            self.hpText.setColorScaleOff(1)
            self.hpText.setBillboardAxis()
            self.hpText.setPos(0, 0, self.height / 2)

            def setAlphaScale(value):
                if self.hpText:
                    self.hpText.setAlphaScale(value)

            self.hpTextInterval = Sequence(
                self.hpText.posInterval(1.0, Point3(0, 0, self.height + 1.5), blendType='easeOut'), Wait(duration),
                LerpFunctionInterval(setAlphaScale, 0.5, fromData=1.0, toData=0.0),
                Func(self.hideHpText))
            self.hpTextInterval.start()

    def doEmote(self, emoteIndex, animMultiplier = 1, ts = 0, callback = None, extraArgs = []):
        self.emoteTrack, duration = TTEmote.globalEmote.doEmote(self, emoteIndex, ts)

    def setAnimState(self, animName, animMultiplier=1.0, timestamp=None, animType=None, callback=None, extraArgs=[]):
        if not animName or animName == 'None':
            return

        if timestamp is None:
            ts = 0.0
        else:
            ts = globalClockDelta.localElapsedTime(timestamp)

        if ConfigVariableBool('check-invalid-anims', True).getValue():
            if animMultiplier > 1.0 and animName in ['neutral']:
                animMultiplier = 1.0

        self.request(
            animName, 
            animMultiplier, ts, callback, extraArgs
        )

    def hideHpText(self):
        try:
            if self.hpText:
                taskMgr.remove(self.uniqueName('hpText'))
                self.hpText.removeNode()
                self.hpText = None
            if self.hpTextInterval:
                self.hpTextInterval.finish()
                self.hpTextInterval = None
        except:
            pass

    def getHp(self):
        return self.hp

    def getMaxHp(self):
        return self.maxHp

    def getDoId(self):
        return self.doId

    def takeDamage(self, hpLost, bonus=0, extraText=''):
        if self.hp is None or hpLost < 0:
            return
        oldHp = self.hp
        self.hp = max(self.hp - hpLost, 0)
        # hpLost = oldHp - self.hp  [this check caps the damage to max out at the toon's laff]
        if hpLost > 0:
            self.showHpText(-hpLost, bonus, extraText=extraText)

    def showHpText(self, number, bonus=0, scale=1, hasInteractivePropBonus=False, extraText=''):
        if number != 0 or extraText:
            if self.hpText:
                self.hideHpText()
            self.HpTextGenerator.setFont(ToontownGlobals.getSignFont())
            if number < 0:
                self.HpTextGenerator.setText(str(number))
            else:
                hpGainedStr = '+' + str(number)
                if hasInteractivePropBonus:
                    hpGainedStr += '\n' + TTLocalizer.InteractivePropTrackBonusTerms[0]
                self.HpTextGenerator.setText(hpGainedStr)
            if extraText:
                self.HpTextGenerator.setText(self.HpTextGenerator.getText() + f'\n{extraText}')
            self.HpTextGenerator.clearShadow()
            self.HpTextGenerator.setAlign(TextNode.ACenter)
            if bonus == 1:
                r = 1.0
                g = 1.0
                b = 0
                a = 1
            elif bonus == 2:
                r = 1.0
                g = 0.5
                b = 0
                a = 1
            elif number < 0:
                r = 0.9
                g = 0
                b = 0
                a = 1
            else:
                r = 0
                g = 0.9
                b = 0
                a = 1
            self.HpTextGenerator.setTextColor(r, g, b, a)
            self.hpTextNode = self.HpTextGenerator.generate()
            self.hpText = self.attachNewNode(self.hpTextNode)
            self.hpText.setScale(scale)
            self.hpText.setColorScaleOff(1)
            self.hpText.setBillboardPointEye()
            self.hpText.setBin('fixed', 100)
            self.hpText.setPos(0, 0, self.height / 2)

            def setAlphaScale(value):
                if self.hpText:
                    self.hpText.setAlphaScale(value)

            self.hpTextInterval = Sequence(
                self.hpText.posInterval(1.0, Point3(0, 0, self.height + 1.5), blendType='easeOut'),
                Wait(0.85),
                LerpFunctionInterval(setAlphaScale, 0.5, fromData=1.0, toData=0.0),
                Func(self.hideHpText)
            )
            self.hpTextInterval.start()

    def toonUp(self, hpGained, hasInteractivePropBonus=False, extraText='', force=False):
        if self.hp is None or hpGained < 0:
            return
        oldHp = self.hp
        if self.hp + hpGained <= 0:
            self.hp += hpGained
        else:
            self.hp = min(max(self.hp, 0) + hpGained, self.maxHp)

        hpGained = self.hp - max(oldHp, 0)
        if hpGained > 0 or force:
            self.showHpText(hpGained, hasInteractivePropBonus=hasInteractivePropBonus, extraText=extraText)
            self.hpChange(quietly=0)

    def hpChange(self, quietly = 0):
        pass

    def doDustCloud(self):
        dustCloud = DustCloud.DustCloud(fBillboard = 0, wantSound = 1)
        dustCloud.setBillboardAxis(2.0)
        dustCloud.setZ(3)
        dustCloud.setScale(0.4)
        dustCloud.createTrack()

        s = Sequence(Func(dustCloud.reparentTo, self), dustCloud.track, Func(dustCloud.destroy), name = 'dustCloudIval')
        s.start()

    def uniqueName(self, s):
        return f'{s}-{id(self)}'

    def playDialogueForString(self, chatString, delay = 0.0):
        if len(chatString) == 0:
            return

        searchString = chatString.lower()
        if searchString.find(TTLocalizer.DialogSpecial) >= 0:
            type = 'special'
        elif searchString.find(TTLocalizer.DialogExclamation) >= 0:
            type = 'exclamation'
        elif searchString.find(TTLocalizer.DialogQuestion) >= 0:
            type = 'question'
        elif searchString.find(TTLocalizer.DialogIndifferent) >= 0:
            type = 'indifferent'
        elif random.randint(0, 1):
            type = 'statementA'
        else:
            type = 'statementB'

        stringLength = len(chatString)
        if stringLength <= TTLocalizer.DialogLength1:
            length = 1
        elif stringLength <= TTLocalizer.DialogLength2:
            length = 2
        elif stringLength <= TTLocalizer.DialogLength3:
            length = 3
        else:
            length = 4

        self.playDialogue(type, length, delay)

    def playDialogue(self, type, length, delay = 0.0):
        dialogueArray = self.getDialogueArray()
        if dialogueArray is None:
            return
        sfxIndex = None
        if type == 'statementA' or type == 'statementB':
            if length == 1:
                sfxIndex = 0
            elif length == 2:
                sfxIndex = 1
            elif length >= 3:
                sfxIndex = 2
        elif type == 'question':
            sfxIndex = 3
        elif type == 'exclamation':
            sfxIndex = 4
        elif type == 'special':
            if length == 1:
                sfxIndex = 5
            elif length == 2:
                sfxIndex = 6
            elif length >= 3:
                sfxIndex = 7
        elif type == 'indifferent':
            sfxIndex = 8
        else:
            self.notify.error('unrecognized dialogue type: ', type)

        if sfxIndex is not None and sfxIndex < len(dialogueArray) and dialogueArray[sfxIndex] is not None:
            sfx = dialogueArray[sfxIndex]
            soundSequence = Sequence(
                Wait(delay),
                SoundInterval(sfx, listenerNode = base.localAvatar, loop = 0, volume = 1.0)
            )
            if base.audio3d:
                base.audio3d.attachSoundToObject(sfx, self)
                soundSequence = Sequence(
                    Wait(delay),
                    SoundInterval(sfx, listenerNode = base.localAvatar, loop = 0, volume = 1.0),
                    Func(base.audio3d.detachSound, sfx)
                )

            self.soundSequenceList.append(soundSequence)
            soundSequence.start()
            self.cleanUpSoundList()

    def cleanUpSoundList(self):
        removeList = []
        for soundSequence in self.soundSequenceList:
            if soundSequence.isStopped():
                removeList.append(soundSequence)

        for soundSequence in removeList:
            self.soundSequenceList.remove(soundSequence)
