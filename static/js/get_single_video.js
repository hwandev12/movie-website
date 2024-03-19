$(document).ready(function () {
  let carouselItemAll = document.querySelectorAll(".carousel__item-right");
  carouselItemAll.forEach((e) => {
    e.addEventListener("click", () => {
      let id = e.getAttribute("data-show-id")
      let isMovie = e.getAttribute("data-ismovie-id")
      let trailerVideoHTML = document.getElementById("youtubeTrailer")
      let trailerVideoHTMLSerie = document.getElementById("youtubeTrailerSerie")

      // Ajax Call
      $.ajax({
        url: `/movies/ajax-single-movie-get/${id}/`,
        type: "GET",
        data: { is_movie: isMovie },
        success: (res) => {
          if(isMovie == 'movie') {
            let trailer = JSON.parse(res.trailer_ajax)
            trailerVideoHTML.src = trailer[0].fields.url
          }else {
            let trailer = JSON.parse(res.serie_trailer)
            trailerVideoHTMLSerie.src = trailer[0].fields.url
          }
        },
        error: (xhr, status, error) => {
          console.log(xhr.responseText);
        }
      })

    });
  });
});
