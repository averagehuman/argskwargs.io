var $        = require('gulp-load-plugins')();
var argv     = require('yargs').argv;
var gulp     = require('gulp');
var rimraf   = require('rimraf');
var sequence = require('run-sequence');
var exec = require('child_process').exec;

// Check for DEBUG environment flag which signals "not production"
var PRODUCTION = (process.env.DEBUG == '0');

// Port to use for the development server.
var PORT = 7070;

// Browsers to target when prefixing CSS.
var COMPATIBILITY = ['last 2 versions', 'ie >= 9'];

// File paths to various assets are defined here.
var PATHS = {
  assets: [
    'src/assets/{!img,!js,!scss}/**/*',
    '!src/assets/*~',
    '!src/assets/*.swp'
  ],
  sass: [
    'bower_components/foundation-sites/scss',
    'bower_components/motion-ui/src/',
    'src/assets/scss/components'
  ],
  javascript: [
    'bower_components/jquery/dist/jquery.js',
    'bower_components/what-input/what-input.js',
    'bower_components/foundation-sites/js/foundation.core.js',
    'bower_components/foundation-sites/js/foundation.util.*.js',
    // Paths to individual JS components defined below
    'bower_components/foundation-sites/js/foundation.offcanvas.js',
    'bower_components/foundation-sites/js/foundation.abide.js',
    'bower_components/foundation-sites/js/foundation.drilldown.js',
    'bower_components/foundation-sites/js/foundation.dropdown.js',
    'bower_components/foundation-sites/js/foundation.dropdownMenu.js',
    'bower_components/foundation-sites/js/foundation.equalizer.js',
    'bower_components/foundation-sites/js/foundation.responsiveMenu.js',
    'bower_components/foundation-sites/js/foundation.responsiveToggle.js',
    'bower_components/foundation-sites/js/foundation.reveal.js',
    'bower_components/foundation-sites/js/foundation.sticky.js',
    'bower_components/foundation-sites/js/foundation.tabs.js',
    'bower_components/foundation-sites/js/foundation.toggler.js',
    'bower_components/foundation-sites/js/foundation.tooltip.js',
    'src/assets/js/!(app).js',
    'src/assets/js/app.js'
  ]
};

gulp.task('environ', function (done) {
  console.log(process.env);
});

// Delete the "dist" folder
// This happens every time a build starts
gulp.task('clean', function(done) {
  rimraf('src/theme/static', done);
});

// Copy files out of the assets folder
// This task skips over the "img", "js", and "scss" folders, which are parsed separately
gulp.task('copy', function() {
  gulp.src(PATHS.assets)
    .pipe(gulp.dest('src/theme/static'));
});

// Compile Sass into CSS
// In production, the CSS is compressed
gulp.task('sass', function() {

  return gulp.src('src/assets/scss/app.scss')
    .pipe($.sourcemaps.init())
    .pipe($.sass({
      includePaths: PATHS.sass
    })
        .on('error', $.sass.logError))
    .pipe($.autoprefixer({
      browsers: COMPATIBILITY
    }))
    .pipe($.if(PRODUCTION, $.cssnano()))
    .pipe($.if(!PRODUCTION, $.sourcemaps.write()))
    .pipe(gulp.dest('src/theme/static/css'));
});

// Combine JavaScript into one file
// In production, the file is minified
gulp.task('javascript', function() {
  return gulp.src(PATHS.javascript)
    .pipe($.babel())
    .pipe($.concat('app.js'))
    .pipe($.if(PRODUCTION, $.uglify()
      .on('error', e => { console.log(e); })
    ))
    .pipe(gulp.dest('src/theme/static/js'));
});

// Copy images to the "dist" folder
// In production, the images are compressed
gulp.task('images', function() {
  var imagemin = $.if(PRODUCTION, $.imagemin({
    progressive: true
  }));

  return gulp.src('src/assets/img/**/*')
    .pipe(imagemin)
    .pipe(gulp.dest('src/theme/static/img'));
});

// build all assets
gulp.task('assets', ['sass', 'javascript', 'images', 'copy']);

gulp.task('pelican', function (cb) {
  var cmd = 'make pelican';
  if (PRODUCTION) {
    cmd += ' DEBUG=0';
  };
  exec(cmd, function (err, stdout, stderr) {
      console.log(stdout);
      console.log(stderr);
      cb(err);
  });
});

// Build the "dist" folder by running all of the above tasks
gulp.task('build', function(done) {
  sequence('clean', 'assets', 'pelican', done);
});

// Starts a test server, which you can view at http://localhost:8079
gulp.task('server', function() {
  gulp.src('dist')
    .pipe($.webserver({
      port: 8079,
      host: 'localhost',
      fallback: 'index.html',
      livereload: true,
      open: false
    }))
  ;
});

gulp.task('watch', function() {
  gulp.watch(PATHS.assets, ['copy']);
  gulp.watch(['src/assets/scss/**/*.scss'], ['sass']);
  gulp.watch(['src/assets/js/**/*.js'], ['javascript']);
  gulp.watch(['src/assets/img/**/*'], ['images']);
  // Watch Pelican source files
  gulp.watch([
    'site.properties',
    'src/articles/**/*',
    'src/pages/**/*',
    'src/theme/**/*',
    'src/config.py'], ['pelican']);
});

// Build the site, run the server, and watch for file changes
gulp.task('default', function(done) {
  sequence('clean', 'assets', 'pelican', 'server', 'watch', done);
});

