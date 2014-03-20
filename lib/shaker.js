var exec = require('child_process').exec;
var spawn = require("child_process").spawn;
exports.run_shaker =function (script,argv)
{
    var path_sc =__dirname+"/../scripts/"+script+"/";
    var cmd = __dirname+"/../py-sc/shaker.py -x -w -e "+path_sc+"env.yaml -s "+path_sc+"shell.sh --argv="+argv;
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
