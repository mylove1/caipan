var fs = require("fs");
 file = fs.open("main.js", 'a');
 file.write("123");
 file.close();
 setTimeout(function () {
     phantom.exit(0)
 }, 2000);
