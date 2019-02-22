var images = [
  'https://hdqwalls.com/download/godzilla-hawaii-2560x1440.jpg',
  'https://orig00.deviantart.net/8cf3/f/2018/084/9/e/avengers_infinity_war___wallpaper_1920x1080_by_sachso74-dc63de9.jpg',
  'https://orig00.deviantart.net/1620/f/2013/182/0/7/attack_on_titan_by_kaskianiohchan-d6bh077.jpg'
]

var imagetag = document.getElementById("bg_image");

var i = 0;
setInterval(function() {
      imagetag.style.backgroundImage = "url(" + images[i] + ")";
      i = i + 1;
      if (i == images.length) {
        i =  0;
      }
}, 2000);