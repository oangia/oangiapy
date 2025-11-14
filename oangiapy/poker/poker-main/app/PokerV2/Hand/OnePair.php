<?php

namespace App\PokerV2\Hand;

/**
  * OnePair
  * 
  * @package    Poker
  * @author     oangia <hqnhatdn@gmail.com>
  *
  */

class OnePair extends Hand
{
    public      $level              = 2;
    public      $instance           = 'OnePair';

    public function pointCalc()
    {
        $total = count($this->cards);
        for ($i = 0; $i < $total; ++$i) {
            if ($i != 0 && $this->cards[$i]->value == $this->cards[$i - 1]->value) {
                continue;
            }
            if ($i != $total - 1 && $this->cards[$i]->value == $this->cards[$i + 1]->value) {
                $this->point += powPoint($this->cards[$i]);
                continue;
            }
            $this->zitchPoint += powPoint($this->cards[$i]);
        }
        // scale 100
        $this->point = round(($this->point/2048) * 100, 4);
        $this->zitchPoint = round(($this->zitchPoint/3584) * 100, 4);
    }
}
