<?php
use Illuminate\Route;

use App\Controllers\PokerController;
use App\Controllers\ApiController;
use Illuminate\Database\Migration;

Route::get('/', function() {
    _view('welcome');
});
Route::get('/ai',                           [PokerController::class, 'index']);
Route::get('/visualize',                    [PokerController::class, 'visualize']);
Route::get('/v2/visualize',                 [PokerController::class, 'visualizeV2']);
Route::get('/generate',                     [PokerController::class, 'generate']);
Route::get('/api/v1/{player_id}/submit',    [ApiController::class, 'submitGame']);
Route::get('/api/v1/{player_id}/get',       [ApiController::class, 'getGame']);

Route::get('/install', function () {
    Migration::run("tables", [
        'id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY',
        'player_id VARCHAR(63) NOT NULL', 
        'cards VARCHAR(63) NOT NULL',
        'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
        'updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
        'INDEX idx_collection (player_id)'
    ]);
});