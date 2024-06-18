document.getElementById('id_ProfileImage').addEventListener('change', function (e) {
    
    let file = e.target.files[0];

    let fileReader = new FileReader();
    fileReader.onload = function() {
        let dataUri = this.result;

        let img = document.getElementById('preview');
        img.src = dataUri;
    }
    
    fileReader.readAsDataURL(file);
});