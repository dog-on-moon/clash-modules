from direct.fsm.FSM import FSM, RequestDenied
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory


@DirectNotifyCategory()
class SafeFSM(FSM):
    """
    This is shrimply an FSM that updates the defaultFilter function to ignore invalid requests instead of erroring.
    This tracks with the previous expected behavior of ClassicFSM, which will make porting more convenient.
    """

    def defaultFilter(self, request, args):
        try:
            return super().defaultFilter(request, args)
        except RequestDenied as rd:
            self.notify.warning(f'Safe FSM {self.__class__.__name__} ignored: {rd}')
            return None

    def hasStateNamed(self, stateName: str) -> bool:
        if not self.defaultTransitions:
            # We'll consider this FSM to have the state if they have either an enter or exit func
            return hasattr(self, f'enter{stateName[0].upper()}{stateName[1:]}') or \
                hasattr(self, f'exit{stateName[0].upper()}{stateName[1:]}')
        # We have defined transitions, just check if it's in there
        return stateName in self.defaultTransitions

    def request(self, request, *args):
        if request[0].islower():
            request = request[0].upper() + request[1:]
        return super().request(request, *args)

    def demand(self, request, *args):
        try:
            if request[0].islower():
                request = request[0].upper() + request[1:]
            return super().demand(request, *args)
        except RequestDenied as rd:
            self.notify.warning(f'Safe FSM {self.__class__.__name__} ignored: {rd}')
