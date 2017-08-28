$(function () {
  function check_medications() {
    $.ajax({
      url: '/medications/check/',
      cache: false,
      success: function (data) {
        $("#overdue-count").text(data);
        print('AJAX TEST - COUNT: ' + data);
      },
      complete: function () {
        window.setTimeout(check_medications, 60000);
      }
    });
  };
  check_medications();

});