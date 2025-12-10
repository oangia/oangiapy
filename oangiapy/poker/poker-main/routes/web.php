<?php
use Illuminate\Route;
use App\Controllers\PokerController;

Route::get('/', function() {
    _view('welcome');
});
Route::get('/ai',                           [PokerController::class, 'index']);
Route::get('/visualize',                    [PokerController::class, 'visualize']);
