<?php

namespace App\Poker\Hand;

/**
  * FullHouse
  * 
  * @package    Poker
  * @author     oangia <hqnhatdn@gmail.com>
  *
  */

class FullHouse extends Hand
{
    public      $level 	            = 7;
    public      $instance           = 'FullHouse';

    public function pointCalc()
    {
        $this->point = round(($this->cards[2]->pointValue/12) * 100, 4);
    }
}
