'use strict';

import plugins        from 'gulp-load-plugins';
import yargs          from 'yargs';
import browser        from 'browser-sync';
import gulp           from 'gulp';
import log            from 'fancy-log';
import rimraf         from 'rimraf';
import child_process  from 'child_process';

// Load all Gulp plugins into one variable
const $ = plugins();

// Your project's server will run on localhost:xxxx at this port
const PORT = 8000;

// Autoprefixer will make sure your CSS works with these browsers
const COMPATIBILITY = [
  "last 2 versions",
  "ie >= 9",
  "ios >= 7"
];

const PWD = process.cwd();

// Gulp will reference these paths when it copies files
const PATHS = {
  sass: {
    // Path to source folder
    src: "assets/scss",
    // Path to dest folder
    dest: "src/theme/static/css",  
    // Paths to Sass libraries, which can then be loaded with @import
    includePaths: [
      "node_modules/foundation-sites/scss",
      "node_modules/motion-ui/src",
      "assets/scss/components"
    ]
  },
  javascript: [
    'node_modules/jquery/dist/jquery.js',
    'node_modules/what-input/dist/what-input.js',
    'node_modules/foundation-sites/js/foundation.core.js',
    'node_modules/foundation-sites/js/foundation.util.*.js',
    'node_modules/foundation-sites/js/foundation.reveal.js',
    'node_modules/foundation-sites/js/foundation.toggler.js',
    'node_modules/foundation-sites/js/foundation.tooltip.js',
    'assets/js/!(app).js',
    'assets/js/app.js'
  ],
  extras: [
      './favicon.ico'
  ],
  pelican: {
    src: "src",
    dest: "build",
  }
};



const PELICAN_BUILD_CMD = [
  'pelican',
  PATHS.pelican.src,
  '-o',
  PATHS.pelican.dest,
  '-s',
  `${PATHS.pelican.src}/config.py`,
  '-D'
];

// UnCSS will use these settings
const UNCSS_OPTIONS = {
    html: [
        PATHS.pelican.dest + '/**/*.html'
    ]
};

// Check for --production flag
const PRODUCTION = !!(yargs.argv.production);

// Delete the "build" folder
// This happens every time a build starts
function clean(done) {
  rimraf(PATHS.pelican.dest, done);
}

// Copy files out of the assets folder
function copy() {
  return gulp.src(PATHS.extras).pipe(gulp.dest(PATHS.pelican.dest));
}

// Combine JavaScript into one file
// In production, the file is minified
function javascript() {
  return gulp.src(PATHS.javascript)
    .pipe($.babel())
    .pipe($.concat('app.js'))
    .pipe($.if(PRODUCTION, $.uglify()
      .on('error', e => { console.log(e); })
    ))
    .pipe(gulp.dest('src/theme/static/js'));
}

// Copy images to the "theme" folder
// In production, the images are compressed
function images() {
  var imagemin = $.if(PRODUCTION, $.imagemin({
    progressive: true
  }));

  return gulp.src('assets/img/**/*')
    .pipe(imagemin)
    .pipe(gulp.dest('src/theme/static/img'));
}

// Compile Sass into CSS
// In production, the CSS is compressed
function sass() {
  return gulp.src(PATHS.sass.src + '/app.scss')
    .pipe($.sourcemaps.init())
    .pipe($.sass({
      includePaths: PATHS.sass.includePaths
    })
      .on('error', $.sass.logError))
    .pipe($.autoprefixer({
      browsers: COMPATIBILITY
    }))
    // Comment in the pipe below to run UnCSS in production
    //.pipe($.if(PRODUCTION, $.uncss(UNCSS_OPTIONS)))
    //.pipe($.if(PRODUCTION, $.cleanCss({ compatibility: 'ie9' })))
    //.pipe($.if(!PRODUCTION, $.sourcemaps.write()))
    .pipe(gulp.dest(PATHS.sass.dest))
    .pipe(browser.reload({ stream: true }));
}

function uncss() {
  return gulp.src(PATHS.pelican.dest + '/assets/css/app.css')
    .pipe($.if(PRODUCTION, $.uncss(UNCSS_OPTIONS)))
    .pipe($.if(PRODUCTION, $.cleanCss({ compatibility: 'ie9' })))
    .pipe($.rename('app-final.css'))
    .pipe(gulp.dest(PATHS.pelican.dest + '/assets/css/'));
}
    
var building = false;
// Clone the environment and set DEBUG when developing
var env = Object.create(process.env);
if (PRODUCTION) {
  env.DEBUG = '0';
}

function pelican() {
  if (building) {
    log.warn("...pelican build in progress.");
    return;
  }
  building = true;
  var proc = child_process.spawn(PELICAN_BUILD_CMD[0], PELICAN_BUILD_CMD.slice(1), {env: env, stdio: 'inherit'});
  proc.on('error', (error) => {
    building = false;
    log.error(error);
  });
  proc.on('close', () => {
    building = false;
    log.info("done pelican");
  });
  return proc;
}

// Start a server with BrowserSync to preview the site in
function server(done) {
  browser.init({
    server: PATHS.pelican.dest, port: PORT
  });
  done();
}

// Reload the browser with BrowserSync
function reload(done) {
  browser.reload();
  done();
}

// Watch for changes to static sass files
function watch() {
  gulp.watch(PATHS.sass.src + '/**/*.scss').on('all', sass);
  gulp.watch([
    `${PATHS.pelican.src}/**/*`,
  ]).on('all', gulp.series(pelican, reload));
}

//-------------------------------------------------------------------------------------------------
// Gulp tasks
//-------------------------------------------------------------------------------------------------

// build all assets
gulp.task('assets', gulp.parallel(sass, javascript, images, copy));

// Build the "dest" folder by running all of the below tasks
gulp.task('build', gulp.series(clean, 'assets', pelican, uncss));

// Build the site, run the server, and watch for file changes
gulp.task('default', gulp.series('build', server, watch));



