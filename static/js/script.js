document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const messageBox = document.createElement("div");
    messageBox.style.marginTop = "20px";
    messageBox.style.textAlign = "center";
    form.appendChild(messageBox);

    form.addEventListener("submit", function(event) {
        event.preventDefault(); 

        messageBox.innerText = "Submitting your clothing details...";
        messageBox.style.color = "#3498db";

        setTimeout(() => {
            messageBox.innerText = "Clothing details submitted successfully!";
            messageBox.style.color = "green";
        }, 2000);
    });
});
