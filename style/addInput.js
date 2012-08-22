var counter = 2;
var limit = 20;
function addInput(divName){
     if (counter == limit)  {
          alert("You have reached the limit of adding " + counter + " inputs");
     }
     else {
          var newdiv = document.createElement('div');
          newdiv.innerHTML = "<p><span>Option " + (counter + 1) + "</span><input type=\"text\" name=\"option\" value=\"\" /></p>"          
          document.getElementById(divName).appendChild(newdiv);
          counter++;
     }
}
