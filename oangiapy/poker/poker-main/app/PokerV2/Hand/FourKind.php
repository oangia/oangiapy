<?php

namespace App\PokerV2\Hand;

/**
  * FourKind
  * 
  * @package    Poker
  * @author     oangia <hqnhatdn@gmail.com>
  *
  */

class FourKind extends Hand
{
    public      $level              = 8;
    public      $instance           = 'FourKind';

    public function pointCalc()
    {
        $this->point = round(($this->cards[2]->pointValue/12) * 100, 4);
    }
}
