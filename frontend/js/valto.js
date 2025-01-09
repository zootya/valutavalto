//const myUrl = "http://127.0.0.1";
const myUrl = "http://azenhazam.mywire.org";

function getArfolyam(){
    fetch(`${myUrl}:8800/restadat`).then(res=>res.json()).then(result=>{
        result.forEach(item => {
            document.querySelector("#fetchResult").innerHTML +=
            `
            <div class = "col-12 col-md-6 col-lg-3">
                <img class = "card-img-top" src = "${item.kepUrl}" alt = "">
                    <div class = "card-body">
                        <h4 class = card-title>${item.arfolyam}</h4>
                        <p class = "card-text">${item.id}</p>
                        <p class = "card-text">${item.valutanevek} - ${item.penznem}</p>
                    </div>
                </div> 
            </div>
            `;
        });
    })
}

getArfolyam()