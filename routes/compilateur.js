var exec = require('child_process').exec;
var spawn = require("child_process").spawn;
module.exports = function(app,client_redis,__dirname){
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
}
