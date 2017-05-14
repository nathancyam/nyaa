document.addEventListener('DOMContentLoaded', function () {
  var userTableEl = document.querySelector('.user-table');

  userTableEl.addEventListener('click', function (event) {
    if (!event.target.hasClass('row-user')) {
      return event.preventDefault();
    }

    debugger;
  });
});