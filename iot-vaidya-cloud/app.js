var express = require('express');
var bodyParser = require('body-parser');
var fs = require('fs');
var request = require('request');
var multer = require('multer');
var mongoose = require('mongoose');
var path = require("path");
var twilio = require('twilio');

var app = express();
var port = (process.env.VCAP_APP_PORT || 3000);
var host = (process.env.VCAP_APP_HOST || 'localhost');

app.use(express.static(path.join(__dirname,'public')));

app.use(bodyParser());
var twilioSid = "SID";
var twilioToken = "Token";

dbURI = 'mongodb://<username>:<password>@ds029804.mongolab.com:29804/dbname'
var db = mongoose.connection;
db.on('disconnected', function() {
    console.log('disconnected');
    console.log('dbURI is: '+dbURI);
    mongoose.connect(dbURI,
      {server: {auto_reconnect:true,
      socketOptions: { keepAlive: 1, connectTimeoutMS: 30000 }},
      replset: { socketOptions: { keepAlive: 1, connectTimeoutMS : 30000 } }});
});
console.log('dbURI is: '+dbURI);
mongoose.connect(dbURI, {server:{auto_reconnect:true}});

var pSchema = mongoose.Schema({
  name : String,
  age : Number,
  contact : Number,
  location : String,
  temperature : Number,
  pulse: Number,
  bp : Array,
  ecg : Array,
  gsr : Array
});
var dSchema = mongoose.Schema({
  name : String,
  email : String,
  pass: String
});
var patient = mongoose.model('patient', pSchema, "patient");
var doc = mongoose.model('doc', dSchema, "doc");    //(new_name_of_schema,schema_object,collection_name)

//var layout = {fileopt : "overwrite", filename : "simple-node-example"};
//mqtt code
var Client = require("ibmiotf").IotfApplication;

var config = {
    "org" : "org",
    "id" : "app-name",
    "auth-key" : "key",
    "auth-token" : "token"
}
var appClient = new Client(config);

appClient.connect();

appClient.on("connect", function () {

    appClient.subscribeToDeviceEvents("registered-device-name");

});
appClient.on("deviceEvent", function (deviceType, deviceId, eventType, format, payload) {
    console.log("Device Event from : "+deviceType+" : "+deviceId+" of event "+eventType+" with payload : "+payload);

    var par = JSON.parse(payload);

      var pay = new patient({
      name : par.name,
      age : par.age,
      contact : par.contact,
      location : par.location,
      temperature : par.temperature,
      pulse: par.pulse,
      bp : par.bp,
      ecg : par.ecg,
      gsr : par.gsr
})

    pay.save(function(err){
    if ( err ) throw err;
    console.log("Patient's data Saved Successfully in DB");
  });

});
//mqtt end


app.get('/',function(req,res){
  res.sendFile(path.join(__dirname, 'public/pages/examples/login.html'));
});

app.post('/imagepro',function(req,res){

  var name = req.body.name;
  var profile = req.body.photo1;

  console.log(req.body);

      // function to create file from base64 encoded string
function base64_decode(base64str, file) {
    // create buffer object from base64 encoded string, it is important to tell the constructor that the string is base64 encoded
    var bitmap = new Buffer(base64str, 'base64');
    // write buffer to file
    fs.writeFileSync(file, bitmap);
    console.log('File created from base64 encoded string!');
}
    // convert base64 string to image
    base64_decode(profile, path.join(__dirname, 'public/dist/img/patient/profile/'+name+'.jpg'));
    //res.status(200).send("OK");

  res.status(200);
});

app.post('/imagesyma',function(req,res){
  //var xyz = JSON.parse(req.body);
  //var js = JSON.stringify(req.body);

  //console.log(req.body);


  var name = req.body.name;
  var sym1 = req.body.photo2;

  console.log(req.body);

      // function to create file from base64 encoded string
function base64_decode(base64str, file) {
    // create buffer object from base64 encoded string, it is important to tell the constructor that the string is base64 encoded
    var bitmap = new Buffer(base64str, 'base64');
    // write buffer to file
    fs.writeFileSync(file, bitmap);
    console.log('File created from base64 encoded string!');
}

    base64_decode(sym1, path.join(__dirname, 'public/dist/img/patient/symptom/'+name+'1.jpg'));

    //res.status(200).send("OK");

  res.status(200);
});

app.post('/imagesymb',function(req,res){
  //var xyz = JSON.parse(req.body);
  //var js = JSON.stringify(req.body);

  //console.log(req.body);


  var name = req.body.name;
  var sym2 = req.body.photo3;

  console.log(req.body);

      // function to create file from base64 encoded string
function base64_decode(base64str, file) {
    // create buffer object from base64 encoded string, it is important to tell the constructor that the string is base64 encoded
    var bitmap = new Buffer(base64str, 'base64');
    // write buffer to file
    fs.writeFileSync(file, bitmap);
    console.log('File created from base64 encoded string!');
}
    base64_decode(sym2, path.join(__dirname, 'public/dist/img/patient/symptom/'+name+'2.jpg'));
    //res.status(200).send("OK");

  res.status(200);
});

//for doctor
var storage =   multer.diskStorage({
  destination: function (req, file, callback) {
    callback(null, './public/dist/img/doc/');
  },
  filename: function (req, file, callback) {
    callback(null, req.body.name + '.jpg');
  }
});
var upload = multer({ storage : storage}).single('imgupload');
//doctor

app.post('/register',function(req,res){
  //res.sendFile(path.join(__dirname, 'public/report.html'));

  upload(req,res,function(err) {
        if(err) {
            return res.end("Error uploading file.");  //on the server
        }
        var n = req.body.name;
        var e = req.body.email;
        var p = req.body.password;
        //console.log(e);
        var d = new doc({
        name : n,
        email : e,
        pass : p
        });
        d.save(function(err){
          if ( err ) throw err;
          console.log("Doc Saved Successfully" + '\n' + d); //to the database
          //res.sendFile(path.join(__dirname, 'public/pages/examples/login.html'));
          res.redirect("/");
        });
      });//upload
});//register

app.post('/login',function(req,res){
  //res.sendFile(path.join(__dirname, 'public/check.html'));
  var i = 0;
  var n;
  var e = req.body.email;
  var p = req.body.password;
  var url = 'https://api.mongolab.com/api/1/databases/mydb/collections/doc?apiKey=KEY';
  request(url, function(err, resp, body) {
   body = JSON.parse(body);
   //res.sendFile(path.join(__dirname, 'public/pages/tables/entry.html'));

   body.forEach(function(element,index){
     if((element.email == e)&&(element.pass == p)){
      n = element.name;
      i++;
    }
    });
   if(i>0){
    //res.sendFile(path.join(__dirname, 'public/pages/tables/entry.html'));
    res.redirect('/entry?'+n);
  }
    else
      //res.sendFile(path.join(__dirname, 'public/pages/examples/login.html'));
    res.redirect("/");

  });

});

app.get('/register',function(req,res){
  res.sendFile(path.join(__dirname, 'public/pages/examples/register.html'));
});
app.get('/login',function(req,res){
  res.sendFile(path.join(__dirname, 'public/pages/examples/login.html'));
  //res.redirect('/');
});
 app.get('/logout',function(req,res){
  res.redirect('/');

});
/*
app.get('/data',function(req,res){
  patient.find({},{ecg:1,_id:0},function(err,datashow){
	if(err)
		console.log(err);

	res.send(JSON.stringify({ 'datashow' : datashow }));
   });

});
*/
/*
app.get('/message', function (req, res) {
    var client = new twilio.RestClient(twilioSid, twilioToken);

    client.sendMessage({
        to:'+917507012952',
        from:'+12403770856',
        body:'IOT VAIDYA is there for you!'
    }, function(err, message) {
        res.send('Message sent! ID: '+message.sid);
    });
});
*/
app.post('/message', function (req, res) {
    var client = new twilio.RestClient(twilioSid, twilioToken);
    var msg = req.body.message;
    var number = req.body.contact_number;
    var t_url = 'http://api.mymemory.translated.net/get?q='+msg+'&langpair=en|hi'   //from mymemory.translated.net
    request(t_url, function(err, resp, url_body) {
      var t = JSON.parse(url_body);
      var msg_translated = t.responseData.translatedText;
      client.sendMessage({     //twilio
        to:number,
        from:'+12013800352',
        body:msg_translated
    }, function(err, message) {
        res.redirect("/");
    });

    //res.redirect("/");
});
});//post

app.get('/entry',function(req,res){
  res.sendFile(path.join(__dirname, 'public/pages/tables/entry.html'));
});
app.get('/report',function(req,res){
  res.sendFile(path.join(__dirname, 'public/report.html'));
});

app.get('/map',function(req,res){
  res.sendFile(path.join(__dirname, 'public/pages/map.html'));

});

app.listen(port, host,function(){
	console.log('Running on PORT : ' + port);
});
