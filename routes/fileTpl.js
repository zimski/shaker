var fs = require('fs');
module.exports = function(app,client_redis,__dirname){
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

}
