<?php

$start_time = null;
$memory = null;

function debug()
{
    global $start_time;
    global $memory;
    if ($start_time && $memory) {
        echo '<p>time: '.(microtime(true) - $start_time)."</p>";
        echo '<p>memory: '.(memory_get_usage() - $memory)."</p>";
        exit;
    }
    $start_time = microtime(true);
    $memory = memory_get_usage();
}

function generateCards($players = 1) {
    $deck = [
        '1h', '1d', '1c', '1s',
        '2h', '2d', '2c', '2s',
        '3h', '3d', '3c', '3s',
        '4h', '4d', '4c', '4s',
        '5h', '5d', '5c', '5s',
        '6h', '6d', '6c', '6s',
        '7h', '7d', '7c', '7s',
        '8h', '8d', '8c', '8s',
        '9h', '9d', '9c', '9s',
        '10h', '10d', '10c', '10s',
        '11h', '11d', '11c', '11s',
        '12h', '12d', '12c', '12s',
        '13h', '13d', '13c', '13s'
    ];
    $done = [];
    $cardses = [];
    for ($p = 0; $p < $players; ++ $p) {
        $cards = [];
        for ($i = 0; $i < 13; ++$i) {
            $random = random(51, $done);
            $done[] = $random;
            $cards[] = $deck[$random];
        }
        $cardses[] = implode(',', $cards);
    }
    return implode('|', $cardses);;
}

function get_opponent_deck($players)
{
    $deck = [
        '1h', '1d', '1c', '1s',
        '2h', '2d', '2c', '2s',
        '3h', '3d', '3c', '3s',
        '4h', '4d', '4c', '4s',
        '5h', '5d', '5c', '5s',
        '6h', '6d', '6c', '6s',
        '7h', '7d', '7c', '7s',
        '8h', '8d', '8c', '8s',
        '9h', '9d', '9c', '9s',
        '10h', '10d', '10c', '10s',
        '11h', '11d', '11c', '11s',
        '12h', '12d', '12c', '12s',
        '13h', '13d', '13c', '13s'
    ];
    $competitor = [];
    foreach ($deck as $name) {
        $done = false;
        foreach ($players as $player) {
            foreach ($player->cards as $card) {
                if ($name == $card->name) {
                    $done = true;
                    break;
                }
            }
            if ($done) {
                break;
            }
        }
        if (! $done) {
            $competitor[] = $name;
        }
    }
    return implode(',', $competitor);
}