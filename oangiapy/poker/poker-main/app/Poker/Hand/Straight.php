<?php

namespace App\Poker\Hand;

/**
  * Straight
  * 
  * @package    Poker
  * @author     oangia <hqnhatdn@gmail.com>
  *
  */

class Straight extends Hand
{
    public      $level              = 5;
    public      $instance           = 'Straight';

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
