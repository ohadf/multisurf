// Saves options to localStorage.
function save_options() {
  var select = document.getElementById("verbosity");
  var current_verbosity = select.children[select.selectedIndex].value;
  localStorage["verbosity"] = current_verbosity;

	localStorage["warning_string"] = document.getElementById("warning_string").value;
	localStorage["safe_string"] = document.getElementById("safe_string").value;
		
  // Update status to let user know options were saved.
  var status = document.getElementById("status");
  status.innerHTML = "Options Saved.";
  setTimeout(function() {
    status.innerHTML = "";
  }, 750);
}

// Restores select box state to saved value from localStorage.
function restore_options() {
  var current_verbosity = localStorage["verbosity"];
  if (!current_verbosity) {
    return;
  }
  var select = document.getElementById("verbosity");
  for (var i = 0; i < select.children.length; i++) {
    var child = select.children[i];
    if (child.value == current_verbosity) {
      child.selected = "true";
      break;
    }
  }
  
  document.getElementById("warning_string").value = localStorage["warning_string"];
  document.getElementById("safe_string").value = localStorage["safe_string"];
}

document.addEventListener('DOMContentLoaded', restore_options);
document.querySelector('#save').addEventListener('click', save_options);
