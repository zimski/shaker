var crypto = require('crypto')
module.exports = function(app,client_redis,__dirname){
    app.get('/logout',function(req,res){
        req.session.authentificated = false;
        res.redirect('/');
    })
    app.post('/login',function(req,res){

        var md5 = crypto.createHash('md5');

        console.log("password "+req.body.password);
        if(req.body.user.length <3 && req.body.password.length <5){
            res.redirect('/');
            return 0;
        }
        client_redis.HGETALL('shaker:login',function(err,data){
            var pass = md5.update(req.body.password).digest('hex');
            console.log(pass);
            if(err){
                res.redirect('/');
                return 0
            }
            if(data && req.body.user == data['user'] && pass == data['pass']){
                req.session.authentificated= true;
                res.redirect('/home');
            }
            else
            res.redirect('/');
        });
    });
    app.get('/', function(req,res){
        if(req.session.authentificated)
        res.redirect('/home');

    res.render('index',{});
    });
    app.get('/home',function(req,res){
        if(!req.session.authentificated)
        res.redirect('/');
    res.render('home',{});
    });
}
