var ADD_NEW_GIF_URL = "http://localhost:5000/gifs/new/"
var LOGIN_URL = "http://localhost:5000/users/login/"

/****************** All pages (base template) *******************/
function remove_self_on_click(element){
    element.remove();
}

function toggle_logging_visibility(){
    let visible_logging_elements = document.querySelectorAll(".visible-menu-item");
    let invisible_logging_elements = document.querySelectorAll(".invisible-menu-item");
    
    visible_logging_elements.forEach(function (item, index){
        item.classList.add("invisible-menu-item")
        item.classList.remove("visible-menu-item")
    });

    invisible_logging_elements.forEach(function (item, index){
        item.classList.add("visible-menu-item")
        item.classList.remove("invisible-menu-item")
    });
};

/****************************************************************/

/*********************** Add New GIF page ***********************/
function create_new_button_badge(new_keyword){
    let new_badge = document.createElement("button");
    new_badge.type = "button";
    new_badge.classList.add("btn");
    new_badge.classList.add("btn-warning");
    new_badge.innerText = new_keyword + " [x]";
    new_badge.onclick = function(){ //on click, remove self
        new_badge.remove();
    }
    return new_badge;
}

function remove_all_keyword_badges(){
    let all_badge_buttons = document.querySelectorAll("div#badges button");  
    all_badge_buttons.forEach(function (item, index){
        item.remove();
    });
}

function get_keywords_csv(){
    let all_badge_buttons = document.querySelectorAll("div#badges button");  
    let keyword_csv_str = "";  
    all_badge_buttons.forEach(function (item, index){
        keyword_csv_str += item.innerText.slice(0, -4) + ((index < (all_badge_buttons.length-1)) ? ',' : '');
    });
    return keyword_csv_str;
}

function prepare_keywords_aux_field(){
    let keywords = document.querySelector("input#keywords");
    keywords.value = get_keywords_csv();

    return keywords.value;
}

//adding badges with the entered keywords
$("button#add_badge").click(function(e) {

    //get new keyword
    let new_keyword_element = document.querySelector("input#new_keyword");
    let new_keyword = new_keyword_element.value;
    if (new_keyword == "") return;
    
    
    //reset new_keyword input field
    new_keyword_element.value = "";
    new_keyword_element.required = false;


    //remove "placeholding" span
    let placeholding_span = document.querySelector("div#badges p");
    if (placeholding_span){
        placeholding_span.remove();
    };
    
    //create and add a new badge with the keyword
    let badges_div = document.querySelector("div#badges");
    badges_div.appendChild(create_new_button_badge(new_keyword));
});

//submitting the form
$("form#new_gif").submit(function(e) {
    //don't redirect
    e.preventDefault();

    //prepare the auxiliary input field's value
    if (prepare_keywords_aux_field() == ""){
        alert("You cannot submit a GIF with no keywords! Please add at least one.");
        return;
    }


    //prepare the data to POST
    var formData = new FormData(this);

    //POST the data
    $.ajax({
        url: ADD_NEW_GIF_URL,
        type: 'POST',
        data: formData,
        success: function (response) {
            alert(response);
        },
        error: function(response) {
            alert(response.responseText);
        },
        cache: false,
        contentType: false,
        processData: false
    });

    //reset the form and badges area
    remove_all_keyword_badges();
    this.reset();
});
/****************************************************************/



/************************* Log In page **************************/
$("input#toggle_password").click(function(e) {
    var x = document.querySelector("input#password");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
});

$("form#login").submit(function(e) {
    //don't redirect
    e.preventDefault();

    //prepare json
    jsonData = {
        "email": document.querySelector("input#email").value,
        "password": document.querySelector("input#password").value
    }

    //POST the data
    $.ajax({
        url: LOGIN_URL,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(jsonData),
        success: function (response) {
            window.location.href = ADD_NEW_GIF_URL;
        },
        error: function(response) {
            alert(response.responseText);
        },
        cache: false,
        processData: false
    });
    
    //reset the form
    this.reset();

});

/****************************************************************/