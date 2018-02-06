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

// UnCSS will use these settings
const UNCSS_OPTIONS = {
  html: "src/**/*.html",
  ignore: [
    /.foundation-mq/,
    /^\.is-.*/,
  ]
};

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
  pelican: {
    src: "src",
    dest: "build",
  },
  dist: "dist"
};


const PWD = process.cwd();

const PELICAN_BUILD_CMD = [
  'pelican',
  PATHS.pelican.src,
  '-o',
  PATHS.pelican.dest,
  '-s',
  `${PATHS.pelican.src}/config.py`,
  '-D'
];

// Check for --production flag
const PRODUCTION = !!(yargs.argv.production);


//-------------------------------------------------------------------------------------------------
// Gulp tasks
//-------------------------------------------------------------------------------------------------

gulp.task('assets',
 gulp.series(clean, sass));

// Build the "dest" folder by running all of the below tasks
gulp.task('build',
 gulp.series(clean, sass, pelican));

// Build the site, run the server, and watch for file changes
gulp.task('default',
  gulp.series('build', server, watch));

// Delete the "build" folder
// This happens every time a build starts
function clean(done) {
  rimraf(PATHS.pelican.dest, done);
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
    .pipe($.if(PRODUCTION, $.cleanCss({ compatibility: 'ie9' })))
    //.pipe($.if(!PRODUCTION, $.sourcemaps.write()))
    .pipe(gulp.dest(PATHS.sass.dest))
    .pipe(browser.reload({ stream: true }));
}

var building = false;
// Clone the environment and set DEBUG when developing
var env = Object.create(process.env);
if (!PRODUCTION) {
  env.DEBUG = '1';
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
