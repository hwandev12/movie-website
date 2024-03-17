// Get the video element
document.addEventListener("DOMContentLoaded", function () {
  var video = document.getElementById("videoSingle");
  var customPlay = document.querySelector(".custom-play");

  video.addEventListener("play", function () {
    customPlay.style.display = "none";
  });
  video.addEventListener("pause", function () {
    customPlay.style.display = "flex";
  });

  customPlay.addEventListener("click", () => {
    video.play();
    customPlay.style.display = "none";
  });

  document.body.addEventListener("keydown", (e) => {
    if (e.key == "f") {
      if (video.requestFullscreen) {
        video.style.visibility = "visible";
        video.requestFullscreen();
      } else if (video.mozRequestFullScreen) {
        /* Firefox */
        video.style.visibility = "visible";
        video.mozRequestFullScreen();
      } else if (video.webkitRequestFullscreen) {
        /* Chrome, Safari and Opera */
        video.style.visibility = "visible";
        video.webkitRequestFullscreen();
      } else if (video.msRequestFullscreen) {
        /* IE/Edge */
        video.style.visibility = "visible";
        video.msRequestFullscreen();
      }
    }
  });
});
