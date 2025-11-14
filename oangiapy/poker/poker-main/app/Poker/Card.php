<?php

namespace App\Poker;

/**
  * Card
  * 
  * @package    Poker
  * @author     oangia <hqnhatdn@gmail.com>
  *
  */

class Card
{
    public $name        = null;
    public $value       = 0;
    public $pointValue  = 0;
    public $pip         = null;

    function __construct($name)
    {
        preg_match_all('!\d+!', $name, $this->value);
        $this->name         = $name;
        $this->value        = (int)$this->value[0][0];
        $this->pip          = str_replace($this->value, '', $name);
        $this->pointValue   = (($this->value == 1) ? 14 : $this->value) - 2;
    }

    public function compare(Card $card)
    {
        if ($this->value > $card->value) return 1;
        if ($this->value < $card->value) return -1;
        return 0;
    }

    public function visualize() {
        return "<img src=\"icon/" . $this->name . ".bmp\"/>";
    }
}
