var express = require('express')
, http = require('http')
, path = require('path')
, mime = require('mime')
, sys = require('sys')
, redis = require('redis')
, io = require('socket.io');
var sanitizer = require('sanitizer');
var app = express();var sanitizer = require('sanitizer');
var client_redis = redis.createClient();

app.configure(function(){
    app.set('port', process.env.PORT || 3002);
    app.set('views', __dirname + '/views');
    app.set('view engine', 'jade');
    app.use(express.multipart())
    app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.bodyParser());
app.use(express.cookieParser());
app.use(express.cookieSession({store: '/',
    secret: 'BBQ12345AHHH////',
    cookie: {httpOnly: false},
    key: 'cookie.sid' }));
app.use(express.static(path.join(__dirname, 'public')));
});
//
// add routes
//
require('./routes/fileTpl')(app,client_redis,__dirname)
require('./routes/cms')(app,client_redis,__dirname)
require('./routes/script')(app,client_redis,__dirname)
require('./routes/compilateur')(app,client_redis,__dirname)
require('./routes/loginHome')(app,client_redis,__dirname)

//---------------------------------------------------------------------
var op= http.createServer(app).listen(app.get('port'), function(){
    console.log("Express server listening on port " + app.get('port'));
});
//--------------------------------------------------------------------

//*************************************************************
//*                  socket IO                                *  
//*************************************************************
io = io.listen(op);
io.sockets.on('connection', function (socket) {
    //socket.emit('faitUneAlerte');
    console.log('client connecté');

    socket.on('console-emit', function (data) {
        var out = sanitizer.escape(data)

        socket.broadcast.emit('console-emit',out.replace(/ /g,"&nbsp;"));
    });
    socket.on('console-emit-cmd', function (data) {
        socket.broadcast.emit('console-emit',data);
    });

    socket.on('disconnect',function()
        {
            console.log("disconnect user from ");

        });
});


