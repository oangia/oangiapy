<?php
namespace App\Controllers;

use Illuminate\Http\Request;
use App\Poker\Poker;
use App\PokerV2\Poker as PokerV2;

class PokerController {
    public function index() {
        $chiAt = Request::get("chiat", false);
        $aiType = Request::get("aitype", "strongest");
        $cards = Request::get("cards");

        $game = new Poker;

        $game->setChiAt($chiAt);
        $game->setAiType($aiType);

        $game->getCardsInput($cards);

        $game->detect();

        echo $game->resultToString();
    }

	public function visualize() {
		$chiAt = Request::get("chiat", false);
        $aiType = Request::get("aitype", "strongest");
        $cards = Request::get("cards");
        $players = Request::get("players");

        $game = new Poker;
        $game->visualize();
        $game->setChiAt($chiAt);
        $game->setAiType($aiType);

        $game->generateCards($players);

        $game->detect();
	}

    public function visualizeV2() {
        $chiAt = Request::get("chiat", false);
        $aiType = Request::get("aitype", "strongest");
        $cards = Request::get("cards");
        $players = Request::get("players");

        $game = new PokerV2;
        $game->visualize();
        $game->setChiAt($chiAt);
        $game->setAiType($aiType);
        if ($cards) {
            $game->getCardsInput($cards);
        } else {
            $game->generateCards($players);
        }

        $game->detect();
    }

    public function generate() {
        $result = generateCards(3);
        gg($result);
        return $result;
    }
}