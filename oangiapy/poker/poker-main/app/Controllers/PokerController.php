<?php
namespace App\Controllers;

use Illuminate\Http\Request;
use App\Poker\Poker;

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

    public function generate() {
        $result = generateCards(3);
        gg($result);
        return $result;
    }
}
