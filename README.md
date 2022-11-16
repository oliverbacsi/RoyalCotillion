# ROYAL COTILLION
---

> A Solitaire card game written in Python using the curses library.

![Screenshot](https://github.com/oliverbacsi/RoyalCotillion/blob/main/screenshot.png)

#####RULES:

* The goal is to move all cards to the **Foundations** in the middle of the screen:
	* One Foundation can accept cards from one color
	* The left Foundation starts with an **`Ace`**, the right one with a **`Two`**
	* The Cards on one Foundation can be only put down in ascending order with a sequence step of 2:
		* On the Left Foundation the sequence will be: `A` `3` `5` `7` `9` `J` `K` `2` `4` `6` `8` `10` `Q`
		* On the Right Foundation the sequence will be: `2` `4` `6` `8` `10` `Q` `A` `3` `5` `7` `9` `J` `K`
	* One Foundation is complete if all 13 cards of one set are put on it, then it accepts no cards any more.
* The right half of the screen is the **Deck** (4x4 cards), You can use any cards to put to the Foundations.
* The bottom left quarter of the screen is the **Field** (4x3 cards), You can only use the topmost card of all 4 columns for the Foundations, the lower cards are blocked by the upper cards.
* In the top left corner there are two **Piles** of cards:
	* The left one is the **Fresh Pile** with lots of spare cards. You can pull a new card from here any time. Only the top card is accessible and can be used for the Foundations.
	* The right one is the **Wastepile**. Cards taken from the Fresh Pile that can not be used for the Foundations are scrapped here. Only the top card is accessible and can be used for the foundations.
* You need to take care about the size of the Wastepile though, as the cards collected here can not be rolled back to the fresh pile any more. You can only pick the top cards one by one if possible.
	* Therefore the sizes of the two Piles are indicated with numbers below the piles.
	* As well as there is a graphical bar at the bottom of the screen representing the same:
		* Blue bar: not visible cards of the Fresh Pile
		* Yellow chars: visible card(s) of the pile(s)
		* Red bar: not visible cards of the Wastepile
* **Replenishment of the used cards of the areas:**
	* Cards removed from the Deck are replenished from the Wastepile (this is a good method to reduce the Wastepile), if not possible then from the Fresh Pile, if this is also not possible, then both Piles are already empty, then the Deck is not replenished any more.
	* Cards removed from the Field are not replenished. These cards are "spare" and single use. If they are gone, they are gone.
	* Cards removed from the two Piles are just decreasing the size of the Piles, even if this means running the Pile completely empty.


#####CONTROLS:

* **`CRSR`** keys and the **`HOME`** key navigate the highlighted area on the screen
* **`SPACE`** invokes the object under the highlight:
	* In case of a functional button: the function is invoked
	* In case of a Card: the Card is tried to move to the foundations
	* For the fresh Pile if the topmost Card can not be moved to the Foundations then it is scrapped to the Wastepile
* **`N`** will initiate a New Game
* **`Q`** will instantly Quit the game
* **`H`** triggers the Help Mode on and off
	* In the Help Mode all cards are highlighted which can be accepted by any of the 8 Foundations

#####TODO:

* [ ] ...

#####BUGS:

* [ ] ...
