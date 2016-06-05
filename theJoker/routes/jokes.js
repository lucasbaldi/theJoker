var express = require('express');
var router = express.Router();

// ****************************
// Script dependant CONSTANTS
// ****************************
var jokes = [
    'Did you hear about the guy whose whole left side was cut off? He\'s all right now.',
    "I'm reading a book about anti-gravity. It's impossible to put down.",
    "I wondered why the baseball was getting bigger. Then it hit me.",
    "It's not that the man did not know how to juggle, he just didn't have the balls to do it.",
    "I'm glad I know sign language, it's pretty handy.",
    "My friend's bakery burned down last night. Now his business is toast.",
    "Why did the cookie cry? It was feeling crumby.",
    "I used to be a banker, but I lost interest.",
    "A drum and a symbol fall off a cliff",
    "Why do seagulls fly over the sea? Because they aren't bay-gulls!",
    "Why did the fireman wear red, white, and blue suspenders? To hold his pants up.",
    "Why didn't the crab share his food? Because crabs are territorial animals, that don't share anything.",
    "Why was the javascript developer sad? Because he didn't Node how to Express himself.",
    "What do I look like? A JOKE MACHINE!?",
    "How did the hipster burn the roof of his mouth? He ate the pizza before it was cool.",
    "Why is it hard to make puns for kleptomaniacs? They are always taking things literally.",
    "Why do mermaid wear sea-shells? Because b-shells are too small.",
    "I'm a humorless, cold hearted, machine.",
    "Two fish in a tank. One looks to the other and says 'Can you even drive this thing???'",
    "Two fish swim down a river, and hit a wall. One says: 'Dam!'",
    "What's funnier than a monkey dancing with an elephant? Two monkeys dancing with an elephant.",
    "How did Darth Vader know what Luke was getting for Christmas? He felt his presents.",
    "What's red and bad for your teeth? A Brick.",
    "What's orange and sounds like a parrot? A Carrot.",
    "What do you call a cow with no legs? Ground beef",
    "Two guys walk into a bar. You'd think the second one would have noticed.",
    "What is a centipedes's favorite Beatle song?  I want to hold your hand, hand, hand, hand...",
    "What do you call a chicken crossing the road? Poultry in moton. ",
    "Did you hear about the Mexican train killer?  He had locomotives",
    "What do you call a fake noodle?  An impasta",
    "How many tickles does it take to tickle an octupus? Ten-tickles!",
    "At the rate law schools are turning them out, by 2050 there will be more lawyers than humans."
];

function getJoke(list) {
    var index = getRandomNum(1, list.length);
    return(list[index])
    /*
    var question = list[index].split("? ")[0];
    var answer = list[index].split("? ")[1];
    console.log("This is the joke: " + question);
    console.log("This is an answer: " + answer);
    */
}

function getRandomNum(min, max) {
    // Produces a random number between min and max
    return (Math.round(min - 0.5 + (Math.random() * max)) - 1);
}

router.get('/', function(req, res, next) {
  res.send(getJoke(jokes))
});

router.get('/:words', function(req, res, next) {
  res.send(getJoke(jokes))
});
module.exports = router;
