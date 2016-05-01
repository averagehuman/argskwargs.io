
VueJS First Steps - SVG Slider Component
========================================

:tags: VueJs, SVG
:category: Javascript
:author: gflanagan
:date: 2016-04-18 14:00


`VueJS`_  is a reactive javascript framework that will feel familiar to anyone
used to `angularjs`_  - two-way binding between model
and view together with templatized DOM fragments annotated inline with loops
and conditionals.
It bills itself as less opinionated than angular, providing just the view or
presentation part of the application equation without any real idea of a
controller, ie. (in angular terms) Templates, Directives and Components but not
Controllers, Services or Providers. For the controller or business logic
aspects of an application you are expected to make your own decisions.
Similarly, there are no builtin utilities such as `$http`_ or `ngRoute`_, but
there are `plugins`_ that can be pulled in to provide similar behaviour.

The following is first attempt at a Vue component. The model is 

.. jsfiddle:: mdhs1t04
    :width: 100%
    :height: 340
    :tabs: result,html,js,resources
    :skin: light


