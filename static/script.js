let directionOfTravel;

function directionOfTravelFunction(direction) {
    if (!directionOfTravel) {
        directionOfTravel = document.createElement("div");
        directionOfTravel.classList.add("card");
        let heading = document.createElement("h1");
        heading.textContent = direction;
        directionOfTravel.appendChild(heading);
        let flexContainer = document.querySelector('.flex-container');
        flexContainer.appendChild(directionOfTravel);
        directionOfTravel.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
    } else{
        directionOfTravel.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
    }   
}

let bookingDiv;
function createNewBookingDiv() {
    if (!bookingDiv) {
        bookingDiv = document.createElement("div");
        bookingDiv.classList.add("card");
        let img1 = document.createElement("img");
        let img2 = document.createElement("img");
        let label1 = "From Campus";
        let label2 = "To Campus";
        let wrapperDiv1 = document.createElement("div");
        let wrapperDiv2 = document.createElement("div");
        
        wrapperDiv1.classList.add("label");
        wrapperDiv2.classList.add("label");
        let heading1 = document.createElement("div");
        let heading2 = document.createElement("div");
        heading1.textContent = label1;
        heading2.textContent = label2;

        wrapperDiv1.classList.add("image-container");
        wrapperDiv2.classList.add("image-container");
        img1.src = "./../static/from-campus.svg";
        img2.src = "./../static/to-campus.svg";
        img1.classList.add("arrival-departure");
        img2.classList.add("arrival-departure");
        img1.onclick = function () {
            directionOfTravelFunction("From Campus")
        };
        img2.onclick = function () {
            directionOfTravelFunction("To Campus")
        };
        wrapperDiv1.appendChild(img1);
        wrapperDiv2.appendChild(img2);
        wrapperDiv1.appendChild(heading1);
        wrapperDiv2.appendChild(heading2);
        let containerDiv = document.createElement("div");
        containerDiv.classList.add("arrival-departure-container");
        containerDiv.appendChild(wrapperDiv1);
        containerDiv.appendChild(wrapperDiv2);
        bookingDiv.appendChild(containerDiv);
        let flexContainer = document.querySelector('.flex-container');
        flexContainer.appendChild(bookingDiv);
        bookingDiv.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
    } else {
        bookingDiv.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
    }
}


