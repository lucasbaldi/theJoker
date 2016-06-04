var express = require('express');
var router = express.Router();
//var curl = require('curlrequest');
var request = require('request')
var password = "D5IKoXbX2m8R";
var username = "1d8bf850-2191-48db-b787-852eabbe7225";

var auth = 'Basic ' + new Buffer(username + ':' + password).toString('base64');


var headers = {
  Authorization : auth,
  'Content-Type': 'application/json'
};

/* GET home page. */
router.get('/', function(req, res, next) {



  var dataString = '{"text": "Hi Team, I know the times are difficult! Our sales have been disappointing for the past three quarters for our data analytics product suite. We have a competitive data analytics product suite in the industry. But we need to do our job selling it! "}';

  var options = {
      url: 'https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2016-05-19',
      headers: headers,
      body: dataString
  };

  function callback(error, response, body) {
      if(error){
        console.log(error)
      }else{
        res.send(response)
      }
  }

  request.post(options, callback);
});

router.get('/:text', function(req, res, next) {
  var text = req.params.text;
  var dataString = '{"text":\"'+ text+'\"}';

  var options = {
     url: 'https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2016-05-19',
     headers: headers,
     body: dataString
  };

  function callback(error, response, body) {
     if(error){
       console.log(error)
     }else{
       res.send(response)
     }
  }

  request.post(options, callback);
})



module.exports = router;
