var fs = require('fs');
var shaker = require('../lib/shaker.js')
module.exports = function(app,client_redis,__dirname){
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
    res.render('cms',{name: '',forms : d, buttons :d,selects:d});
    });
    app.get("/cms/edit_module/:module",function(req,res){
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

    var module_name = req.params.module;
    var forms=[];
    var select=[];
    var button=[];
    var i = 0;
    client_redis.hgetall('M:'+module_name+':Forms',function(err,data){
        for(var j in data){
            forms.push(data[j].split(':'));
        }
        console.log(data);
        i=i+1;
        if(i==3){
            console.log(forms);
            console.log(button);
            res.render('cms',{name: module_name,forms : forms, buttons : button,selects : select});
        }

    });
    client_redis.hgetall('M:'+module_name+':Select',function(err,data){
        for(var j in data){
            select.push(data[j].split(':'));
        }
        select.push(f);
        console.log(data);
        i=i+1;
        if(i==3){
            console.log(forms);
            console.log(button);
            res.render('cms',{name: module_name,forms : forms, buttons : button,selects : select});
        }

    });

    client_redis.hgetall('M:'+module_name+':Button',function(err,data){
        for(var j in data){
            button.push(data[j].split(':'));
        }
        console.log(data);
        i=i+1;
        if(i==3){
            console.log(forms);
            console.log(button);
            res.render('cms',{name: module_name,forms : forms, buttons : button,selects : select});
        }

    });
    });

    function CMS_create_setup_file(name_module,cmd){
        var path_sc = __dirname+"/views/"+name_module+"/install.sh" ;
        fs.appendFile(path_sc,cmd+'\n');

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

    client_redis.del('M:'+name_module+':Button');
    client_redis.del('M:'+name_module+':Forms');
    client_redis.del('M:'+name_module+':Select');

    for(i=0;i< names.length;i++){
        var hash =index[i]+':'+show[i]+':'+names[i]+':'+keys[i];
        CMS_create_setup_file(name_module,'redis-cli HSET M:'+name_module+':Forms '+i+' "'+hash+'"');
        client_redis.hset('M:'+name_module+':Forms',i,hash,function (err){
            if(err)
            console.log(err);
        });

    }
    // add selects
    var select_names = req.body.select_name_field;
    var select_keys = req.body.select_key_field;
    var select_content = req.body.select_content_field;
    var select_show = req.body.select_show;

    for(i=0;i< select_names.length;i++){
        var hash =select_show[i]+':'+select_names[i]+':'+select_keys[i]+':'+select_content[i];
        CMS_create_setup_file(name_module,'redis-cli HSET M:'+name_module+':Select '+i+' "'+hash+'"');
        client_redis.hset('M:'+name_module+':Select',i,hash,function (err){
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
        CMS_create_setup_file(name_module,'redis-cli HSET M:'+name_module+':Button '+i+' "'+hash+'"');
        client_redis.hset('M:'+name_module+':Button',i,hash,function (err){
            if(err)
            console.log(err);
        });
    }
    // Shaker add module in list
    client_redis.lrem("Shaker:module:list",1,name_module);
    CMS_create_setup_file(name_module,'redis-cli RPUSH Shaker:module:list '+name_module);

    client_redis.rpush("Shaker:module:list",name_module,function(err){
        if(err)
        console.log(err);
        else
    {
        shaker.run_shaker("generate_shaker_layout_for_modules","");
        //CMS_create_setup_file(name_module,'python ../../')
        shaker.run_shaker("generate_module_view_and_form",name_module);
        res.redirect('/cms/edit_module/'+name_module);
    }
    });
    });
    app.get("/module/:name/edit/:key",function(req,res){
        var module_name = req.params.name;
        var key = req.params.key;

        client_redis.hgetall('DB:'+module_name+":"+key,function(err,data){
            if(err){
                console.log(err)
            res.render(module_name+'/view');
            }
            else{
                res.render(module_name+'/form',{data:data});
            }
        });

    });
    app.get("/module/:name/:method",function(req,res){
        if(!req.session.authentificated)
        res.redirect('/');

    if(req.params.method == "form")
        res.render(req.params.name+"/form",{data:{}})
    else
    {
        client_redis.LRANGE('DB:'+req.params.name+':list',0,-1,function(err,data_l){
            console.log(data_l);
            var list_machine=[];
            if(data_l.length==0)
            res.render(req.params.name+'/view',{'data':list_machine});
            else
            data_l.sort().forEach(function(item){
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
    var select =[];
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
        // store data from SelectBoxes
        client_redis.HGETALL('M:'+module_name+':Select',function(err,data){
            for(var j in data){
                var tmp = data[j].split(':');
                select.push(tmp);
            }
            for(var j in select){
                client_redis.HSET('DB:'+module_name+':'+req.body[forms[index][3]],select[j][2],req.body[select[j][2]],function(err){
                    if(err)
                    console.log(err);
                });
            }

        });
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


}
