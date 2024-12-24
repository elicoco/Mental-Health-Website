function showSnackbar(message, colour, time=3) {
  var snackbar = document.createElement("div");
  snackbar.textContent = message;

  // Apply styles
  snackbar.style.position = "fixed";
  snackbar.style.top = "20px";
  snackbar.style.left = "50%";
  snackbar.style.transform = "translateX(-50%)";
  snackbar.style.backgroundColor = colour;
  snackbar.style.color = "#FFFFFF";
  snackbar.style.padding = "10px 20px";
  snackbar.style.borderRadius = "5px";
  snackbar.style.zIndex = "1000";

  // Add to body
  document.body.appendChild(snackbar);

  // Remove after time seconds
  setTimeout(function () {
    snackbar.style.opacity = "0";
    setTimeout(function () {
      document.body.removeChild(snackbar);
    }, 500);
  }, time*1000);
}
