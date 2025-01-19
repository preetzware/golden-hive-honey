document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed.");

    const desktopSearchIcon = document.getElementById("searchClick"); // Desktop search icon
    const mobileSearchIcon = document.getElementById("mobileSearchIcon"); // Mobile search icon
    const desktopSearchBar = document.getElementById("search-bar"); // Desktop search bar
    const mobileSearchBar = document.getElementById("mobile-search-bar"); // Mobile search bar

    const toggleSearchBar = (searchBar) => {
        if (searchBar) {
            searchBar.classList.toggle("hidden");
            if (!searchBar.classList.contains("hidden")) {
                searchBar.querySelector("input").focus(); // Focus on input if search bar is visible
            }
        }
    };

    // Desktop search icon toggle
    if (desktopSearchIcon && desktopSearchBar) {
        desktopSearchIcon.addEventListener("click", (event) => {
            event.preventDefault();
            toggleSearchBar(desktopSearchBar);
        });
    }

    // Mobile search icon toggle
    if (mobileSearchIcon && mobileSearchBar) {
        mobileSearchIcon.addEventListener("click", (event) => {
            event.preventDefault();
            toggleSearchBar(mobileSearchBar);
        });
    }
});
