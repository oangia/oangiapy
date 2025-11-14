<?php

namespace App\PokerV2\Hand;

/**
  * HandDetect
  * 
  * @package    Poker
  * @author     oangia <hqnhatdn@gmail.com>
  *
  */

class HandDetect
{
    private     $cards              = [];
    private     $values             = [];
    private     $pips               = [];
    private     $valuesCount        = [];
    private     $pipsCount          = [];
    private     $flush              = false;
    private     $chiAt              = false;

    function __construct($chiAt = false)
    {
        $this->chiAt = $chiAt;
    }

    public function detect($cards)
    {
        $this->cards = $cards;
        $this->values = array_map(function($card) {return $card->value;}, $this->cards);
        $this->pips = array_map(function($card) {return $card->pip;}, $this->cards);
        $this->valuesCount = array_count_values($this->values);
        $this->pipsCount = array_count_values($this->pips);
        $this->flush = count($this->pipsCount) == 1;

        switch (count($this->cards)) {
            case 3:
                return $this->frontDetect();
            case 5:
                return $this->backDetect();
        }
    }

    private function frontDetect()
    {
        switch (count($this->valuesCount)) {
            case 1:
                return new ThreeKind($this->cards);
            case 2:
                return new OnePair($this->cards);
            case 3:
                $zitch = new Zitch($this->cards);
                if (
                    $this->cards[1]->value + 1 == $this->cards[2]->value
                    && (
                        $this->cards[0]->value + 1 == $this->cards[1]->value
                        || $this->cards[0]->value + 12 == $this->cards[2]->value
                    )
                ) {
                    $zitch->isStraight = true;
                }
                if ($this->flush) {
                    $zitch->isFlush = true;
                }
                return $zitch;
        }
    }

    private function backDetect()
    {
        switch (count($this->valuesCount)) {
            case 2:
                foreach ($this->valuesCount as $item) {
                    if ($item == 4) {
                        return new FourKind($this->cards);
                    }
                    if ($item == 3) {
                        return new FullHouse($this->cards);
                    }
                }
            case 3:
                foreach ($this->valuesCount as $item) {
                    if ($item == 3) {
                        return new ThreeKind($this->cards);
                    }
                    if ($item == 2) {
                        return new TwoPair($this->cards);
                    }
                }
            case 4:
                return new OnePair($this->cards);
            case 5;
                if ($this->isStraight($this->cards)) {
                    return $this->flush ? new StraightFlush($this->cards, $this->chiAt) : new Straight($this->cards, $this->chiAt);
                }
                return $this->flush ? new Flush($this->cards) : new Zitch($this->cards);
        }
    }

    private function isStraight($cards)
    {
        if (
            $cards[1]->value + 1 == $cards[2]->value
            && $cards[2]->value + 1 == $cards[3]->value
            && $cards[3]->value + 1 == $cards[4]->value
            && (
                $cards[0]->value + 1 == $cards[1]->value
                || $cards[0]->value + 12 == $cards[4]->value
            )
        ) {
            return true;
        }
        return false;
    }
}
