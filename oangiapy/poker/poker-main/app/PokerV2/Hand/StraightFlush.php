<?php

namespace App\PokerV2\Hand;

/**
  * StraightFlush
  * 
  * @package    Poker
  * @author     oangia <hqnhatdn@gmail.com>
  *
  */

class StraightFlush extends Hand
{
    public      $level              = 9;
    public      $instance           = 'StraightFlush';

    public function pointCalc()
    {
        $this->point = ($this->cards[4]->value == 13 && $this->cards[0]->value == 1) ? 10 : $this->cards[4]->value - 4;
        if ($this->chiAt) {
            switch ($this->point) {
                case 1:
                    $this->point = 9;
                case 10:
                    break;
                default:
                    --$this->point;
            }
        }
        // scale 100
        $this->point = round(($this->point/10) * 100, 4);
    }
}
