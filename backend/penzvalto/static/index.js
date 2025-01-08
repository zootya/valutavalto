const adatok = document.getElementById("adatok"); //ezzel egy div elemre hivatkozz

//a függvény lekéri az árfolyamadatokat az adatbázisból és kiíja őket egy html fájlba felsorolásban
function getAll() {
    fetch("http://127.0.0.1:8000/restadat/")
        .then(res => res.json())
        .then(result => {
            result.forEach(item => {
                document.querySelector("#adatok").innerHTML += `
                    <div>
                        <ul>
                            <li>Pénznem: ${item.penznem} Árfolyam: ${item.arfolyam}</li>
                        </ul>
                    </div>
                `;
            });
        })
        .catch(error => console.error('Hiba:', error));
}

getAll();