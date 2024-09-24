// function handleMenuClick(event) {
//     document.querySelectorAll('footer.curved-menu nav.menu ul li').forEach(item => {
//         item.classList.remove('active');
//     });
//     event.currentTarget.classList.add('active');
// }

// document.querySelectorAll('footer.curved-menu nav.menu ul li').forEach(item => {
//     item.addEventListener('click', handleMenuClick);
// });

// File input handling for uploading files
const fileInput = document.getElementById('file-input');
const uploadFilesImage = document.getElementById('upload-files');
const confirmationMessage = document.getElementById('confirmation-message');

// When the "Upload Files" image is clicked, trigger the file input
uploadFilesImage.addEventListener('click', (event) => {
    event.preventDefault();
    fileInput.click(); // Trigger file input click
});

// Handle file selection
fileInput.addEventListener('change', (event) => {
    const files = event.target.files;
    if (files.length > 0) {
        console.log('Files selected:', files);
        // Simulate file upload and show confirmation
        confirmationMessage.style.display = 'block';
        setTimeout(() => {
            confirmationMessage.style.display = 'none';
        }, 3000); // Hide after 3 seconds
    }
});

// Camera input handling
const cameraInput = document.getElementById('camera-input');
const cameraClickImage = document.getElementById('camera-click');

// When the "Camera" image is clicked, trigger the camera input
cameraClickImage.addEventListener('click', (event) => {
    event.preventDefault();
    cameraInput.click(); // Trigger camera input click
});

// Handle camera photo capture
cameraInput.addEventListener('change', (event) => {
    const photo = event.target.files[0];
    if (photo) {
        console.log('Photo captured:', photo);
    }
});
