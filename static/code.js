var ADD_NEW_GIF_URL = "http://10.16.20.139:5000/gifs/new/";
var LOGIN_URL = "http://10.16.20.139:5000/users/login/";
var REGISTER_URL = "http://10.16.20.139:5000/users/register/";
var QUERY_URL = "http://10.16.20.139:5000/gifs/retrieve/";
var RETRIEVE_HEAD_URL = "http://10.16.20.139:5000/gifs/retrieve/heads/";
var RETRIEVE_TORSO_URL = "http://10.16.20.139:5000/gifs/retrieve/torsos/";

/****************** All pages (base template) *******************/
function remove_self_on_click(element){
    element.remove();
}

function remove_all_elements_matching_to_selector(selector){
    let elements = document.querySelectorAll(selector);  
    elements.forEach(function (item, index){
        item.remove();
    });
}

$("input#toggle_password").click(function(e) {
    var x = document.querySelector("input#password");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
});
/****************************************************************/

/*********************** Add New GIF page ***********************/
function create_new_button_badge(new_keyword){
    let new_badge = document.createElement("button");
    new_badge.type = "button";
    new_badge.classList.add("btn");
    new_badge.classList.add("btn-warning");
    new_badge.innerText = new_keyword.toLowerCase() + " [x]";
    new_badge.onclick = function(){ //on click, remove self
        new_badge.remove();
    }
    return new_badge;
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

//toggle switch
$("input#new_language_toggle").click(function(e) {
    let toggle  = document.querySelector("input#new_language_toggle");
    let new_language_input_box = document.querySelector("input#new_language");
    let existing_sign_languages_select = document.querySelector("select#sign_languages");
    if (toggle.checked) {
        new_language_input_box.removeAttribute('disabled');
        existing_sign_languages_select.setAttribute('disabled', '');
    } else {
        new_language_input_box.setAttribute('disabled', '');
        existing_sign_languages_select.removeAttribute('disabled');
    }
});

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
    remove_all_elements_matching_to_selector("div#badges button");
    this.reset();
});
/****************************************************************/



/************************* Log In page **************************/
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




/************************* Register page **************************/
$("form#register").submit(function(e) {
    //don't redirect
    e.preventDefault();

    //prepare json
    jsonData = {
        "email": document.querySelector("input#email").value,
        "password": document.querySelector("input#password").value
    }

    //POST the data
    $.ajax({
        url: REGISTER_URL,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(jsonData),
        success: function (response) {
            window.location.href = LOGIN_URL;
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



/*********************** Query GIF page *************************/
function prepare_json_data_for_query(){
    
    let sign_language_select = document.querySelector("select#sing_languages");
    let sign_language = sign_language_select.options[sign_language_select.selectedIndex].value;

    let gif_type = 'h';
    if (document.querySelector("input#torso_gif").checked){
        gif_type = 'b';
    }

    let kwords = document.querySelector("input#query_keywords").value.split(/(?:,| )+/);

    jsonData = {
        "sign_language": sign_language,
        "gif_type": gif_type,
        "keywords": kwords
    }

    return jsonData;
}


function prepare_url_for_gif(gif_type, gif_details){
    if (gif_type == 'h'){
        return RETRIEVE_HEAD_URL + gif_details["filename"];
    }

    return RETRIEVE_TORSO_URL + gif_details["filename"];
}

function img_create(src, alt, width, height) {

    let img = document.createElement("img");
    img.setAttribute('src', src);
    img.setAttribute('alt', alt);
    img.setAttribute('height', width);
    img.setAttribute('width', height);

    return img;
}



function display_gifs_in_preview_area(response){

    let gif_preview_area = document.querySelector("div#gif_preview_area");
    response["gif_matches"].forEach( function(gif, index){
        let gif_element = img_create(prepare_url_for_gif(response["gif_type"], gif), gif["filename"], "", "");
        gif_element.classList.add("my-2");
        gif_element.classList.add("mx-2");
        gif_preview_area.appendChild(gif_element)
    });

}

$("form#query_gifs").submit(function(e) {
    //don't redirect
    e.preventDefault();

    //prepare json
    jsonData = prepare_json_data_for_query();

    //POST the data
    $.ajax({
        url: QUERY_URL,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(jsonData),
        success: function (response) {
            remove_all_elements_matching_to_selector("div#gif_preview_area img");
            display_gifs_in_preview_area(response);
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
