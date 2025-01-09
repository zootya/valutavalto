//const myUrl = "http://127.0.0.1";
const myUrl = "http://azenhazam.mywire.org";

var id = [];
var penznem = [];
var arfolyam = [];
var valutanevek = [];


function szamol(){
    const mirol = document.querySelector("#inputSelect").value;
    const mire = document.querySelector("#outputSelect").value;
    const mennyit = document.querySelector("#mennyi").value;
    const euroid = penznem.indexOf("EUR");
    
    // 1 USA dollár = EUR/USD*HUF = 401.6 forint
    keresem = arfolyam[euroid] / arfolyam[id.indexOf(parseInt(mirol))] * arfolyam[id.indexOf(parseInt(mire))];
    visszefelekeresem = arfolyam[euroid] / arfolyam[id.indexOf(parseInt(mire))] * arfolyam[id.indexOf(parseInt(mirol))];
    
    document.querySelector(".valtas1sor").innerHTML = mennyit + " " + penznem[id.indexOf(parseInt(mirol))] + " - " + valutanevek[id.indexOf(parseInt(mirol))] + " =";

    document.querySelector(".valtas2sor").innerHTML = mennyit * keresem + " " + penznem[id.indexOf(parseInt(mire))] + " - " + valutanevek[id.indexOf(parseInt(mire))];

    document.querySelector(".valtas3sor").innerHTML = "1 " + penznem[id.indexOf(parseInt(mirol))] + " = " + keresem + " " + penznem[id.indexOf(parseInt(mire))] + "<br>" + "1 " + penznem[id.indexOf(parseInt(mire))] + " = " + visszefelekeresem + " " + penznem[id.indexOf(parseInt(mirol))];
    
}


function getValutaadatok(){
    document.querySelector("#inputSelect").innerHTML = "";
    document.querySelector("#outputSelect").innerHTML = "";

    fetch(`${myUrl}:8800/restadat`).then(res=>res.json()).then(result=>{
        result.forEach(item => {
            item.penznem == "EUR" ? document.querySelector("#inputSelect").innerHTML +=`<option value = "${item.id}" selected>${item.valutanevek} - (${item.penznem})</option>` : document.querySelector("#inputSelect").innerHTML +=`<option value = "${item.id}">${item.valutanevek} - (${item.penznem})</option>`;
            
            item.penznem == "HUF" ? document.querySelector("#outputSelect").innerHTML +=`<option value = "${item.id}" selected>${item.valutanevek} - (${item.penznem})</option>` : document.querySelector("#outputSelect").innerHTML +=`<option value = "${item.id}">${item.valutanevek} - (${item.penznem})</option>`;

            id.push(item.id);
            penznem.push(item.penznem);
            arfolyam.push(item.arfolyam);
            valutanevek.push(item.valutanevek);
        });
    })
}

getValutaadatok()