<?php

namespace App\Poker\Hand;

/**
  * TwoPair
  * 
  * @package    Poker
  * @author     oangia <hqnhatdn@gmail.com>
  *
  */

class TwoPair extends Hand
{
    public      $level              = 3;
    public      $instance           = 'TwoPair';

    public function pointCalc()
    {
        // point
        $this->point = powPoint($this->cards[1]);
        $this->point += powPoint($this->cards[3]);
        // zitch point
        if ($this->cards[0]->value != $this->cards[1]->value) {
            $this->zitchPoint = $this->cards[0]->pointValue;
        }
        if (
            $this->cards[1]->value != $this->cards[2]->value && $this->cards[2]->value
            != $this->cards[3]->value
        ) {
            $this->zitchPoint = $this->cards[2]->pointValue;
        }
        if ($this->cards[3]->value != $this->cards[4]->value) {
            $this->zitchPoint = $this->cards[4]->pointValue;
        }
        // scale 100
        $this->point = round(($this->point/3072) * 100, 4);
        $this->zitchPoint = round(($this->zitchPoint/12) * 100, 4);
    }
}
