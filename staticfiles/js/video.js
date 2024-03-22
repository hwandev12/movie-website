// Get the video element
document.addEventListener("DOMContentLoaded", function () {
  ("use strict");

  var video = document.getElementById("videoSingle");
  const playNpauseBtn = document.querySelector("#play-pause");
  const rewindBtn = document.querySelector("#rewind");
  const fastForwardBtn = document.querySelector("#fast-forward");
  const volumeBtn = document.querySelector("#volume");
  const fullScreen = document.querySelector("#fullscreen");
  const progressIndicator = document.querySelector("#progress-indicator");
  const progessBar = document.querySelector("#progress-bar");
  const controls = document.querySelector("#controls");
  const customPlay = document.querySelector(".custom-play");
  const volumeChangeDown = document.querySelector("#volumeRange");

  let mouseIsDown = false;
  function seekingFn(e) {
    const updatedTime = (e.offsetX / progessBar.offsetWidth) * video.duration;

    video.currentTime = updatedTime;
  }

  function playNpauseFn() {
    if (video.paused || video.ended) {
      video.play();
    } else {
      video.pause();
    }
  }

  function updatePlayNPauseIcon() {
    const icon = playNpauseBtn.querySelector("i");
    icon.textContent = "";

    icon.textContent = video.pause ? "play_arrow" : "paused";
  }

  function playNpauseFn() {
    if (video.paused) {
      customPlay.style.display = "none";
      video.play();
    } else {
      customPlay.style.display = "flex";
      video.pause();
    }
  }

  function updatePlayNPauseIcon() {
    const icon = playNpauseBtn.querySelector("i");
    icon.textContent = "";

    icon.textContent = video.paused ? "play_arrow" : "paused";
  }

  function rewindNforwardFn(type) {
    video.currentTime += type === "rewind" ? -10 : 10;
  }

  function muteNunmuteFn() {
    video.muted = video.muted ? false : true;
  }

  function updateVolumeIcon() {
    const icon = volumeBtn.querySelector("i");
    icon.textContent = "";
    icon.textContent = video.muted ? "volume_off" : "volume_up";
  }

  function updateProgress() {
    const progressPercentage = (video.currentTime / video.duration) * 100;

    progressIndicator.style.width = `${progressPercentage}%`;
  }

  rewindBtn.addEventListener("click", () => rewindNforwardFn("rewind"));
  fastForwardBtn.addEventListener("click", () => rewindNforwardFn("forward"));

  video.addEventListener("volumechange", updateVolumeIcon);
  volumeBtn.addEventListener("click", muteNunmuteFn);

  video.addEventListener("play", updatePlayNPauseIcon);
  video.addEventListener("click", playNpauseFn);
  video.addEventListener("pause", updatePlayNPauseIcon);
  playNpauseBtn.addEventListener("click", playNpauseFn);
  video.addEventListener("timeupdate", updateProgress);
  customPlay.addEventListener("click", playNpauseFn);

  progessBar.addEventListener("mousedown", () => (mouseIsDown = true));
  progessBar.addEventListener("mouseup", () => (mouseIsDown = false));
  progessBar.addEventListener("click", seekingFn);
  progessBar.addEventListener("mousemove", (e) => mouseIsDown && seekingFn);

  volumeChangeDown.addEventListener("input", () => {
    video.volume = volumeRange.value;
    video.muted = false;
  });

  video.volume = volumeChangeDown.value;

  window.addEventListener("keydown", (e) => {
    if (e.code === "Space") {
      e.preventDefault();
      playNpauseFn();
    } else if (e.code === "ArrowLeft") {
      rewindNforwardFn("rewind");
    } else if (e.code === "ArrowRight") {
      rewindNforwardFn("forward");
    } else {
      return;
    }
  });
  fullScreen.addEventListener("click", () => {
    if (!document.fullscreenElement) {
      if (document.documentElement.requestFullscreen) {
        document.documentElement.requestFullscreen();
      } else if (document.documentElement.webkitRequestFullscreen) {
        document.documentElement.webkitRequestFullscreen();
      }
      screen.orientation.lock("landscape");
    } else {
      document.exitFullscreen();
      screen.orientation.unlock();
    }
  });

  document.body.addEventListener("keydown", (e) => {
    if (e.key == "f") {
      if (!document.fullscreenElement) {
        if (document.documentElement.requestFullscreen) {
          document.documentElement.requestFullscreen();
        } else if (document.documentElement.webkitRequestFullscreen) {
          // For older versions of Safari
          document.documentElement.webkitRequestFullscreen();
        }
        // Set screen orientation to landscape
        screen.orientation.lock("landscape");
      } else {
        document.exitFullscreen(); // Exit fullscreen mode
        // Unlock screen orientation
        screen.orientation.unlock();
      }
    }
  });

  document.addEventListener("fullscreenchange", toggleCustomControls);

  function toggleCustomControls() {
    if (document.fullscreenElement) {
      document
        .querySelector(".single__movie-video_player")
        .classList.remove("container");
      document
        .querySelector(".single__movie-video_player")
        .classList.add("activeSingle");

      document.body.style.overflow = "hidden";
      video.classList.add("activeVideo");
      screen.orientation.lock("landscape")
    } else {
      document
        .querySelector(".single__movie-video_player")
        .classList.add("container");
      document
        .querySelector(".single__movie-video_player")
        .classList.remove("activeSingle");
      document.body.style.overflow = "scroll";

      video.classList.remove("activeVideo");
      screen.orientation.unlock()
    }
  }
});
