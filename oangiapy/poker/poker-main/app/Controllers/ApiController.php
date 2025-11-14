<?php
namespace App\Controllers;

use Illuminate\Http\Request;
use Illuminate\Database\MySQL\DB;

class ApiController {
	public function submitGame($player_id) {
		$cards = Request::get('cards');
        $result = DB::create('tables', ['player_id' => $player_id, 'cards' => $cards]);
        if (isset($result['last_id']) && is_numeric($result['last_id'])) {
            $result = DB::find('tables', $result['last_id']);
        }
        return $result;
	}

    public function getGame($player_id) {
        $cards = Request::get('cards');
        $playerCards = explode(',', $cards);
        $period = Request::get('period');
        $players = DB::query('select * from tables where created_at > NOW() - ' . $period . ' AND player_id <> \'' . $player_id . '\' ORDER BY id DESC');
  
        $potential = [];
        foreach ($players as $player) {
            $arr = array_intersect($playerCards, explode(',', $player['cards']));
            if (count($arr) == 0) {
                if (! isset($potential[$player['player_id']])) {
                    $potential[$player['player_id']] = explode(',', $player['cards']);
                }
            }
        }
        if (count($potential) < 2) {
            return ['players' => []];
        }
        $result = [];
        foreach ($potential as $player => $cards) {
            $result[] = ['player' => $player, 'cards' => implode(',', $cards)];
        }
        return ['players' => $result];
    }
}