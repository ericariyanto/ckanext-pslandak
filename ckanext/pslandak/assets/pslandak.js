ckan.module("pslandak-module", function ($, _) {
  "use strict";
  return {
    options: {
      debug: false,
    },

    initialize: function () {
      console.log('pslandak module js initialization');
      console.log(this.options);
    },
  };
});