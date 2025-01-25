document.addEventListener("DOMContentLoaded", function () {
    const backToTopLink = document.querySelector(".btt-link");

    if (backToTopLink) {
        // Show the button when the user scrolls down
        window.addEventListener("scroll", function () {
            if (window.scrollY > 200) {
                backToTopLink.classList.add("visible");
            } else {
                backToTopLink.classList.remove("visible");
            }
        });

        backToTopLink.addEventListener("click", function (e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });
    }
});
