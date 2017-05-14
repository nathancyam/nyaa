document.addEventListener('DOMContentLoaded', function () {
  var userTableEl = document.querySelector('.user-table');

  userTableEl.addEventListener('change', function (event) {
    if (event.target.getAttribute('name') === 'action') {
      var levelSelectEl = event.target.nextElementSibling;

      if (event.target.value === 'level-change' && levelSelectEl.classList.contains('hidden')) {
        levelSelectEl.classList.remove('hidden');
      } else {
        levelSelectEl.classList.add('hidden');
      }
    }
  });
});