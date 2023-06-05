
function validateForm() {
    var password = document.getElementById("password").value;
    var confirm_password = document.getElementById("confirm_password").value;

        if (password !== confirm_password) {
            alert("Password and Confirm Password must match.");
            return false;
        }
        return true;
    }
