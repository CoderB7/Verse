const otpInputs = document.querySelectorAll('.otp-input');

otpInputs.forEach((input, index) => {
  input.addEventListener('input', () => {
    if (input.value.length === 1 && index < otpInputs.length - 1) {
      otpInputs[index + 1].focus();
    }
  });

  input.addEventListener('keydown', (event) => {
    if (event.key === 'Backspace' && index > 0) {
      otpInputs[index - 1].focus();
    }
  });
});

document.getElementById('otp-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    // Clear any previous error messages
    const errorMessage = document.getElementById('error-message');
    errorMessage.style.display = 'none';
    errorMessage.textContent = '';
  
    let isValid = true;
    const usernameInput = document.getElementById('username-input');
    const otpInputs = document.querySelectorAll('.otp-input');
    const otpValues = Array.from(otpInputs).map(input => input.value).join('');
  
    // Check if username is filled
    if (usernameInput.value.trim() === '') {
        isValid = false;
        errorMessage.style.display = 'block';
        errorMessage.textContent = 'Username is required.';
    }
  
    // Check if OTP is fully entered
    if (otpValues.length < 6) {
        isValid = false;
        errorMessage.style.display = 'block';
        errorMessage.textContent = 'Please enter the full OTP.';
    }

    if(isValid){
      let usernameValue = usernameInput.value;
      let otpValue = '';


      otpInputs.forEach(input => {
        otpValue += input.value;
      });
    
      // Now otpValue contains the combined OTP value
      console.log("OTP:", otpValue);
      console.log("Username:", usernameValue);
      var csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    
      fetch('/bot/otp-login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,  // Ensure you include CSRF token for Django
        },
        body: JSON.stringify({ otp: otpValue, username: usernameValue })
      })
      .then(response => {
        if(response.ok) {
          console.log(response.ok);
          window.location.href = '/dashboard/channels/';
        } else {
          return response.json().then(data => {
            console.error("Error:", data.message);
            // Display error message to the user
            alert(data.message);
          });
        }
      })
        
      .then(data => {
        console.log('Success:', data);
        // Handle success (e.g., redirect to another page, display a message, etc.)
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    }
    
     
  });



  
