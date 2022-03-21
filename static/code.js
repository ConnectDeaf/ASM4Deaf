$("form#data").submit(function(e) {
    //don't redirect
    e.preventDefault();

    //prepare the data to POST
    var formData = new FormData(this);

    //POST the data
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: formData,
        success: function (data) {
            alert(data)
        },
        error: function (e) {
            alert(e)
        },
        cache: false,
        contentType: false,
        processData: false
    });

    //clear the form
    this.reset();
});
