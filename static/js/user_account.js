$(document).ready(function(){
    let account_img_input = $('.change-account-image-input');
    account_img_input.on('input', function(){
        let file = account_img_input[0].files[0];
        if(!file.type.includes('image')){
            alert('not an image');
        } else if(file.size > 1048576) {
            alert('image too large');
        } else {
            $('#image-upload-form').submit();
        }
    })

    // TODO: Remove after S3 implementation for media
    account_img_input.click(function(event){
        event.preventDefault();
        alert("This feature is currently still in development!");
    })
})