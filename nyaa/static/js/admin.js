document.addEventListener('DOMContentLoaded', function () {
  var userTableEl = document.querySelector('.user-table');
  var massActions = document.querySelector('#mass-actions select[name="action"]');
  var selectAllEl = document.querySelector('#select-all');
  var massActionForm = document.querySelector('form#mass-actions');

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

  massActionForm.addEventListener('submit', function (event) {
    debugger;
    var checkboxes = Array.prototype.slice.call(userTableEl.querySelectorAll('.checkbox'));
    var selectedCheckboxes = checkboxes.filter(function (checkbox) {
      return checkbox.checked;
    });

    var selectedIds = selectedCheckboxes.map(function (checkbox) {
      return checkbox.getAttribute('data-user-id');
    });

    var hiddenInput = event.target.querySelector('input[name="selected_ids"]');
    hiddenInput.value = selectedIds.join(',');

    event.target.submit();
  });

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