let bookingDiv;
let directionOfTravel;
let curDate = new Date();

let img1 = document.getElementById("img1")
let img2 = document.getElementById("img2")


img1.addEventListener("click", function () {
  switchBookingType("From Campus");
});
img2.addEventListener("click", function () {
  switchBookingType("To Campus");
});

function switchBookingType(direction) {
  if (directionOfTravel) {
    directionOfTravel.remove();
    directionOfTravel = null;
  }
  sendDataForBooking(direction);
}

function sendDataForBooking(direction) {
  directionOfTravel = document.createElement("div");
  directionOfTravel.classList.add("card");
  directionOfTravel.classList.add("form-div");
  if (direction === "From Campus" || direction === "To Campus") {
    let heading = document.createElement("h1");
    heading.textContent = direction;
    heading.classList.add("from-to-heading");
    directionOfTravel.appendChild(heading);
    let form = document.createElement("form");
    form.method = "post";
    form.action = "getDataForBooking";
    let input = document.createElement("input");
    input.type = "hidden";
    input.name = "direction";
    input.value = direction;
    form.appendChild(input);
    let stationLabel = document.createElement("label");
    stationLabel.textContent = `${direction === "From Campus" ? "To" : "From"
      } Station:`;
    let stationDropdown = document.createElement("select");
    stationDropdown.name = "station";
    stationDropdown.required = true;



    let stations = [
      "Rajiv Gandhi International Airport",
      "Secunderabad Junction",
      "Kacheguda Railway Station",
    ];

    for (let station of stations) {
      let option = document.createElement("option");
      option.value = station;
      option.textContent = station;
      stationDropdown.appendChild(option);
    }

    stationLabel.appendChild(stationDropdown);

    let dateLabel = document.createElement("label");
    dateLabel.textContent = "Date of Departure:";
    let dateInput = document.createElement("input");
    dateInput.type = "date";
    dateInput.name = "departureDate";
    dateInput.min = curDate.toISOString().split("T")[0];
    dateLabel.appendChild(dateInput);
    dateInput.required = true;


    let timeLabel = document.createElement("label");
    timeLabel.textContent = "Time of Departure:";
    let timeInput = document.createElement("input");
    timeInput.type = "time";
    timeInput.name = "departureTime";
    timeLabel.appendChild(timeInput);
    timeInput.required = true;

    let submitButton = document.createElement("button");
    submitButton.type = "submit";
    submitButton.textContent = "Submit";

    form.appendChild(stationLabel);
    form.appendChild(dateLabel);
    form.appendChild(timeLabel);
    form.appendChild(submitButton);
    
    directionOfTravel.appendChild(form);
  }
  let flexContainer = document.querySelector(".flex-container");
  flexContainer.appendChild(directionOfTravel);
  directionOfTravel.scrollIntoView({
    behavior: "smooth",
    block: "end",
    inline: "nearest",
  });
}


function deleteBooking(entry_id, direction) {
  let form = document.createElement("form");
  form.method = "post";
  form.action = "deleteBooking";
  let input = document.createElement("input");
  input.type = "hidden";
  input.name = "entry_id";
  input.value = entry_id;
  form.appendChild(input);
  input = document.createElement("input");
  input.type = "hidden";
  input.name = "direction";
  if (direction === 0) {
    input.value = "From Campus";
  } else {
    input.value = "To Campus";
  }
  form.appendChild(input);
  document.body.appendChild(form);
  form.submit();
}



function redirect_to_booking() {
  window.location.href = "/viewBookingRedirect";

}

function logout_user() {
  let form = document.createElement("form");
  form.method = "post";
  form.action = "logout_user";
  document.body.appendChild(form);
  form.submit();
}

// Dropdown functions
function toggleUserDropDown() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
// window.onclick = function (e) {
//   if (!e.target.matches('.dropbtn')) {
//     var myDropdown = document.getElementById("myDropdown");
//     if (myDropdown.classList.contains('show')) {
//       myDropdown.classList.remove('show');
//     }
//   }
// }


/////////////////////////////////////////////// SIDEBAR 

document.getElementById("openSidebar").onclick = function () {
  document.getElementById("sidebar").style.width = "23rem";
  document.getElementById("overlay").style.display = "block";
}

document.getElementById("closeSidebar").onclick = function () {
  document.getElementById("sidebar").style.width = "0";
  document.getElementById("overlay").style.display = "none";
}

// Close sidebar when clicking outside of it
document.getElementById("overlay").onclick = function () {
  document.getElementById("sidebar").style.width = "0";
  document.getElementById("overlay").style.display = "none";
}