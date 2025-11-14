<?php

namespace App\PokerV2\Hand;

/**
  * Flush
  * 
  * @package    Poker
  * @author     oangia <hqnhatdn@gmail.com>
  *
  */

class Flush extends Hand
{
    public      $level              = 6;
    public      $instance           = 'Flush';
    private     $pointRatio         = 2;

    public function pointCalc()
    {
        $total = count($this->cards);
        for ($i = 0; $i < $total; ++$i) {
            if ($this->cards[$i]->value == 1) {
                $this->point += powPoint($this->cards[$i]);
                continue;
            }
            if (
                $i < $total - $this->pointRatio
                || (
                    $i == $total - $this->pointRatio
                    && $this->cards[0]->value == 1
                )
            ) {
                $this->zitchPoint += powPoint($this->cards[$i]);
            } else {
                $this->point += powPoint($this->cards[$i]);
            }
        }
        // scale 100
        $this->point = round(($this->point/3072) * 100, 4);
        $this->zitchPoint = round(($this->zitchPoint/832) * 100, 4);
    }
}
