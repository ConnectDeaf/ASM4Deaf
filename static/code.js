var LOGIN_URL = "http://172.20.227.205:5000/users/login/";
var REGISTER_URL = "http://172.20.227.205:5000/users/register/";
var REMOVE_USER_URL = "http://172.20.227.205:5000/users/remove/";
var VERIFY_USER_URL = "http://172.20.227.205:5000/users/verify/";

var ADD_NEW_VIDEO_URL = "http://172.20.227.205:5000/media/videos/new/";
var QUERY_VIDEO_URL = "http://172.20.227.205:5000/media/videos/retrieve/";
var RETRIEVE_VIDEO_ORIGINAL_URL = "http://172.20.227.205:5000/media/videos/retrieve/original/";
var RETRIEVE_VIDEO_THUMBNAIL_URL = "http://172.20.227.205:5000/media/videos/retrieve/thumbnail/";

var ADD_NEW_IMAGE_URL = "http://172.20.227.205:5000/media/images/new/";
var QUERY_IMAGE_URL = "http://172.20.227.205:5000/media/images/new/";
var RETRIEVE_IMAGE_URL = "http://172.20.227.205:5000/media/images/new/";


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
        url: ADD_NEW_VIDEO_URL,
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
            window.location.href = ADD_NEW_VIDEO_URL;
        },
        error: function(response) {
            console.log(response);
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
function prepare_json_data_for_query_page(){
    
    let sign_language_select = document.querySelector("select#sing_languages");
    let sign_language = sign_language_select.options[sign_language_select.selectedIndex].value;

    let kwords = document.querySelector("input#query_keywords").value.split(/(?:,| )+/);

    jsonData = {
        "sign_language": sign_language,
        "keywords": kwords
    }

    return jsonData;
}


function video_create(src, alt, width, height, id) {

    let video = document.createElement("video");
    video.setAttribute('src', src);
    video.setAttribute('alt', alt);
    video.setAttribute('height', height);
    video.setAttribute('width', width);
    video.setAttribute('id', id);
    video.autoplay = false;
    video.controls = true;

    return video;
}


function display_videos_in_preview_area(response){

    let gif_preview_area = document.querySelector("div#gif_preview_area");
    response["gif_matches"].forEach( function(gif, index){
        console.log(RETRIEVE_VIDEO_ORIGINAL_URL+gif["filename"])
        let gif_element = video_create(RETRIEVE_VIDEO_ORIGINAL_URL+gif["filename"], "", "300", "350", gif["id"]);
        gif_element.classList.add("my-2");
        gif_element.classList.add("mx-2");
        gif_preview_area.appendChild(gif_element)
    });

}

$("form#query_gifs").submit(function(e) {
    //don't redirect
    e.preventDefault();

    //prepare json
    jsonData = prepare_json_data_for_query_page();

    //POST the data
    $.ajax({
        url: QUERY_VIDEO_URL,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(jsonData),
        success: function (response) {
            remove_all_elements_matching_to_selector("div#gif_preview_area img");
            display_videos_in_preview_area(response);
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


/********************** Manage Users page ***********************/
function extract_user_email_from_element(element){
    return element.getAttribute('email');
}

function extract_user_id_from_element(element){
    return element.getAttribute('user_id');
}

function prepare_json_data_for_user(remove_button){
    return {"user_id" : extract_user_id_from_element(remove_button)};
}

function remove_user_from_table(user_id){
    console.log(user_id);
    let table_row_selector = "tr#table_row_" + user_id;
    remove_self_on_click(document.querySelector(table_row_selector));
}

function turn_pending_badge_to_verification_badge(user_id){
    let badge = document.querySelector("span.badge#badge_"+user_id);
    badge.classList.add("bg-success");
    badge.classList.remove("bg-secondary");
    badge.innerText = "Verified";
}

function hide_verify_buttonlink(user_id){
    let buttonlink = document.querySelector("button.verify-button#verify_"+user_id);
    buttonlink.classList.add("invisible");
}

$("button.remove-button").click(function() {
   
    let button = this;

    //prepare json
    jsonData = prepare_json_data_for_user(button);

    //PUT the data
    $.ajax({
        url: REMOVE_USER_URL + extract_user_email_from_element(button),
        type: 'DELETE',
        contentType: 'application/json',
        data: JSON.stringify(jsonData),
        success: function (response) {
            let user_id = extract_user_id_from_element(button);
            remove_user_from_table(user_id);
            alert(response);
        },
        error: function(response) {
            alert(response.responseText);
        },
        cache: false,
        processData: false
    });

});

$("button.verify-button").click(function() {
   
    let button = this;

    //prepare json
    jsonData = prepare_json_data_for_user(button);

    //PUT the data
    $.ajax({
        url: VERIFY_USER_URL + extract_user_email_from_element(button),
        type: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(jsonData),
        success: function (response) {
            let user_id = extract_user_id_from_element(button);
            turn_pending_badge_to_verification_badge(user_id);
            hide_verify_buttonlink(user_id);
            alert(response);
        },
        error: function(response) {
            alert(response.responseText);
        },
        cache: false,
        processData: false
    });

});
/****************************************************************/



/********************** Add New Image page **********************/
//submitting the form
$("form#new_image").submit(function(e) {
    //don't redirect
    e.preventDefault();

    //prepare the data to POST
    var formData = new FormData(this);

    //POST the data
    $.ajax({
        url: ADD_NEW_IMAGE_URL,
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

    this.reset();
});
/****************************************************************/


/******************** Preview All Images page *******************/


/****************************************************************/