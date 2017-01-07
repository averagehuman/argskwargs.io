var gulp = require("gulp");
var browserify = require("browserify");
var source = require('vinyl-source-stream');
var tsify = require("tsify");
var livereload = require('gulp-livereload');


var build = function(cfg) {
    return browserify({
        basedir: '.',
        debug: cfg.debug,
        entries: ['client/src/main.ts'],
        cache: {},
        packageCache: {}
    })
    .plugin(tsify)
    .bundle()
    .pipe(source('app.js'))
    .pipe(gulp.dest("client/dist"));
}


gulp.task("debug", function () {
    return build({debug: true})
});


gulp.task("build", function () {
    return build({debug: false})
});


gulp.task("watch", function () {
    livereload.listen(32700);
    gulp.watch(['client/src/**/*.ts'], ['debug']);
    gulp.watch(['client/dist/app.js']).on('change', livereload.changed)
});


gulp.task("default", ["debug"], function() {
    gulp.start('watch')
});
