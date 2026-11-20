document.addEventListener("DOMContentLoaded", function () {

    // Destination card animation

    const cards = document.querySelectorAll(".card");

    cards.forEach(card => {

        card.addEventListener("mouseenter", function () {
            card.style.transform = "translateY(-7px)";
        });

        card.addEventListener("mouseleave", function () {
            card.style.transform = "translateY(0)";
        });

    });

    // Booking date validation

    const checkIn = document.querySelector(
        'input[name="check_in"]'
    );

    const checkOut = document.querySelector(
        'input[name="check_out"]'
    );

    if (checkIn && checkOut) {

        checkIn.addEventListener("change", function () {
            checkOut.min = checkIn.value;

            if (checkOut.value && checkOut.value <= checkIn.value) {
                checkOut.value = "";
            }
        });

    }

});
