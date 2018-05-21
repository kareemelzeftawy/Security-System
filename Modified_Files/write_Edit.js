#!/usr/bin/env node

var ndef = require('ndef'),
    mifare = require('..'),
    message,
    bytes;

message = [
    ndef.textRecord("Allah Akbr"),
    ndef.textRecord("Elhamdullah"),
    ndef.textRecord("123456789")
];

bytes = ndef.encodeMessage(message);

mifare.write(bytes, function(err) {
    if (err) {
        console.log("Write failed ");
        console.log(err);
    } else {
        console.log("OK");
    }
});
