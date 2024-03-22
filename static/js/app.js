
    document.getElementById('input-foto').addEventListener('change', function(event) {
        var input = event.target;
        var reader = new FileReader();
        reader.onload = function(){
            var dataURL = reader.result;
            var preview = document.getElementById('preview');
            var img = new Image();
            img.src = dataURL;
            img.style.maxWidth = '200px'; // Ajusta el tamaño máximo de la imagen para que no sea demasiado grande
            preview.innerHTML = ''; // Limpia cualquier imagen previa
            preview.appendChild(img);
        };
        reader.readAsDataURL(input.files[0]);
    });

