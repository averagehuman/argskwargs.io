
VueJS First Steps - SVG Slider Component
========================================

:tags: VueJs, SVG
:category: Javascript
:author: gflanagan
:date: 2016-04-18 14:00


`VueJS`_  is a reactive javascript framework that will feel reasonably familiar
to anyone that has used `knockout`_ or `angular`_. Like those other frameworks,
VueJS features two-way binding between data and view, self-contained
components and templatised DOM fragments annotated inline with loops and
conditionals.

A flavour of the template syntax from the `vuejs docs`_:

.. code-block:: html

    <div id="app">
        <ul>
            <li class="user" v-for="user in users">
                <span>{{user.name}} - {{user.email}}</span>
                <button v-on:click="removeUser(user)">X</button>
            </li>
        </ul>
        <form id="form" v-on:submit="addUser">
            <input v-model="newUser.name">
            <input v-model="newUser.email">
            <input type="submit" value="Add User">
        </form>
        <ul class="errors">
            <li v-show="!validation.name">Name cannot be empty.</li>
            <li v-show="!validation.email">Please provide a valid email address.</li>
        </ul>
    </div>

In comparison to angular, VueJS is a lighter, less opinionated framework,
providing just the view or presentation part of an application without enforcing
any idea of a controller. So, in angular terms: Templates, Directives and
Components but not Controllers, Services or Providers. For the controller or
business logic aspect of an application you are expected to make your own
decisions. Similarly, there are no kitchen-sink utilities such as angular's
`$http`_ or `$cookies`_ , but there are `plugins`_ that you can use or create to
provide equivalent functionality.

VueJS 1.0 `was released last year`_ and an upcoming backwards-compatible
version 2 `was recently announced`_.

After a brief play, I like it. It's slick. It's modern. It's easy to reason about.
It can be a single script tag on a page or a module in `a larger application`_.
So yeah.


Example
-------

The following is a first attempt at a Vue component. The model is a simple "stat"
object with a numeric "value" property. This value is two-way bound to a range
input element, and one-way bound to a coloured "pill" which is an elongated SVG
rectangle with rounded corners. So moving the input slider changes the model data
which in turn changes the width of the coloured pill. The component itself is
simply a vertical sequence of these input+pill pairs at hard-coded intervals.
(Note: html range inputs are not available in IE9 or earlier).

.. jsfiddle:: mdhs1t04
    :width: 100%
    :height: 460
    :tabs: result,html,js,resources
    :skin: light

.. _vuejs: https://vuejs.org
.. _angular: https://angularjs.org/
.. _knockout: http://knockoutjs.com/
.. _vuejs docs: https://vuejs.org/examples/firebase.html
.. _$http: https://docs.angularjs.org/api/ng/service/$http
.. _$cookies: https://docs.angularjs.org/api/ngCookies/service/$cookies
.. _plugins: https://vuejs.org/guide/plugins.html
.. _a larger application: https://vuejs.org/guide/application.html
.. _was released last year: http://vuejs.org/2015/10/26/1.0.0-release/
.. _was recently announced: http://vuejs.org/2016/04/27/announcing-2.0/

