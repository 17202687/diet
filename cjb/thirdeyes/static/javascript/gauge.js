var control = document.getElementById('control');
var leftBar = document.querySelector('.left .bar');
var rightBar = document.querySelector('.right .bar');
var per = document.querySelector('.value');

function progress(value) {
  per.innerHTML=value +'%';
  if (value <= 50) {
    var degree = 18*value/5;
    rightBar.style.transform = "rotate("+degree+"deg)";
    leftBar.style.transform = "rotate(0deg)";
  } else {
    var degree = 18*(value-50)/5;
    rightBar.style.transform = "rotate(180deg)";
    leftBar.style.transform = "rotate("+degree+"deg)";
  }
}

control.addEventListener('input', function(event) {
  progress(event.target.valueAsNumber);
});
control.addEventListener('change', function(event){
  progress(event.target.valueAsNumber);
});

progress(60);