document.addEventListener("DOMContentLoaded", function () {
  const banner = document.getElementById("banner-bg");
  const images = [
    "/static/img/fondo1.png",
    "/static/img/fondo2.png",
    "/static/img/fondo3.png",
    "/static/img/fondo4.png",
    "/static/img/fondo5.png",
    "/static/img/fondo6.png",
  ];
  let index = 0;

  setInterval(() => {
    index = (index + 1) % images.length;
    banner.style.backgroundImage = `url('${images[index]}')`;
  }, 5000);
});
