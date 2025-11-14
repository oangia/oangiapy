<?php

function random($max, $done)
{
    $max = $max - count($done);
    $num = rand(0, $max);
    for ($i = 0; $i <= $num; ++$i) {
        if (in_array($i, $done) && $i <= $num) {
            ++$num;
        }
    }
    return $num;
}

function to_hop($arr, $k, $output = [])
{
    $arr = array_values($arr);
    if (empty($output)) {
        for ($i = 0; $i < count($arr); ++$i) {
            if ($i <= count($arr) - $k) {
                $output[] = [$arr[$i]];
            }
        }
    }
    if ($k == 1) {
        return $output;
    }
    $new_output = array();
    foreach ($output as $item) {
        for ($i = count($item); $i < count($arr) - $k + 2; ++$i) {
            $key = array_search($item[count($item) - 1], $arr);
            if ($i > $key) {
                $new_output[] = array_merge($item, [$arr[$i]]);
            }
        }
    }
    return toHop($arr, $k - 1, $new_output);
}

function chinh_hop($arr, $k, $output = [])
{
    if (empty($output)) {
        for ($i = 0; $i < count($arr); ++$i) {
            $output[] = [$arr[$i]];
        }
    }
    if ($k == 1) {
        return $output;
    }
    $new_output = array();
    foreach ($output as $item) {
        for ($i = 0; $i < count($arr); ++$i) {
            if (!in_array($arr[$i], $item)) {
                $new_output[] = array_merge($item, [$arr[$i]]);
            }
        }
    }
    return chinhHop($arr, $k - 1, $new_output);
}

function hoan_vi($arr)
{
    return chinhHop($arr, count($arr));
}

function power($base, $pow)
{
    if ($pow < 0) {
        return 0;
    }
    return pow($base, $pow);
}