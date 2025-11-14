<?php

function card_echo($card)
{
    echo '<img src="/icon/' . $card->name . '.bmp" />';
}

function powPoint($card)
{
    return power(2, $card->pointValue - 1);
}

function card_order($card1, $card2)
{
    if (
        $card1->value > $card2->value
        || (
            $card1->value == $card2->value
            && array_search($card1->pip, ['h', 'd', 'c', 's']) > array_search($card2->pip, ['h', 'd', 'c', 's'])
        )
    ) {
        return 1;
    }
    return -1;
}

function hand_order($hand1, $hand2)
{
    if ($hand1->compare($hand2, true) == 1) {
        return 1;
    }
    return -1;
}