var page = require('webpage').create();
page.open('http://item.jd.com/1312640.html', function () {
    page.render('example.png');
    phantom.exit();
});
