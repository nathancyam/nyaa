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

  function rowHandler(event, callback) {
    var action = event.target.getAttribute('data-action');

    var actions = {
      banned: {
        predicate: action === 'ban',
        formSelector: 'input[name="banned"]',
        callback: function (formInput) {
          formInput.value = "2";
        }
      },

      unban: {
        predicate: action === 'unban',
        formSelector: 'input[name="banned"]',
        callback: function (formInput) {
          formInput.value = "1";
        }
      },

      updateLevel: {
        predicate: action === 'level-select',
        formSelector: 'input[name="level"]',
        callback: function (formInput, node) {
          formInput.value = node.value;
        }
      }
    };

    Object.keys(actions)
      .filter(function (action) { return actions[action].predicate; })
      .forEach(function (action) {
        action = actions[action];

        return recurUserRow(event.target, function (userRow) {
          return action.callback(
            userRow.querySelector('.edit-form ' + action.formSelector),
            event.target
          );
        });
      });

    return recurUserRow(event.target, function (userRow) {
      callback(event, userRow);
    });
  }

  massActions.addEventListener('change', onLevelSelect);

  userTableEl.addEventListener('change', onLevelSelect);

  userTableEl.addEventListener('click', function (event) {
    if (event.target.nodeName !== 'TD') {
      return;
    }

    return recurUserRow(event.target, function (userRow) {
      var checkbox = userRow.querySelector('.checkbox');
      checkbox.checked = !checkbox.checked;
    });
  });

  userTableEl.addEventListener('click', function (event) {
    event.preventDefault();

    if (!event.target.classList.contains('edit-btn')) {
      return;
    }

    return recurUserRow(event.target, function (userRow) {
      userRow.classList.toggle('editing');
    });
  });

  userTableEl.addEventListener('click', function (event) {
    rowHandler(event, function (event, userRow) {
      if (event.target.getAttribute('data-action').indexOf('ban') !== -1) {
        userRow.querySelector('.edit-form').submit();
      }
    });
  });
});