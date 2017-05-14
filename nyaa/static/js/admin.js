document.addEventListener('DOMContentLoaded', function () {
  var userTableEl = document.querySelector('.user-table');
  var massActions = document.querySelector('#mass-actions select[name="action"]');
  var selectAllEl = document.querySelector('#select-all');

  /**
   * @param {Node} node
   * @param {Function} callback
   * @returns {*}
   */
  function recurUserRow(node, callback) {
    if (!node.classList.contains('row-user')) {
      return recurUserRow(node.parentNode, callback);
    } else {
      return callback(node);
    }
  }

  function onLevelSelect(event) {
    if (event.target.getAttribute('name') === 'action') {
      var levelSelectEl = event.target.nextElementSibling;

      if (event.target.value === 'level-change' && levelSelectEl.classList.contains('hidden')) {
        levelSelectEl.classList.remove('hidden');
      } else {
        levelSelectEl.classList.add('hidden');
      }
    }
  }

  selectAllEl.addEventListener('click', function (event) {
    event.preventDefault();

    var rows = Array.prototype.slice.call(userTableEl.querySelectorAll('.row-user'));
    var checkboxes = rows.map(function (row) { return row.querySelector('.checkbox'); });

    checkboxes.forEach(function (checkbox) {
      checkbox.checked = !checkbox.checked;
    })
  });

  massActions.addEventListener('change', onLevelSelect);

  userTableEl.addEventListener('change', onLevelSelect);

  userTableEl.addEventListener('click', function (event) {
    return recurUserRow(event.target, function (userRow) {
      var checkbox = userRow.querySelector('.checkbox');
      checkbox.checked = !checkbox.checked;
    });
  });
});