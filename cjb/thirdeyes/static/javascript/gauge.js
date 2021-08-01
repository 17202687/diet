var control = document.getElementById('control');
var bar = document.querySelector('.bar');
var value = document.querySelector('.value');

var RADIUS = 54;
var CIRCUMFERENCE = 2 * Math.PI * RADIUS;

function progress(per) {
  var progress = per / 100;
  var dashoffset = CIRCUMFERENCE * (1 - progress);
  
  //value.innerHTML=per +'%';
  value.innerHTML= "{{content}}";
  bar.style.strokeDashoffset = dashoffset;
}

control.addEventListener('input', function(event) {
  progress(event.target.valueAsNumber);
});
control.addEventListener('change', function(event){
  progress(event.target.valueAsNumber);
});

bar.style.strokeDasharray = CIRCUMFERENCE;
progress(60);