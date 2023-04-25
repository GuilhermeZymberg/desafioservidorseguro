 function send(){
   var text = document.getElementById("text");
   var texto = text.value;
   var teste = texto.split(" ");
   var metodo = teste.shift();
   console.log(teste);
   teste = teste.join(" ")
   console.log(teste);
   var texto2 = teste.split("\n");
   var arq = texto2.shift();
   console.log(texto2)
   texto2 = texto2.join("\n");
   const x = new XMLHttpRequest();
   x.open(metodo, arq, true);
   x.send(texto2);
   document.getElementById("text").value = "";
   }