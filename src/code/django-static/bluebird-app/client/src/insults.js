"use strict";
var Insults = (function () {
    function Insults() {
    }
    Insults.random = function () {
        var a = Insults.adj1[Math.floor(Math.random() * Insults.adj1.length)];
        var b = Insults.adj2[Math.floor(Math.random() * Insults.adj2.length)];
        var c = Insults.nouns[Math.floor(Math.random() * Insults.nouns.length)];
        return a + " " + b + " " + c;
    };
    return Insults;
}());
Insults.adj1 = [
    "beslubbering", "bawdy", "cretinous", "dribbling", "foetid", "greasy",
    "grotesque", "hideous", "knavish", "lazy", "mewling", "puny", "pungent",
    "rank", "reekish", "slimy", "villainous", "weedy"
];
Insults.adj2 = [
    "boil-ridden", "clay-brained", "distempered", "dull-witted", "flap-mouthed",
    "gorbellied", "half-brained", "half-faced", "ill-bred", "lily-livered",
    "pig-faced", "purple-nosed", "shag-eared", "slack-jawed", "sour-faced",
    "swag-bellied", "whey-faced"
];
Insults.nouns = [
    "carbuncle", "canker-blossom", "clot", "codpiece", "dog", "dunce",
    "fat guts", "fool", "harpy", "harlot", "loon", "lout", "maggot",
    "malignancy", "measle", "miscreant", "mongrel", "mumbler", "old cow",
    "scut", "stinkhorn", "strumpet", "toad", "weasel"
];
exports.Insults = Insults;
