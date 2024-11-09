document.addEventListener('DOMContentLoaded', function () {
    const steps = document.querySelectorAll('.form-step');
    let currentStep = 0;

    // Show the current step
    function showStep(step) {
        steps.forEach((stepDiv, index) => {
            if (index === step) {
                stepDiv.classList.add('active');
            } else {
                stepDiv.classList.remove('active');
            }
        });
    }

    // Show the next step
    function nextStep() {
        if (currentStep < steps.length - 1) {
            currentStep++;
            showStep(currentStep);
        }
    }

    // Show the previous step
    function prevStep() {
        if (currentStep > 0) {
            currentStep--;
            showStep(currentStep);
        }
    }

    // Attach event listeners to buttons
    document.querySelectorAll('.next-step').forEach(button => {
        button.addEventListener('click', nextStep);
    });

    document.querySelectorAll('.prev-step').forEach(button => {
        button.addEventListener('click', prevStep);
    });

    // Initially show the first step
    showStep(currentStep);
});
