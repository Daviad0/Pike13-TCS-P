const express = require('express')
const app = express()
const bodyParser = require('body-parser');

const port = 1337;
var messages = [];

var authToken = "";
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(__dirname + '/public'));
app.get('/', (req, res) => {
  res.sendFile(__dirname + "/live.html")
})

app.get('/auth', (req, res) => {
  res.sendFile(__dirname + "/a.html")
})

app.get('/live', (req, res) => {
  res.sendFile(__dirname + "/live.html")
})

app.post("/token", (req, res) => {
  authToken = req.body.token;
  
  res.status(200).send({success: true});
})
app.post("/message", (req,res)=>{
  messages.push(req.body.message);
  res.status(200).send({success: true});
})
app.get("/message", (req,res)=> {
  if(messages.length > 0){
    res.status(200).send({m: true, message: messages.pop()});
  } 
  else{
    res.status(200).send({m: false});
  }
});

app.get("/token", (req, res) => {
  if(authToken != ""){
    res.status(200).send({token: authToken, success: true});
  }else{
    res.status(418).send({message: "I'm a teapot!", success:false});
  }
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})

