// Handle model selection
document.querySelectorAll('.model-option').forEach(option => {
    option.addEventListener('click', function() {
        // Remove selected class from all options
        document.querySelectorAll('.model-option').forEach(opt => {
            opt.classList.remove('selected');
            opt.querySelector('input[type="radio"]').checked = false;
        });
        
        // Add selected class to clicked option
        this.classList.add('selected');
        this.querySelector('input[type="radio"]').checked = true;
        
        // Update hidden input
        document.getElementById('selectedModel').value = this.dataset.model;
    });
});

// Handle form submission with loading state
document.getElementById('queryForm').addEventListener('submit', function() {
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    
    submitBtn.disabled = true;
    btnText.innerHTML = '<span class="loading"></span>Procesando...';
});

// Set initial selected model based on server value
const currentModel = "{{ model or 'gemini' }}";
const currentOption = document.querySelector(`[data-model="${currentModel}"]`);
if (currentOption) {
    document.querySelectorAll('.model-option').forEach(opt => {
        opt.classList.remove('selected');
        opt.querySelector('input[type="radio"]').checked = false;
    });
    currentOption.classList.add('selected');
    currentOption.querySelector('input[type="radio"]').checked = true;
}