// fancyedit.js
$(document).ready(function() {
  $("#id_FIELDNAME").wymeditor({ // "FIELDNAME" is the name of the field you want to give the wysiwyg features
    updateSelector: "input:submit",
    updateEvent: "click"
  });
});
