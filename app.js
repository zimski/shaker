var express = require('express')
, http = require('http')
, crypto = require('crypto')
, path = require('path')
, mime = require('mime')
, fs = require('fs')
, sys = require('sys')
, redis = require('redis')
, io = require('socket.io');
var exec = require('child_process').exec;
var spawn = require("child_process").spawn;
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

    res.render('index',{});
});
app.get('/home',function(req,res){
    if(!req.session.authentificated)
    res.redirect('/');
res.render('home',{});
});
app.get('/dashboard', function(req,res){
    client_redis.LRANGE('hosts',0,-1,function(err,data_l){
        console.log(data_l);
        var list_machine=[];
        if(data_l.length==0)
        res.render('dashboard',{'data':list_machine});
        else
        data_l.forEach(function(item){
            client_redis.hgetall(item,function(err,data)
                {
                    data['hostname']=item;
                    list_machine.push(data);
                    console.log(data);
                    //console.log("list "+list_machine.length+" vs data "+length(data));
                    if(list_machine.length == data_l.length)
                res.render('dashboard',{'data':list_machine});
                }); 
        });
    console.log(list_machine);

    });

});


app.get('/show_script', function(req,res){
    if(!req.session.authentificated)
    res.redirect('/');

client_redis.LRANGE('shell_list',0,-1,function(err,data_l){
    console.log(data_l);
    res.render('show_script',{'data':data_l});
    console.log(data_l); 
});


});




app.get('/add_vm', function(req,res){

    res.render('add_vm',{});
});
app.post('/delete_vm', function(req,res){
    client_redis.lrem('hosts',1,req.body.host);
    client_redis.del(req.body.host);
    res.send("ok");
});
app.post('/add_vm', function(req,res){
    client_redis.HMSET(req.body.hostname,
        'ip',req.body.ip,
        'mac', req.body.mac,
        'domain',req.body.domain,
        'gateway',req.body.gateway,
        'dns',req.body.dns,
        'roles',req.body.roles,
        'pass',req.body.pass,

        function(err){
            if(err)    
        console.log('erreur'+err);
        });
    client_redis.lrem('hosts',1,req.body.hostname);
    client_redis.rpush('hosts',req.body.hostname,function(err){
        if(err) 
        console.log('erreur'+err);
    });
    res.redirect('/dashboard');
});
//*****************************************************
app.get('/add_script', function(req,res){
    if(!req.session.authentificated)
    res.redirect('/');

res.render('add_script',{name:'', var_env:'',script_bash:'' });
});

app.get('/edit_script/:nameS', function(req,res){
    if(!req.session.authentificated)
    res.redirect('/');

var path_sc = __dirname+"/scripts/"+req.params.nameS ;
var i =0;
var script_content_data ,env_content_data;
client_redis.hgetall('shell:'+req.params.nameS,function(err,data)
    {
        fs.readFile(path_sc+'/shell.sh', 'utf8', function (err,script_content) {
            if (err) {
                console.log(err);
            }
            else
        {
            script_content_data = script_content
            i=i+1;
        if(i==2)
            res.render('add_script',{name:req.params.nameS, var_env:env_content_data,script_bash:script_content_data });
        }
        });
        fs.readFile(path_sc+'/env.yaml', 'utf8', function (err,env_content) {
            if (err) {
                console.log(err);
            }
            else
        {
            env_content_data= env_content
            i=i+1;
        console.log('file sc '+i)
            if(i==2)
            res.render('add_script',{name:req.params.nameS, var_env:env_content_data,script_bash:script_content_data });
        }
        });

    });


});

app.post('/add_script', function(req,res){
    if(!req.session.authentificated)
    res.redirect('/');

var path_sc = __dirname+"/scripts/"+req.body.name_script ;
fs.mkdir(path_sc,function(e){
    if(!e || (e && e.code === 'EEXIST')){
        //do something with contents
        fs.writeFile(path_sc+'/env.yaml',req.body.var_env);
        fs.writeFile(path_sc+'/shell.sh',req.body.script_bash);
        client_redis.lrem('shell_list',1,req.body.name_script);
        client_redis.rpush('shell_list',req.body.name_script,function(err){
            if(err) 
            console.log('erreur'+err);
        });
    } else {
        //debug
        console.log(e);
    }
});
res.redirect('/edit_script/'+req.body.name_script);
});
//************************************************************
//******************************** MODULE CONF FILE **********
//************************************************************
app.get('/add_conf_file', function(req,res){
    if(!req.session.authentificated)
    res.redirect('/');

client_redis.LRANGE('shell_list',0,-1,function(err,data_l){
    console.log(data_l);
    res.render('module_conf_file_add',{conf_name: '',conf_content:'',list_env: data_l });
});

});


app.post('/add_conf_file', function(req,res){
    if(!req.session.authentificated)
    res.redirect('/');

var path_sc = __dirname+"/config_files/" ;
fs.writeFile(path_sc+req.body.conf_name,req.body.conf_content);

client_redis.lrem('conf_list',1,req.body.conf_name);
client_redis.rpush('conf_list',req.body.conf_name,function(err){
    if(err) 
    console.log('erreur'+err);
    else
    res.redirect('/show_config_file')
});
});

app.get('/edit_conf_file/:nameS', function(req,res){
    if(!req.session.authentificated)
    res.redirect('/');

var path_sc = __dirname+"/config_files/"+req.params.nameS;
fs.readFile(path_sc, 'utf8', function (err,content) {
    if (err)
    console.log(err);
    else
    client_redis.LRANGE('shell_list',0,-1,function(err,data_l){
        console.log(data_l);
        res.render('module_conf_file_add',{conf_name: req.params.nameS,conf_content:content,list_env: data_l });
    });

});
});

app.get('/show_config_file', function(req,res){
    if(!req.session.authentificated)
    res.redirect('/');

client_redis.LRANGE('conf_list',0,-1,function(err,data_l){
    console.log(data_l);
    res.render('module_conf_file_show',{'data':data_l});
    console.log(data_l); 
});
});


app.post('/module-cof-file-get-var/:nameS', function(req,res){
    if(!req.session.authentificated)
    res.redirect('/');

var path_sc = __dirname+"/scripts/"+req.params.nameS ;
fs.readFile(path_sc+'/env.yaml', 'utf8', function (err,env_content) {
    if (err)
{
    console.log(err);
    res.send('');
}
else
res.send(env_content);
});
});

//************************************************************
//************************************************************
//************************************************************


//************************************************************
//          CHECK / RUN Shaker
//************************************************************

app.post('/check_shaker/:sc',function(req,res){
    var path_sc =__dirname+"/scripts/"+req.params.sc+"/";
    var cmd = "python "+__dirname+"/py-sc/shaker.py -d -e "+path_sc+"env.yaml -s "+path_sc+"shell.sh --argv=\""+req.body.argv+"\"";
    child = exec(cmd, function (error, stdout, stderr) {
        var out = stdout.replace(/ /g,"&nbsp;");
        var err = stderr.replace(/ /g,"&nbsp;")
        res.send('<span class="console-cmd">[#] Start checking .. </span><br>'+out+err);
    });  
});

app.post('/run_shaker/:sc',function(req,res){

    var path_sc =__dirname+"/scripts/"+req.params.sc+"/";
    var cmd = __dirname+"/py-sc/shaker.py -x -w -e "+path_sc+"env.yaml -s "+path_sc+"shell.sh --argv="+req.body.argv;
    //console.log(cmd.split(' '));  
    var child = spawn("python",cmd.split(' '));
    child.stdout.on("data", function (data) {
        console.log("spawnSTDOUT:"+ data)
    });

    child.stderr.on("data", function (data) {
        console.log("spawnSTDERR:"+ data)
    });
    child.on("close",function(code){
        res.send("exit code: "+code);
    }); 
});
function run_shaker(script,argv)
{
    var path_sc =__dirname+"/scripts/"+script+"/";
    var cmd = __dirname+"/py-sc/shaker.py -x -w -e "+path_sc+"env.yaml -s "+path_sc+"shell.sh --argv="+argv;
    //console.log(cmd.split(' '));  
    var child = spawn("python",cmd.split(' '));
    child.stdout.on("data", function (data) {
        console.log("spawnSTDOUT:"+ data)
    });

    child.stderr.on("data", function (data) {
        console.log("spawnSTDERR:"+ data)
    });
    child.on("close",function(code){
        console.log("exit code: "+code);
    }); 
}
//************************************************************

//************************************************************
//*******             CMS                                 ****
//************************************************************

app.get("/cms",function(req,res){
    if(!req.session.authentificated)
    res.redirect('/');

var f=[];
f[0]='';
f[1]='';
f[2]='';
f[3]='';
f[4]='';
var d=[];
d.push(f);
res.render('cms',{name: '',forms : d, buttons :d});
});
app.get("/cms/edit_module/:module",function(req,res){
    if(!req.session.authentificated)
    res.redirect('/');

var module_name = req.params.module;
var forms=[];
var button=[];
var i = 0;
client_redis.hgetall('M:'+module_name+':Forms',function(err,data){
    for(var j in data){
        forms.push(data[j].split(':'));
    }
    console.log(data);
    i=i+1;
    if(i==2){
        console.log(forms);
        console.log(button);
        res.render('cms',{name: module_name,forms : forms, buttons : button});
    }

});
client_redis.hgetall('M:'+module_name+':Button',function(err,data){
    for(var j in data){
        button.push(data[j].split(':'));
    }
    console.log(data);
    i=i+1;
    if(i==2){
        console.log(forms);
        console.log(button);
        res.render('cms',{name: module_name,forms : forms, buttons : button});
    }

});
});

function CMS_create_redis_file(name_module,cmd){
    var path_sc = __dirname+"/views/"+name_module+"/install.sh" ;
    fs.appendFile(path_sc,'redis-cli '+cmd+'\n');

}
app.post("/cms/add_module",function(req,res){
    if(!req.session.authentificated)
    res.redirect('/');

var name_module = req.body.name_module;
// create folder for the module
fs.unlink(__dirname+"/views/"+name_module+"/install.sh");
var path_sc = __dirname+"/views/"+req.body.name_module ;
fs.mkdir(path_sc,function(e){
    if(!e || (e && e.code === 'EEXIST')){
        //do something with contents
        console.log("folder created");
    } else {
        //debug
        console.log(e);
    }
});

// add form
console.log("post cms ");
var names = req.body.name_field;
var keys = req.body.key_field;
var index = req.body.index;
var show = req.body.show;

client_redis.del('M:'+name_module+':Forms');
client_redis.del('M:'+name_module+':Button');
for(i=0;i< names.length;i++){
    var hash =index[i]+':'+show[i]+':'+names[i]+':'+keys[i];
    CMS_create_redis_file(name_module,'HSET M:'+name_module+':Forms '+i+' "'+hash+'"');
    client_redis.hset('M:'+name_module+':Forms',i,hash,function (err){
        if(err)
        console.log(err);
    });

}
// add button 
var button_color = req.body.button_color;
var button_name = req.body.button_name;
var button_script = req.body.button_script;
var button_argv = req.body.button_argv;
for(i=0;i<button_color.length;i++){
    var hash = button_color[i]+':'+button_name[i]+':'+button_script[i]+':'+button_argv[i].replace('$',''); 
    CMS_create_redis_file(name_module,'HSET M:'+name_module+':Button '+i+' "'+hash+'"');
    client_redis.hset('M:'+name_module+':Button',i,hash,function (err){
        if(err)
        console.log(err);
    });
}
// Shaker add module in list
client_redis.lrem("Shaker:module:list",1,name_module);
CMS_create_redis_file(name_module,'RPUSH Shaker:module:list '+name_module);

client_redis.rpush("Shaker:module:list",name_module,function(err){
    if(err)
    console.log(err);
    else
{
    run_shaker("generate_shaker_layout_for_modules","");
    run_shaker("generate_module_view_and_form",name_module);
    res.redirect('/cms/edit_module/'+name_module);
}
});
});
app.get("/module/:name/:method",function(req,res){
    if(!req.session.authentificated)
    res.redirect('/');

if(req.params.method == "form")
    res.render(req.params.name+"/form")
else
{
    client_redis.LRANGE('DB:'+req.params.name+':list',0,-1,function(err,data_l){
        console.log(data_l);
        var list_machine=[];
        if(data_l.length==0)
        res.render(req.params.name+'/view',{'data':list_machine});
        else
        data_l.forEach(function(item){
            client_redis.hgetall(item,function(err,data)
                {
                    data['key']=item;
                    list_machine.push(data);
                    console.log(data);
                    //console.log("list "+list_machine.length+" vs data "+length(data));
                    if(list_machine.length == data_l.length)
                res.render(req.params.name+'/view',{'data':list_machine});
                }); 
        });
    });
}

});
app.post("/module/:mod/post",function(req,res){
    if(!req.session.authentificated)
    res.redirect('/');

var module_name = req.params.mod;
var forms=[];
var index;
var i = 0;
client_redis.hgetall('M:'+module_name+':Forms',function(err,data){
    for(var j in data){
        var tmp = data[j].split(':');
        if(tmp[0]=='yes')
    index = j;
forms.push(tmp);
    }
    for(var j in forms){
        client_redis.HSET('DB:'+module_name+':'+req.body[forms[index][3]],forms[j][3],req.body[forms[j][3]],function(err){
            if(err)
            console.log(err);
        });
    }
    client_redis.lrem('DB:'+module_name+':list',1,'DB:'+module_name+':'+req.body[forms[index][3]]);
    client_redis.rpush('DB:'+module_name+':list','DB:'+module_name+':'+req.body[forms[index][3]],function(err){
        if(err) 
        console.log('erreur'+err);

    res.redirect('/module/'+module_name+'/view');});

});
});
app.post("/module/:mod/del",function(req,res){
    if(!req.session.authentificated)
    res.redirect('/');

var name = req.params.mod;
var key = req.body.key;
client_redis.lrem('DB:'+name+':list',1,'DB:'+name+':'+key);
client_redis.del('DB:'+name+':'+key);
res.send("ok");

});

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


