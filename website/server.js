const express = require('express');
var bodyParser = require("body-parser");
const spawn = require("child_process").spawn;
const app = express();
app.set('view engine', 'pug');
app.use(express.static(__dirname + '/public'))
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.get('/', (req, res) => {
    res.render('index',{
        title: 'Propaganda Detector'

    });
});
app.post('/result', function (req, res){
   var weblink = req.body.weblink;
   var prediction ='No URL';
   if (weblink == ''){
       res.render('results', {
           title: 'Propaganda Detector Results',
           weblink: weblink,
           prediction: prediction
       });
   }
   else {
       const pythonProcess = spawn('C:\\Users\\Kevin\\AppData\\Local\\Programs\\Python\\Python37\\python.exe', ["C:/Users/Kevin/Desktop/propaganda-website/webparser.py", weblink]);
       pythonProcess.stdout.on('data', (data) => {
           prediction = data.toString()
           if (prediction == '')
               prediction = 'None found!'
           res.render('results', {
               title: 'Propaganda Detector Results',
               weblink: weblink,
               prediction: prediction
           });
       });
   }
});

app.get('/result', function (req, res){
    res.redirect('/');
});

const server = app.listen(7000, () => {
    console.log(`Express running → PORT ${server.address().port}`);
});
