// side navigation bar
function toggleSidebar() {
  document.getElementById("side-nav").classList.toggle("toggle-active");
  document.getElementById("main").classList.toggle("toggle-active");
  document.getElementById("top-navbar").classList.toggle("toggle-active");
  document.querySelector(".manage-wrap").classList.toggle("toggle-active");
}

// #################################
// popup

var c = 0;
function pop() {
  if (c == 0) {
    document.getElementById("popup-box").style.display = "block";
    c = 1;
  } else {
    document.getElementById("popup-box").style.display = "none";
    c = 0;
  }
}

// const popupMessagesButtons = document.querySelectorAll('popup-btn-messages')

// popupMessagesButtons.forEach(button, () => {
//     button.addEventListener('click', () => {
//         document.getElementById('popup-box-messages').style.display = 'none';
//     })
// })

// const popupMessagesButtom = document.getElementById('popup-btn-messages')
// popupMessagesButtom.addEventListener('click', () => {
//     document.getElementById('popup-box-messages').style.display = 'none';
// })
// ##################################

// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
  "use strict";

  window.addEventListener(
    "load",
    function () {
      // Fetch all the forms we want to apply custom Bootstrap validation styles to
      var forms = document.getElementsByClassName("needs-validation");

      // Loop over them and prevent submission
      Array.prototype.filter.call(forms, function (form) {
        form.addEventListener(
          "submit",
          function (event) {
            if (form.checkValidity() === false) {
              event.preventDefault();
              event.stopPropagation();
            }
            form.classList.add("was-validated");
          },
          false
        );
      });
    },
    false
  );
})();
// ##################################

// extend and collapse
function showCourses(btn) {
  var btn = $(btn);

  if (collapsed) {
    btn.html('Collapse <i class="fas fa-angle-up"></i>');
    $(".hide").css("max-height", "unset");
    $(".white-shadow").css({ background: "unset", "z-index": "0" });
  } else {
    btn.html('Expand <i class="fas fa-angle-down"></i>');
    $(".hide").css("max-height", "150");
    $(".white-shadow").css({
      background: "linear-gradient(transparent 50%, rgba(255,255,255,.8) 80%)",
      "z-index": "2",
    });
  }
  collapsed = !collapsed;
}

document.addEventListener('DOMContentLoaded', function () {
    var toggles = document.querySelectorAll('.icon');

    toggles.forEach(function (toggle) {
        toggle.addEventListener('click', function () {
            var target = document.querySelector(this.getAttribute('href'));

            toggles.forEach(function (otherToggle) {
                if (otherToggle !== toggle) {
                    var otherTarget = document.querySelector(otherToggle.getAttribute('href'));
                    otherToggle.classList.remove('rotate');
                    otherTarget.classList.remove('show');
                }
            });

            if (target.classList.contains('show')) {
                this.classList.remove('rotate');
            } else {
                this.classList.add('rotate');
            }
        });
    });

    $('.collapse').on('shown.bs.collapse', function () {
        var toggle = document.querySelector('a[href="#' + this.id + '"]');
        toggle.classList.add('rotate');
    });

    $('.collapse').on('hidden.bs.collapse', function () {
        var toggle = document.querySelector('a[href="#' + this.id + '"]');
        toggle.classList.remove('rotate');
    });
});
// this is the right side navigation js
document.getElementById('toggleButton').addEventListener('click', function () {
    const sidenav = document.getElementById('rightSidenav');
    const overlay = document.getElementById('screenOverlay');

    // Toggle the 'show' class on the sidenav
    sidenav.classList.toggle('show');

    // Toggle the display of the overlay based on the 'show' class presence
    overlay.style.display = sidenav.classList.contains('show') ? 'block' : 'none';
});

// Hide the side navigation and overlay when clicking on the overlay
document.getElementById('screenOverlay').addEventListener('click', function () {
    const sidenav = document.getElementById('rightSidenav');
    const overlay = document.getElementById('screenOverlay');

    sidenav.classList.remove('show');
    overlay.style.display = 'none';
});

// Close button functionality for right side navigation
document.getElementById('closeToggleButton').addEventListener('click', function () {
    const sidenav = document.getElementById('rightSidenav');
    const overlay = document.getElementById('screenOverlay');

    // Remove the 'show' class from the sidenav
    sidenav.classList.remove('show');

    // Hide the overlay
    overlay.style.display = 'none';
});

// Toggle the side navigation and screen overlay
document.getElementById('toggleSidenavButton').addEventListener('click', function () {
    const sidenav = document.getElementById('sidenav');
    const overlay = document.getElementById('screenOverlay');

    // Toggle the 'show' class on the sidenav
    sidenav.classList.toggle('show');

    // Toggle the display of the overlay based on the 'show' class presence
    overlay.style.display = sidenav.classList.contains('show') ? 'block' : 'none';
});

// Hide the side navigation and overlay when clicking on the overlay
document.getElementById('screenOverlay').addEventListener('click', function () {
    const sidenav = document.getElementById('sidenav');
    const overlay = document.getElementById('screenOverlay');

    sidenav.classList.remove('show');
    overlay.style.display = 'none';
});