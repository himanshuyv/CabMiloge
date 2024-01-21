
function createBookingDetailsDiv(displayText) {
    let newDiv = document.createElement("div");
    newDiv.classList.add("card");
    let heading = document.createElement("h1");
    heading.textContent = displayText;
    newDiv.appendChild(heading);
    let flexContainer = document.querySelector('.flex-container');
    flexContainer.appendChild(newDiv);
    newDiv.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
}

let arrival;
let departure;

function arrivalDepartureFunction(typeOfTravel){
    if (!arrival && typeOfTravel==="Arrival"){
        arrival = document.createElement("div");
        arrival.classList.add("card");
        let heading = document.createElement("h1");
        heading.textContent = typeOfTravel;
        arrival.appendChild(heading);
        let flexContainer = document.querySelector('.flex-container');
        flexContainer.appendChild(arrival);
        arrival.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
    }else{
        arrival.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
    }

    if (!departure && typeOfTravel==="Departure"){
        departure = document.createElement("div");
        departure.classList.add("card");
        let heading = document.createElement("h1");
        heading.textContent = typeOfTravel;
        departure.appendChild(heading);
        let flexContainer = document.querySelector('.flex-container');
        flexContainer.appendChild(departure);
        departure.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
    }else{
        departure.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
    }
}
  

let bookingDiv;

function createNewBookingDiv(){
    if (!bookingDiv){
        bookingDiv = document.createElement("div");
        bookingDiv.classList.add("card");
        let Button1 = document.createElement("Button");
        let Button2 = document.createElement("Button");
        Button1.textContent = "Arrival";
        Button2.textContent = "Departure";
        Button1.classList.add("arrival-departure");
        Button2.classList.add("arrival-departure");

        Button1.onclick = function(){
            arrivalDepartureFunction("Arrival");
        }

        Button2.onclick = function(){
            arrivalDepartureFunction("Departure");
        }

        let containerDiv = document.createElement("div");
        containerDiv.classList.add("arrival-departure-container");
        containerDiv.appendChild(Button1);
        containerDiv.appendChild(Button2);
        bookingDiv.appendChild(containerDiv);
        let flexContainer = document.querySelector('.flex-container');
        flexContainer.appendChild(bookingDiv);
        bookingDiv.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
    }else{
        bookingDiv.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
    }
}