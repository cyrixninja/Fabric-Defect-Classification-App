document.addEventListener('DOMContentLoaded', function() {
    console.log("Document loaded, initializing file upload handlers");
    
    // Get elements
    const fileInput = document.getElementById('file');
    const browseButton = document.getElementById('browse-button');
    const analyzeButton = document.getElementById('analyze-button');
    const previewContainer = document.querySelector('.preview-container');
    const uploadContent = document.querySelector('.upload-content');
    const preview = document.getElementById('preview');
    const fileName = document.getElementById('file-name');
    const removeButton = document.getElementById('remove-button');
    const dropArea = document.getElementById('drop-area');
    
    // Debug logging
    console.log("Browse button:", browseButton);
    console.log("File input:", fileInput);
    
    // Connect browse button to file input
    if (browseButton && fileInput) {
        console.log("Setting up browse button click handler");
        browseButton.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("Browse button clicked");
            fileInput.click();
        });
    }
    
    // Handle file selection
    if (fileInput) {
        console.log("Setting up file input change handler");
        fileInput.addEventListener('change', function() {
            console.log("File input changed, files:", fileInput.files);
            if (fileInput.files.length > 0) {
                displayPreview(fileInput.files[0]);
            }
        });
    }
    
    // Handle file preview
    function displayPreview(file) {
        console.log("Displaying preview for file:", file.name);
        if (file) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                console.log("File loaded, updating UI");
                preview.src = e.target.result;
                fileName.textContent = file.name;
                previewContainer.style.display = 'block';
                uploadContent.style.display = 'none';
                analyzeButton.disabled = false;
            }
            
            reader.readAsDataURL(file);
        }
    }
    
    // Remove selected file
    if (removeButton) {
        console.log("Setting up remove button click handler");
        removeButton.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("Remove button clicked");
            fileInput.value = '';
            previewContainer.style.display = 'none';
            uploadContent.style.display = 'block';
            analyzeButton.disabled = true;
        });
    }
    
    // Drag and drop functionality
    if (dropArea) {
        console.log("Setting up drag and drop handlers");
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            dropArea.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, unhighlight, false);
        });
        
        function highlight() {
            console.log("Drag highlight");
            dropArea.classList.add('highlight');
        }
        
        function unhighlight() {
            console.log("Drag unhighlight");
            dropArea.classList.remove('highlight');
        }
        
        dropArea.addEventListener('drop', handleDrop, false);
        
        function handleDrop(e) {
            console.log("File dropped");
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length > 0) {
                console.log("Dropped file:", files[0].name);
                fileInput.files = files;
                displayPreview(files[0]);
            }
        }
    }
});