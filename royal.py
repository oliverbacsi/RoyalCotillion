#!/usr/bin/env python3

#################### INIT PART ####################

import curses
import random

num :list = list(("_", "A", "2", "3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K"))
col :list = list(("♠", "♣", "♥", "♦"))
X   :int  = 0
Y   :int  = 0
vege :bool = False
_sum :int = -1

scr = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
scr.keypad(True)
curses.curs_set(False)
curses.nonl()
scr.refresh()

for b in range(0,8):
    for f in range(0,8) :
        if b+f :
            curses.init_pair(10*f+b,f,b)



#################### CLASS PART ####################

class Game:

    def __init__(self):
        """
        Define the main game object
        """
        global X, Y
        self.WastePile  :list = list(())
        self.Foundation :list = list(())
        self.Field      :list = list(())
        self.Deck       :list = list(())
        self.HelpMode   :bool = False

        for i in range(0,8): self.Foundation.append(list(()))
        for i in range(0,4): self.Field.append(list(()))
        for i in range(0,2): self.WastePile.append(list(()))

        Tarhely :list = list(())
        for i in range(0,104) : Tarhely.append(i%13 +1 + 16*((i//13)%4))
        for i in range(0,4):
            for j in range(0,3): self.Field[i].append(Tarhely.pop(random.randint(0,len(Tarhely)-1)))
        for i in range(0,16): self.Deck.append(Tarhely.pop(random.randint(0,len(Tarhely)-1)))
        self.WastePile[1].append(Tarhely.pop(random.randint(0,len(Tarhely)-1)))
        for i in range(0,75): self.WastePile[0].append(Tarhely.pop(random.randint(0,len(Tarhely)-1)))

        X, Y = 0, 0
        scr.bkgd(" ",curses.color_pair(7))
        scr.clear()
        self.ScreenFresh()


    def ScreenFresh(self) -> None:
        """
        Update the whole game screen based on the current status of the game
        :return: None
        """
        global col, X, Y
        HaveSel :bool =False

        scr.addstr(0,33,"ROYAL COTILLION",curses.color_pair(17))
        for i in range(0,8):
            _col = curses.color_pair(17) if i>3 else curses.color_pair(7)
            scr.addstr(4+(i//2)*6, 36+(i%2)*7, col[i//2]*2, _col)
            scr.addstr(5+(i//2)*6, 36+(i%2)*7, col[i//2]*2, _col)

        for i in range(0,2):
            if len(self.WastePile[i]):
                v = self.WastePile[i][-1]
            else:
                v = 0
            HaveSel = HaveSel | self.PutCard(i, 0, v, False, True)
            if v: scr.addstr(8, i*7+6, str(len(self.WastePile[i])), curses.color_pair(7))
            for j in range(0,4):
                if len(self.Foundation[j*2+i]):
                    v = self.Foundation[j*2+i][-1]
                    if v : self.PutCard(i*7+34, j*6+2, v, True, False)
        for i in range(0,4):
            for j in range(1,4) : self.PutCard(i, j, 0, False, False)
            for j in range(0,len(self.Field[i])) : HaveSel = HaveSel | self.PutCard(i, j+1, self.Field[i][j], False, True)
            for j in range(0,4) : HaveSel = HaveSel | self.PutCard(i+4, j, self.Deck[j*4+i], False, True)

        if (X==2) and (Y==0) :
            _col=33
            HaveSel=True
        else:
            _col=22
        scr.addstr(2,18,"╔════╗",curses.color_pair(_col)|curses.A_BOLD)
        scr.addstr(3,18,"║New ║",curses.color_pair(_col)|curses.A_BOLD)
        scr.addstr(4,18,"╚════╝",curses.color_pair(_col)|curses.A_BOLD)
        if (X==3) and (Y==0) :
            _col=33
            HaveSel=True
        else:
            _col=55
        scr.addstr(2,25,"╔════╗",curses.color_pair(_col)|curses.A_BOLD)
        scr.addstr(3,25,"║Quit║",curses.color_pair(_col)|curses.A_BOLD)
        scr.addstr(4,25,"╚════╝",curses.color_pair(_col)|curses.A_BOLD)
        scr.addstr(28,1,"▶"*(len(self.WastePile[0])-1),curses.color_pair(44)|curses.A_BOLD)
        if len(self.WastePile[0]): scr.addstr("◆",curses.color_pair(33)|curses.A_BOLD)
        if len(self.WastePile[1]): scr.addstr("◆",curses.color_pair(33)|curses.A_BOLD)
        scr.addstr("◀"*(len(self.WastePile[1])-1),curses.color_pair(11)|curses.A_BOLD)
        if self.HelpMode:
            scr.addstr(6,22," HELP ",curses.color_pair(64))
        else:
            scr.addstr(6,22,"      ", curses.color_pair(7))
        if not HaveSel: self.PutCard(X, Y, 0, False, False)
        scr.refresh()


    def PullCard(self) -> int:
        """
        Pull a card from the best WastePile and return it (automatic pull to fill the Deck)
        :return: The Card value itself as int
        """
        global X, Y
        ret :int =-1

        if len(self.WastePile[1]):
            ret = self.WastePile[1].pop()
            Animate(ret, xcoord(1), ycoord(0,1), xcoord(X), ycoord(Y,X))
            return ret
        if len(self.WastePile[0]):
            ret = self.WastePile[0].pop()
            Animate(ret, xcoord(0), ycoord(0,0), xcoord(X), ycoord(Y,X))
            return ret
        return 0


    def PutCard(self, _XPos :int =-1, _YPos :int =-1, _Value :int =255, _DirectMode :bool =False, _AllowHelp :bool =True) -> bool:
        """
        Display a card to a logical card position on the screen.
        Do NOT refresh the curses window, as generally more cards are drawn at the same time,
        so the caller procedure should handle it.
        :param _XPos: Logical X position of the card
        :param _YPos: Logical Y position of the card
        :param _Value: The value of the card to display
        :param _DirectMode: If true, no coordinate transformation is done between logical and screen
        :param _AllowHelp: If false, the card is not allowed to be drawn with the help highlight color (cyan)
        :return: Whether a Selected (highlighted) card was drawn or not : bool
            (to evaluate the need to draw a cursor marker)
        """
        global col, num, X, Y

        _MyX :int = _XPos
        _MyY :int = _YPos
        _Sel :bool = False
        if not _DirectMode:
            _MyX = xcoord(_XPos)
            _MyY = ycoord(_YPos, _XPos)
            _Sel = (_XPos == X) and (_YPos == Y)

        T :int = _Value//16
        E :int = _Value%16
        if T > 3 and _Value != 255 : _Value = 255
        if E >13 and _Value != 255 : _Value = 255
        if E < 0 and _Value !=   0 : _Value = 0

        _colr :int =7
        if _AllowHelp and self.HelpMode and self.TryFoundation(_Value, False): _colr=6
        if _Sel: _colr=3 if _colr==7 else 2

        if not _Value:
            for j in range(0,6): scr.addstr(_MyY+j, _MyX, "      ", curses.color_pair(_colr))
            return _Sel
        scr.addstr(_MyY, _MyX, "┌────┐", curses.color_pair(_colr))
        for j in range(1,5): scr.addstr(_MyY+j, _MyX, "│    │", curses.color_pair(_colr))
        scr.addstr(_MyY+5, _MyX, "└────┘", curses.color_pair(_colr))
        if _Value == 255:
            for j in range(1, 5): scr.addstr(_MyY+j, _MyX, "####", curses.color_pair(7))
            return _Sel
        if T > 1 : _colr += 10
        scr.addstr(_MyY+1, _MyX+1, col[T]+num[E], curses.color_pair(_colr))
        scr.addstr(_MyY+4, _MyX+3, num[E]+col[T], curses.color_pair(_colr))
        return _Sel


    def TryFoundation(self, _Value :int =-1, _PerformMove :bool =False) -> bool:
        """
        Assess if <_Value> is accepted by any of the foundations (return True if accepted),
        and also actually perform the card move if <_PerformMove> is True.
        Backdraw: Can not select which foundation of the 2 if both are accepting,
        but "best guess" is the lower one, as it has more "future"...
        :param _Value: Card Value to check
        :param _PerformMove: Actually move the Card pysically to the accepting Foundation
        :return: True if card can be moved to the foundation.
        """

        # This is the index of the left one of the potential 2 Foundations
        c :int = _Value //16 *2
        # By default both Foundations accept the value, set to False later on
        ac :list = list((True, True))
        # Accepted values without color is:
        acv :list = list((-1,-1))
        # better cell id if both are OK
        _colmn :int =-1

        # Not try to catch such cases if Foundation does not accept the card
        for i in range(0,2):
            if len(self.Foundation[c+i]) > 12:
                ac[i] = False
            else:
                if not len(self.Foundation[c+i]):
                    acv[i] = i+1
                else:
                    acv[i] = self.Foundation[c+i][-1] %16 +2
                    if acv[i] > 13 : acv[i] -= 13
                if acv[i] != _Value%16: ac[i] = False

        if not (ac[0] or ac[1]) : return False
        if not _PerformMove: return True
        if ac[0]:
            if ac[1]:
                if len(self.Foundation[c]) < len(self.Foundation[c+1]):
                    _colmn = c
                else:
                    _colmn = c+1
            else:
                _colmn = c
        else:
            _colmn = c+1
        Animate(_Value, xcoord(X), ycoord(Y,X), 34+(_colmn%2)*7, 2+(_colmn//2)*6)
        self.Foundation[_colmn].append(_Value)
        return True


    def triggerHelp(self) -> None:
        """
        Trigger the help mode on and off.
        :return: None
        """
        self.HelpMode = not self.HelpMode



#################### PROCS PART ####################


def xcoord(_pos :int) -> int:
    """
    Return the screen X coordinate of a logical card position
    :param _pos: Logical Card X position (0..7)
    :return: Screen X coordinate
    """
    if _pos > 3:
        return _pos*7+22
    else:
        return _pos*7+4

def ycoord(_pos :int, _x :int) -> int:
    """
    Return the screen Y coordinate of a logical card position
    :param _pos: Logical Card Y position (0..3)
    :param _x:   Logical Card X position (0..7)
    :return: Screen Y coordinate
    """
    if _x > 3:
        return _pos*6+2
    else:
        return _pos*2+9 if _pos else 2


def Animate(a_value :int, a_strx :int, a_stry :int, a_endx :int, a_endy :int) -> None:
    """
    Animate a card move on the screen
    :param a_value: The card value to show during animation
    :param a_strx: Starting Screen X coordinate
    :param a_stry: Starting Screen Y coordinate
    :param a_endx: Ending Screen X coordinate
    :param a_endy: Ending Screen Y coordinate
    :return: None
    """
    a_dx :int = a_endx-a_strx
    a_dy :int = a_endy-a_stry

    if abs(a_dy) < abs(a_dx):
        _dif = 1 if a_dx > 0 else -1
        for a_seg in range(0,a_dx,_dif):
            game.PutCard(a_strx+a_seg, int(a_stry+a_seg*a_dy/a_dx), a_value, True, True)
            scr.refresh()
            curses.delay_output(10)
    else:
        _dif = 1 if a_dy > 0 else -1
        for a_seg in range(0,a_dy,_dif):
            game.PutCard(int(a_strx+a_seg*a_dx/a_dy), a_stry+a_seg, a_value, True, True)
            scr.refresh()
            curses.delay_output(10)
    game.PutCard(a_endx, a_endy, a_value, True, True)
    scr.refresh()
    curses.delay_output(100)



#################### MAIN PART ####################

scr.bkgd(" ", curses.color_pair(7))
scr.clear()
Line :int =0
for txt in list(("#"*72, "# ROYAL COTILLION", "# ===============", "#",
    "# A Patience game written in Python using curses library.", "#", "#RULES:",
    "# Move all cards to the 8 Foundations in the middle of the screen,",
    "#  creating piles of the same color, containing all cards from one set.",
    "#  In the left Foundation starting from Ace, in the right Foundation",
    "#  starting from Two, and the following cards increasing by 2.",
    "#  So on the top of 5 You can only put 7 from the same color.",
    "# The game is complete if all 13 cards from one set are placed",
    "#  on each Foundation, with values increasing by 2",
    "# You can use any card from the Deck in the right half of the screen,",
    "#  or the topmost cards from the Fields in the bottom-left quarter,",
    "#  or the topmost cards of the two Piles in the upper-left corner.",
    "# Initially all new cards are in the fresh Pile (top left),",
    "#  and scrapped cards are collected in the Wastepile (right beside it).",
    "# If no cards can be put into the Foundations, scrap one card",
    "#  from the top of the fresh Pile to the Wastepile.",
    "# Take care of the Wastepile though, as it can NOT be rolled back",
    "#  to the fresh Pile any more! You can only access its top card!",
    "# Therefore the height of the two Piles are indicated with numbers below them.",
    "# A blue-red slider at the very bottom of the screen also displays the same",
    "#  in a graphical way. Yellow characters mean the visible cards on the Piles.",
    "# The cards from the Deck are replenished automatically from the Wastepile,",
    "#  while the Field is not replenished, it is single use.", "#",
    "#CONTROLS:", "# * Use the [CRSR] and [HOME] keys to navigate the highlight on the screen.",
    "# * Hit the [Space bar] to invoke the highlighted area:",
    "#   Either one of the two functional buttons (New or Quit),",
    "#   Or try to move the highlighted Card to the Foundations.",
    "#   In case of the fresh Pile the top card is tried for the Foundations,",
    "#   if it's not possible, then scrap it to the Wastepile.",
    "# * [n] invokes New Game, [q] invokes instant Quit, and",
    "#   [h] triggers the Help Mode on/off. In the Help Mode all cards are",
    "#   highlighted with cyan which could be moved to any of the Foundations.", "#",
    "#   HAVE FUN !", "#")):
    scr.addstr(Line, 0, txt, curses.color_pair(7))
    Line += 1
scr.refresh()
ch = scr.getch()

game = Game()

while not vege:
    game.ScreenFresh()

    _sum = 0
    for q in range(0,8): _sum += len(game.Foundation[q])
    if _sum == 104:
        scr.addstr(10, 34, "############", curses.color_pair(46))
        scr.addstr(11, 34, "#          #", curses.color_pair(46))
        scr.addstr(12, 34, "# YOU WON! #", curses.color_pair(46))
        scr.addstr(13, 34, "#          #", curses.color_pair(46))
        scr.addstr(14, 34, "############", curses.color_pair(46))
        scr.getch()
        game = Game()

    ch = scr.getch()
    if ch == curses.KEY_UP    : Y = (Y-1)%4
    if ch == curses.KEY_DOWN  : Y = (Y+1)%4
    if ch == curses.KEY_LEFT  : X = (X-1)%8
    if ch == curses.KEY_RIGHT : X = (X+1)%8
    if ch == curses.KEY_HOME  : X, Y = 0, 0
    if ch == ord('q')         : vege = True
    if ch == ord('n')         : game = Game()
    if ch == ord('h')         : game.triggerHelp()

    if ch == ord(' ') :

        # Enter was it on a control button
        if (Y==0) and (X==2) :
            game = Game()
            continue
        if (Y==0) and (X==3) :
            vege = True
            continue

        # Enter was hit on the Deck
        if X > 3:
            V = game.Deck[X-4 + Y*4]
            if not V : continue
            if game.TryFoundation(V, True):
                game.Deck[X-4 + Y*4] = game.PullCard()
                scr.clear()
            continue

        # Enter was hit on the Field
        if Y > 0:
            if Y != len(game.Field[X]) : continue
            V = game.Field[X][-1]
            if not V : continue
            if game.TryFoundation(V, True):
                game.Field[X].pop()
                scr.clear()
            continue

        # Enter was hit on the Wastepile
        if not len(game.WastePile[X]) : continue
        V = game.WastePile[X][-1]
        if not V : continue
        if game.TryFoundation(V, True):
            game.WastePile[X].pop()
            scr.clear()
        else:
            if not X:
                Animate(V, 4, 2, 11, 2)
                game.WastePile[1].append(game.WastePile[0].pop())
                scr.clear()


curses.curs_set(True)
curses.nl()
scr.keypad(False)
curses.nocbreak()
curses.echo()
curses.endwin()
