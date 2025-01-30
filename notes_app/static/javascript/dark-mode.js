document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("dark-mode-toggle");
    const body = document.body;
    const featuredImage = document.getElementById("featured-image");

    // Define the images for light and dark mode
    const lightModeImage = "/static/images/philosophers.jpg"; // Light mode image
    const darkModeImage = "/static/images/darkphilosophers.jpg"; // Dark mode image (Add this image to your static/images folder)

    // Function to update the image based on the mode
    function updateImage() {
        if (body.classList.contains("dark-mode")) {
            featuredImage.src = darkModeImage;
        } else {
            featuredImage.src = lightModeImage;
        }
    }

    // Check localStorage for saved theme preference
    if (localStorage.getItem("theme") === "dark") {
        body.classList.add("dark-mode");
        updateImage();
    }

    // Add event listener to toggle dark mode
    toggleButton.addEventListener("click", function () {
        body.classList.toggle("dark-mode");

        // Save user preference
        if (body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
        } else {
            localStorage.setItem("theme", "light");
        }

        updateImage(); // Change the image when toggling
    });
});