<?php

namespace App\Poker;

use App\Poker\Hand;
use App\Poker\Card;
use App\Poker\Player;

class Poker
{
    public $chiAt = false;
    public $result = "";
    public $visualize = false;
    public $cards;
    public $aiType = "strongest";

    function __construct()
    {
    }

    public function setChiAt($chiAt) {
        $this->chiAt = $chiAt;
    }

    public function setAiType($aiType) {
        $this->aiType = $aiType;
    }

    public function generateCards($players) {
        $this->cards = explode("|", generateCards($players));
    }

    public function getCardsInput($cards) {
        $this->cards = explode("|", $cards);
    }

    public function detect() {
        $totalPlayers = count($this->cards);
        switch ($totalPlayers) {
            case 1:
                $this->result .= $this->getHands($this->cards[0], $this->aiType);
                break;
            case 2:
                $this->result .= $this->getHands($this->cards[0]) . "|" . $this->getHands($this->cards[1]);
                break;
            case 3:
                $player1 = new Player($this->cards[0], $this->chiAt);
                $player2 = new Player($this->cards[1], $this->chiAt);
                $player3 = new Player($this->cards[2], $this->chiAt);

                $names = get_opponent_deck([$player1, $player2, $player3]);
                $competitor = new Player($names, $this->chiAt);
                $competitor->getHandsesPoint();
                //$competitor->orderHandses();

                foreach ($competitor->handses as $comp) {
                    $player1->compare($comp, $competitor->totalHandsesPoint);
                    $player2->compare($comp, $competitor->totalHandsesPoint);
                    $player3->compare($comp, $competitor->totalHandsesPoint);
                }

                $player1->orderHandses(true);
                $player2->orderHandses(true);
                $player3->orderHandses(true);

                $hands = $player1->getStrongestHands();
                if ($this->visualize) {
                    echo $hands->visualize();
                }
                $this->result .= $hands->toString() . '|';
                $hands = $player2->getStrongestHands();
                if ($this->visualize) {
                    echo $hands->visualize();
                }
                $this->result .= $hands->toString() . '|';
                $hands = $player3->getStrongestHands();
                if ($this->visualize) {
                    echo $hands->visualize();
                }
                $this->result .= $hands->toString();
                break;
            default:
                $this->result .= "Bài không hợp lệ";
        }
    }

    public function resultToString() {
        return $this->result;
    }

    public function visualize() {
        $this->visualize = true;
    }

    private function getHands($cards, $aiType = "strongest") {
        $player = new Player($cards, $this->chiAt);
        $player->getHandsesPoint();
        $player->orderHandses();
        $hands = null;
        switch ($aiType) {
            case "strongest":
                $hands = $player->getStrongestHands();
                break;
            case "weakest":
                $hands = $player->getWeakestHands();
                break;
        }
        if ($this->visualize) {
            echo $hands->visualize();
        }
        return $hands->toString();
    }
}