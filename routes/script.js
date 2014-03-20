var fs = require('fs');
module.exports = function(app,client_redis,__dirname){ 
    app.get('/show_script', function(req,res){
        if(!req.session.authentificated)
        res.redirect('/');

    client_redis.LRANGE('shell_list',0,-1,function(err,data_l){
        console.log(data_l);
        res.render('show_script',{'data':data_l});
        console.log(data_l); 
    });


    });

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
}
