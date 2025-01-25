document.addEventListener("DOMContentLoaded", function () {
    const sortSelector = document.getElementById("sort-selector");

    if (sortSelector) {
        sortSelector.addEventListener("change", function () {
            const selectedVal = this.value;
            const currentUrl = new URL(window.location);

            if (selectedVal !== "reset") {
                const [sort, direction] = selectedVal.split("_");
                currentUrl.searchParams.set("sort", sort);
                currentUrl.searchParams.set("direction", direction);
            } else {
                currentUrl.searchParams.delete("sort");
                currentUrl.searchParams.delete("direction");
            }

            window.location.href = currentUrl; // Redirect to the updated URL
        });
    }
});