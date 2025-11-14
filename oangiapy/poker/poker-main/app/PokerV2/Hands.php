<?php

namespace App\PokerV2;

use App\PokerV2\Hand\Hand;

/**
  * Hands
  * 
  * @package    Poker
  * @author     oangia <hqnhatdn@gmail.com>
  *
  */

class Hands
{
    public      $middle             = null;
    public      $back               = null;
    public      $front              = null;
    public      $point              = 0;
    public      $bonus              = 0;
    public      $setting            = null;
    public      $thangSapHam        = 0;
    public      $thuaSapHam         = 0;
    public      $winRate            = 0;
    public      $naturals           = 0;
    public      $royalties          = 0;
    public      $fitPoint           = 0;

    function __construct(Hand $front, Hand $middle, Hand $back)
    {
        $this->front    = $front;
        $this->middle   = $middle;
        $this->back     = $back;
        $this->setting  = $back->instance . $middle->instance . $front->instance;
    }

    public function detectNaturals()
    {
        // straight
        if (
            $this->front->level == Hand::ZITCH
            && $this->front->isFlush
            && ($this->middle->level == Hand::FLUSH || $this->middle->level == Hand::STRAIGHTFLUSH)
            && ($this->back->level == Hand::FLUSH || $this->back->level == Hand::STRAIGHTFLUSH)
        ) {
            $this->naturals = true;
            return;
        }
        if (
            $this->front->level == Hand::ZITCH
            && $this->front->isStraight
            && ($this->middle->level == Hand::STRAIGHT || $this->middle->level == Hand::STRAIGHTFLUSH)
            && ($this->back->level == Hand::STRAIGHT || $this->back->level == Hand::STRAIGHTFLUSH)
        ) {
            $this->naturals = true;
            return;
        }
        if (
            $this->front->level == Hand::ONEPAIR
            && $this->middle->level == Hand::TWOPAIR
            && $this->back->level == Hand::TWOPAIR
            && (
                $this->front->zitchPoint == $this->middle->zitchPoint
                || $this->middle->zitchPoint == $this->back->zitchPoint
                || $this->back->zitchPoint == $this->front->zitchPoint
            )
        ) {
            $this->naturals = true;
        }
    }

    public function detectRoyalties()
    {
        if ($this->middle->level == Hand::FULLHOUSE) {
            $this->royalties += 4;
        }
        if ($this->front->level == Hand::THREEKIND) {
            $this->royalties += 6;
        }
        if ($this->back->level == Hand::FOURKIND) {
            $this->royalties += 8;
        }
        if ($this->back->level == Hand::STRAIGHTFLUSH) {
            $this->royalties += 10;
        }
        if ($this->middle->level == Hand::FOURKIND) {
            $this->royalties += 16;
        }
        if ($this->middle->level == Hand::STRAIGHTFLUSH) {
            $this->royalties += 20;
        }
    }

    public function compare(Hands $hands)
    {
        $front      = $this->front->compare($hands->front);
        $middle     = $this->middle->compare($hands->middle);
        $back       = $this->back->compare($hands->back);
        if (
            $front == 0
            && $middle == 0
            && $back == 0
        ) {
            return $this->front->compareZitchPoint($hands->front) == 1 ? 1 : -1;
        }
        if (
            $front <= 0
            && $middle <= 0
            && $back <= 0
        ) {
            return -1;
        }
        if (
            $front >= 0
            && $middle >= 0
            && $back >= 0
        ) {
            return 1;
        }

        return 0;
    }

    public function compare2(Hands $hands)
    {
        $front      = $this->front->compare($hands->front, true);
        $middle     = $this->middle->compare($hands->middle, true);
        $back       = $this->back->compare($hands->back, true);
        return [$front, $middle, $back];
    }

    public function toString()
    {
        $str = '';
        $str .= $this->front->toString() . ',';
        $str .= $this->middle->toString() . ',';
        $str .= $this->back->toString();

        return $str;
    }

    public function visualize() {
        $str = '';
        $str .= $this->front->visualize() . '<br />';
        $str .= $this->middle->visualize() . '<br />';
        $str .= $this->back->visualize() . '<br />';

        echo $str;
    }

    public function handsToArray($hands)
    {
        return [
            'front' => [
                $hands->front->cards[0]->name, $hands->front->cards[1]->name, $hands->front->cards[2]->name
            ],
            'middle' => [
                $hands->middle->cards[0]->name, $hands->middle->cards[1]->name, $hands->middle->cards[2]->name, $hands->middle->cards[3]->name, $hands->middle->cards[4]->name
            ],
            'back' => [
                $hands->back->cards[0]->name, $hands->back->cards[1]->name, $hands->back->cards[2]->name, $hands->back->cards[3]->name, $hands->back->cards[4]->name
            ]
        ];
    }

    public function pointCalc()
    {
        /*
        Z (b)           = 0
        Z (m)           = 100
        OP (b)          = 200
        OP (m; < k)     = 300
        Z (f; < k)      = 400
        TP (b)          = 500
        TK (b)          = 600
        OP (m; ak)      = 700
        S (b)           = 800
        TP (m)          = 900
        Z (f; ak)       = 1000
        TK (m)          = 1100
        F (b)           = 1200
        OP (f)          = 1300
        S (m)           = 1400
        F (m)           = 1500
        FH (b)          = 1600
        FH (m)          = 2500 1700 + 200 * 4
        TK (f)          = 3000 1800 + 200 * 6
        FK (b)          = 3500 1900 + 200 * 8
        SF (b)          = 4000 2000 + 200 * 10
        FK (m)          = 5300 2100 + 200 * 16
        SF (m)          = 6200 2200 + 200 * 20
        */
        $system = [
            'StraightFlush' => [
                'm' => 6200,
                'b' => 4000
            ],
            'FourKind' => [
                'm' => 5300,
                'b' => 3500
            ],
            'FullHouse' => [
                'm' => 2500,
                'b' => 1600
            ],
            'Flush' => [
                'm' => 1500,
                'b' => 1200
            ],
            'Straight' => [
                'm' => 1400,
                'b' => 800
            ],
            'ThreeKind' => [
                'f' => 3000,
                'm' => 1100,
                'b' => 600
            ],
            'TwoPair' => [
                'm' => 900,
                'b' => 500
            ],
            'OnePair' => [
                'f' => 1300,
                'm' => [
                    'ak' => 700,
                    'qj' => 300
                ],
                'b' => 200
            ],
            'Zitch' => [
                'f' => [
                    'ak' => 1000,
                    'qj' => 400
                ],
                'm' => 100,
                'b' => 0
            ]
        ];
        switch ($this->front->level) {
            case 4:
                $this->point += $system['ThreeKind']['f'] + $this->front->point;
                break;
            case 2:
                $this->point += $system['OnePair']['f'] + $this->front->point;
                break;
            case 1:
                if ($this->front->point >= 50) {
                    $this->point += $system['Zitch']['f']['ak'] + $this->front->point;
                } else {
                    $this->point += $system['Zitch']['f']['qj'] + $this->front->point;
                }
                break;
        }
        switch ($this->middle->level) {
            case 1:
                $this->point += $system['Zitch']['m'] + $this->middle->point;
                break;
            case 2:
                if ($this->front->point >= 50) {
                    $this->point += $system['OnePair']['m']['ak'] + $this->middle->point;
                } else {
                    $this->point += $system['OnePair']['m']['qj'] + $this->middle->point;
                }
                break;
            case 3:
                $this->point += $system['TwoPair']['m'] + $this->middle->point;
                $this->bonus += $this->middle->point;
                break;
            case 4:
                $this->point += $system['ThreeKind']['m'] + $this->middle->point;
                break;
            case 5:
                $this->point += $system['Straight']['m'] + $this->middle->point;
                break;
            case 6:
                $this->point += $system['Flush']['m'] + $this->middle->point;
                break;
            case 7:
                $this->point += $system['FullHouse']['m'] + $this->middle->point;
                $this->bonus += $this->middle->point;
                break;
            case 8:
                $this->point += $system['FourKind']['m'] + $this->middle->point ;
                $this->bonus += $this->middle->point;
                break;
            case 9:
                $this->point += $system['StraightFlush']['m'] + $this->middle->point;
                $this->bonus += $this->middle->point;
                break;
        }
        switch ($this->back->level) {
            case 1:
                $this->point += $system['Zitch']['b'] + $this->back->point;
                break;
            case 2:
                $this->point += $system['OnePair']['b'] + $this->back->point;
                break;
            case 3:
                $this->point += $system['TwoPair']['b'] + $this->back->point;
                break;
            case 4:
                $this->point += $system['ThreeKind']['b'] + $this->back->point;
                break;
            case 5:
                $this->point += $system['Straight']['b'] + $this->back->point;
                break;
            case 6:
                $this->point += $system['Flush']['b'] + $this->back->point;
                break;
            case 7:
                $this->point += $system['FullHouse']['b'] + $this->back->point;
                $this->bonus += $this->back->point * 2;
                break;
            case 8:
                $this->point += $system['FourKind']['b'] + $this->back->point;
                $this->bonus += $this->back->point * 2;
                break;
            case 9:
                $this->point += $system['StraightFlush']['b'] + $this->back->point;
                $this->bonus += $this->back->point * 2;
                break;
        }
        $this->point = round($this->point, 2);
        $this->bonus = round($this->bonus, 2);
    }
}
