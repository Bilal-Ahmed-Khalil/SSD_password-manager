// Display modal centered with dim background
function displayModal(id) {
    const modalWrapper = document.querySelector(".modals-wrapper");
    const modal = document.getElementById(id);

    // Hide all other modals
    document.querySelectorAll(".modal").forEach(m => m.style.display = "none");

    // Show modal and overlay
    modalWrapper.style.display = "flex";
    modal.style.display = "flex";

    // Disable page scroll
    document.body.style.overflow = "hidden";

    // Close modal on 'X' click
    const close = document.getElementById("close-modal");
    close.onclick = () => {
        modalWrapper.style.display = "none";
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    };
}

// Copy to clipboard functionality
const copies = document.querySelectorAll(".copy");
copies.forEach(copy => {
    copy.onclick = () => {
        let elemntToCopy = copy.previousElementSibling;
        elemntToCopy.select();
        document.execCommand("copy");
    };
});
