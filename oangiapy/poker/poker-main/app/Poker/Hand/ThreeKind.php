<?php

namespace App\Poker\Hand;

/**
  * FourKind
  * 
  * @package    Poker
  * @author     oangia <hqnhatdn@gmail.com>
  *
  */

class ThreeKind extends Hand
{
    public      $level              = 4;
    public      $instance           = 'ThreeKind';

    public function pointCalc()
    {
        $this->point = round(($this->cards[((count($this->cards) - 1) / 2)]->pointValue/12) * 100, 4);
    }
}
