function openProfileDropdown() {
    let profileFrame = document.getElementById("profileDropdown");

    if (!profileFrame) {
        profileFrame = document.createElement("iframe");
        profileFrame.id = "profileDropdown";
        profileFrame.src = "/profile"; // Adjust if needed
        profileFrame.style.position = "absolute";
        profileFrame.style.top = "50px"; // Adjust as needed
        profileFrame.style.right = "10px";
        profileFrame.style.width = "200px";
        profileFrame.style.height = "auto";
        profileFrame.style.border = "none";
        profileFrame.style.zIndex = "1000";
        document.body.appendChild(profileFrame);
    } else {
        profileFrame.remove(); // Close if already open
    }
}

// Close the dropdown when clicking outside
window.addEventListener("click", function(event) {
    let profileFrame = document.getElementById("profileDropdown");
    if (profileFrame && !event.target.closest(".profile-icon, #profileDropdown")) {
        profileFrame.remove();
    }
});
