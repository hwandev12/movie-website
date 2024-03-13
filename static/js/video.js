// Get the video element
var video = document.getElementById("videoSingle");
var customPlay = document.querySelector(".custom-play");
var previewVideo = document.querySelector("#previewVideo");

// Create custom controls
var controls = document.createElement("div");
controls.className = "custom-controls";

// Add play/pause button
var playPauseButton = document.createElement("button");
playPauseButton.innerHTML = "<i class='fa fa-play'></i>";
playPauseButton.addEventListener("click", function () {
  if (video.paused) {
    video.play();
    video.style.display = 'block'
    previewVideo.style.display = 'none'
    customPlay.style.display = "none";
    playPauseButton.innerHTML = "<i class='fa fa-pause'></i>";
  } else {
    video.pause();
    customPlay.style.display = "flex";
    playPauseButton.innerHTML = "<i class='fa fa-play'></i>";
  }
});
video.addEventListener("click", function () {
  if (video.paused) {
    video.play();
    video.style.display = 'block'
    previewVideo.style.display = 'none'
    customPlay.style.display = "none";
    playPauseButton.innerHTML = "<i class='fa fa-pause'></i>";
  } else {
    video.pause();
    customPlay.style.display = "flex";
    playPauseButton.innerHTML = "<i class='fa fa-play'></i>";
  }
});
previewVideo.addEventListener("click", function () {
  video.style.display = 'block'
  previewVideo.style.display = 'none'
  video.play();
  customPlay.style.display = "none";
  playPauseButton.innerHTML = "<i class='fa fa-pause'></i>";
});
customPlay.addEventListener("click", function () {
  customPlay.style.display = "none";
  if (video.paused) {
    video.play();
    video.style.display = 'block'
    previewVideo.style.display = 'none'
    playPauseButton.innerHTML = "<i class='fa fa-pause'></i>";
  } else {
    video.pause();
    playPauseButton.innerHTML = "<i class='fa fa-play'></i>";
  }
});
controls.appendChild(playPauseButton);

// Add progress bar
var progressContainer = document.createElement("div");
progressContainer.className = "progress-container";
var progressBar = document.createElement("input");
progressBar.type = "range";
progressBar.min = "0";
progressBar.max = "100";
progressBar.value = "0";
progressBar.className = "progress-bar";
progressBar.addEventListener("input", function () {
  var time = video.duration * (progressBar.value / 100);
  video.currentTime = time;
});
progressContainer.appendChild(progressBar);

// Add time display
var timeDisplay = document.createElement("span");
timeDisplay.className = "time-display";
progressContainer.appendChild(timeDisplay);
controls.appendChild(progressContainer);

// Add volume control
var volumeControl = document.createElement("input");
volumeControl.type = "range";
volumeControl.min = "0";
volumeControl.max = "1";
volumeControl.step = "0.1";
volumeControl.value = "1";
volumeControl.className = "volume-control";
volumeControl.addEventListener("input", function () {
  video.volume = this.value;
});
controls.appendChild(volumeControl);

// Add fullscreen button
var fullscreenButton = document.createElement("button");
fullscreenButton.innerHTML = "<i class='fa fa-expand'></i>";
fullscreenButton.addEventListener("click", function () {
  if (video.requestFullscreen) {
    video.requestFullscreen();
  } else if (video.mozRequestFullScreen) {
    /* Firefox */
    video.mozRequestFullScreen();
  } else if (video.webkitRequestFullscreen) {
    /* Chrome, Safari and Opera */
    video.webkitRequestFullscreen();
  } else if (video.msRequestFullscreen) {
    /* IE/Edge */
    video.msRequestFullscreen();
  }
});
controls.appendChild(fullscreenButton);

// Update progress bar and time display as video plays
video.addEventListener("timeupdate", function () {
  var value = (video.currentTime / video.duration) * 100;
  progressBar.value = value;

  // Update time display
  var remainingTime = formatTime(video.duration - video.currentTime);
  timeDisplay.textContent = remainingTime;
});

// Function to format time in mm:ss format
function formatTime(time) {
  var minutes = Math.floor(time / 60);
  var seconds = Math.floor(time % 60);
  seconds = seconds < 10 ? "0" + seconds : seconds;
  return minutes + ":" + seconds;
}

// Append custom controls to the video element
video.parentNode.insertBefore(controls, video);

// Hide default controls
video.controls = false;
