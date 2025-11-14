<?php

namespace App\PokerV2\Hand;

use App\PokerV2\Card;

/**
  * Hand
  * 
  * @package    Poker
  * @author     oangia <hqnhatdn@gmail.com>
  *
  */

class Hand
{
    const       ZITCH               = 1;
    const       ONEPAIR             = 2;
    const       TWOPAIR             = 3;
    const       THREEKIND           = 4;
    const       STRAIGHT            = 5;
    const       FLUSH               = 6;
    const       FULLHOUSE           = 7;
    const       FOURKIND            = 8;
    const       STRAIGHTFLUSH       = 9;

    public      $point              = 0;
    public      $zitchPoint         = 0;
    public      $cards              = [];
    public      $chiAt              = false;

    function __construct(array $cards, $chiAt = false)
    {
        $this->cards = $cards;
        $this->chiAt = $chiAt;
        $this->pointCalc();
    }

    public function compare(Hand $hand, $zitch = false)
    {
        if ($this->level < $hand->level) return -1;
        if ($this->level > $hand->level) return 1;
        if ($this->level == $hand->level) {
            if ($this->point > $hand->point){
                return 1;
            }
            if ($this->point < $hand->point) {
                return -1;
            }
            if ($this->point == $hand->point) {
                return ($zitch) ? $this->compareZitchPoint($hand) : 0;
            }
        }
    }

    public function compareZitchPoint(Hand $hand)
    {
        if ($this->zitchPoint > $hand->zitchPoint) {
            return 1;
        }
        if ($this->zitchPoint < $hand->zitchPoint) {
            return -1;
        }
        if ($this->zitchPoint == $hand->zitchPoint) {
            return 0;
        }
    }

    public function duplicate(Hand $hand)
    {
        foreach ($this->cards as $card) {
            foreach ($hand->cards as $card2) {
                if ($card->name == $card2->name) {
                    return true;
                }
            }
        }
        return false;
    }

    public function duplicateCard(Card $card)
    {
        foreach ($this->cards as $item) {
            if ($item->name == $card->name) {
                return true;
            }
        }
        return false;
    }

    public function toString()
    {
        $str = '';
        foreach ($this->cards as $card) {
            $str .= $card->name . ',';
        }
        return trim($str, ',');
    }

    public function visualize() {
        $str = '';
        foreach ($this->cards as $card) {
            $str .= $card->visualize();
        }
        return $str;
    }
}
