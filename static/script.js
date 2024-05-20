let bookingDiv;
let directionOfTravel;

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

    // Event listeners for image clicks to switch booking type
    img1.addEventListener("click", function () {
      switchBookingType("From Campus");
    });
    img2.addEventListener("click", function () {
      switchBookingType("To Campus");
    });

    wrapperDiv1.appendChild(img1);
    wrapperDiv2.appendChild(img2);
    wrapperDiv1.appendChild(heading1);
    wrapperDiv2.appendChild(heading2);
    let containerDiv = document.createElement("div");
    containerDiv.classList.add("arrival-departure-container");
    containerDiv.appendChild(wrapperDiv1);
    containerDiv.appendChild(wrapperDiv2);
    bookingDiv.appendChild(containerDiv);
    let flexContainer = document.querySelector(".flex-container");
    flexContainer.appendChild(bookingDiv);
    bookingDiv.scrollIntoView({
      behavior: "smooth",
      block: "end",
      inline: "nearest",
    });
  } else {
    bookingDiv.scrollIntoView({
      behavior: "smooth",
      block: "end",
      inline: "nearest",
    });
  }
}

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
  if (direction === "From Campus" || direction === "To Campus") {
    let heading = document.createElement("h1");
    heading.textContent = direction;
    heading.classList.add("from-to-heading");
    directionOfTravel.appendChild(heading);
    let formContainer = document.createElement("div");
    formContainer.classList.add("form-container");
    let form = document.createElement("form");
    form.method = "post";
    form.action = "getDataForBooking";
    let input = document.createElement("input");
    input.type = "hidden";
    input.name = "direction";
    input.value = direction;
    form.appendChild(input);
    let stationLabel = document.createElement("label");
    stationLabel.textContent = `${
      direction === "From Campus" ? "To" : "From"
    } Station:`;
    let stationDropdown = document.createElement("select");
    stationDropdown.name = "station";

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
    dateLabel.appendChild(dateInput);

    let timeLabel = document.createElement("label");
    timeLabel.textContent = "Time of Departure:";
    let timeInput = document.createElement("input");
    timeInput.type = "time";
    timeInput.name = "departureTime";
    timeLabel.appendChild(timeInput);

    let submitButton = document.createElement("button");
    submitButton.type = "submit";
    submitButton.textContent = "Submit";

    form.appendChild(stationLabel);
    form.appendChild(dateLabel);
    form.appendChild(timeLabel);
    form.appendChild(submitButton);

    formContainer.appendChild(form);
    directionOfTravel.appendChild(formContainer);
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

function redirect_to_booking(entry_id, direction) {
  window.location.href = "/viewBookingRedirect";
  let form = document.createElement("form");
  form.method = "post";
  form.action = "viewBookingRedirect";
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
window.onclick = function(e) {
  if (!e.target.matches('.dropbtn')) {
  var myDropdown = document.getElementById("myDropdown");
    if (myDropdown.classList.contains('show')) {
      myDropdown.classList.remove('show');
    }
  }
}