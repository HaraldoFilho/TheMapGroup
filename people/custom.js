function custom() {

  document.title = user_info["name"].concat(" | Photos Map");

  addFavicon();
  addFooter();
  createNavButton();
  createOverlay();

  window.onkeyup = function (event) {
    if (event.keyCode == 27) {
      closeOverlay();
    }
  }

  var avatar= document.createElement("IMG");
  avatar.setAttribute("style", "border-radius: 50%");
  avatar.setAttribute("src", user_info["avatar"]);
  avatar.setAttribute("width", "80px");
  avatar.setAttribute("height", "80px");
  document.getElementById("avatar").appendChild(avatar);

  var member_name = user_info["name"];

  if (member_name.length > 18) {
    member_name = member_name.substring(0, 14).concat("...");
  }

  var member_link = document.createElement("A");
  member_link.setAttribute("id", "member_link");
  member_link.setAttribute("href", user_info["url"]);
  member_link.setAttribute("target", "_blank");
  document.getElementById("user-name").appendChild(member_link);
  document.getElementById("member_link").innerText = member_name;

  if (countries.length > 1) {
    document.getElementById("n-countries").innerText = countries.length.toString().concat(" countries");
  } else {
    document.getElementById("n-countries").innerText = countries.length.toString().concat(" country");
  }

  document.getElementById("n-markers").innerText = user_info["markers"];
  document.getElementById("n-photos").innerText = user_info["photos"];

  countries.sort(function(a,b) {
    var delta = (b[2]-a[2]);
    if (delta == 0) {
      return (b[3]-a[3]);
    }
    return delta;
   });

  for (var i = 0; i < countries.length; i++) {

    var country_code = countries[i][0];

    var bbox_defined = true;

    if (typeof countries_bbox[country_code] === 'undefined') {
      bbox_defined = false;
    }

    var country_name = '';

    if (bbox_defined) {
      country_name = countries_bbox[country_code][0];
    } else {
      country_name = countries[i][1];
    }

    var i_flags = document.createElement("IMG");
    var icon_src = getIconSrc(country_name);
    i_flags.setAttribute("class", "tiny-icon");
    i_flags.setAttribute("src", icon_src);
    document.getElementById("flags").appendChild(i_flags);

    var i_countries = document.createElement("P");
    i_countries.setAttribute("class", "country");
    i_countries.setAttribute("id", country_code);

    if (country_name.length > 15) {
      i_countries.setAttribute("title", country_name);
      country_name = country_name.substring(0, 13).concat("...");
    }

    if (!bbox_defined) {
      i_countries.setAttribute("style", "cursor:not-allowed");
    }

    i_countries.innerText = country_name;
    document.getElementById("countries").appendChild(i_countries);

    var i_places = document.createElement("P");
    i_places.setAttribute("class", "item");
    i_places.innerText = countries[i][2];
    document.getElementById("places").appendChild(i_places);

    var i_places_icon = document.createElement("IMG");
    var icon_src = "../../icons/place.svg";
    i_places_icon.setAttribute("class", "tiny-icon");
    i_places_icon.setAttribute("src", icon_src);
    document.getElementById("place-icon").appendChild(i_places_icon);

    var i_photos = document.createElement("P");
    i_photos.setAttribute("class", "item");
    i_photos.innerText = countries[i][3];
    document.getElementById("photos").appendChild(i_photos);

    var i_photos_icon = document.createElement("IMG");
    var icon_src = "../../icons/photo.svg";
    i_photos_icon.setAttribute("class", "tiny-icon");
    i_photos_icon.setAttribute("src", icon_src);
    document.getElementById("photo-icon").appendChild(i_photos_icon);
  }

  countries.forEach(addListener);

}


// Functions

function addFavicon() {
  var favicon = document.createElement("LINK");
  favicon.setAttribute("rel", "shortcut icon");
  favicon.setAttribute("type", "image/x-icon");
  favicon.setAttribute("href", "../../favicon.ico");
  document.head.append(favicon);
}

function createNavButton() {
  var div_nav_button = document.createElement("DIV");
  div_nav_button.setAttribute("id", "nav-button");
  div_nav_button.setAttribute("class", "nav-button");
  div_nav_button.setAttribute("onclick", "toggleOverlay()");
  div_nav_button.innerHTML = "&#9776";
  document.body.append(div_nav_button);
}

function createOverlay() {

  // User Container
  var div_avatar = document.createElement("DIV");
  div_avatar.setAttribute("id", "avatar");
  div_avatar.setAttribute("class", "avatar");
  var div_user_name = document.createElement("DIV");
  div_user_name.setAttribute("id", "user-name");
  div_user_name.setAttribute("class", "user-name");
  var div_n_countries = document.createElement("DIV");
  div_n_countries.setAttribute("id", "n-countries");
  div_n_countries.setAttribute("class", "n-countries");
  var div_u_place_icon = document.createElement("IMG");
  div_u_place_icon.setAttribute("class", "tiny-icon");
  div_u_place_icon.setAttribute("src", "../../icons/place.svg");
  var div_n_markers = document.createElement("DIV");
  div_n_markers.setAttribute("id", "n-markers");
  div_n_markers.setAttribute("class", "n-markers");
  var div_u_photo_icon = document.createElement("IMG");
  div_u_photo_icon.setAttribute("class", "tiny-icon");
  div_u_photo_icon.setAttribute("src", "../../icons/photo.svg");
  var div_n_photos = document.createElement("DIV");
  div_n_photos.setAttribute("id", "n-photos");
  div_n_photos.setAttribute("class", "n-photos");
  var div_user_container = document.createElement("DIV");
  div_user_container.setAttribute("id", "user-container");
  div_user_container.setAttribute("class", "user-container");
  div_user_container.appendChild(div_avatar);
  div_user_container.appendChild(div_user_name);
  div_user_container.appendChild(div_n_countries);
  div_user_container.appendChild(div_u_place_icon);
  div_user_container.appendChild(div_n_markers);
  div_user_container.appendChild(div_u_photo_icon);
  div_user_container.appendChild(div_n_photos);

  // Countries Container
  var div_flags = document.createElement("DIV");
  div_flags.setAttribute("id", "flags");
  div_flags.setAttribute("class", "flags");
  var div_countries = document.createElement("DIV");
  div_countries.setAttribute("id", "countries");
  div_countries.setAttribute("class", "countries");
  var div_places = document.createElement("DIV");
  div_places.setAttribute("id", "places");
  div_places.setAttribute("class", "places");
  var div_place_icon = document.createElement("DIV");
  div_place_icon.setAttribute("id", "place-icon");
  div_place_icon.setAttribute("class", "place-icon");
  var div_photos = document.createElement("DIV");
  div_photos.setAttribute("id", "photos");
  div_photos.setAttribute("class", "photos");
  var div_photo_icon = document.createElement("DIV");
  div_photo_icon.setAttribute("id", "photo-icon");
  div_photo_icon.setAttribute("class", "photo-icon");
  var div_countries_container = document.createElement("DIV");
  div_countries_container.setAttribute("id", "countries-container");
  div_countries_container.setAttribute("class", "countries-container");
  div_countries_container.appendChild(div_flags);
  div_countries_container.appendChild(div_countries);
  div_countries_container.appendChild(div_places);
  div_countries_container.appendChild(div_place_icon);
  div_countries_container.appendChild(div_photos);
  div_countries_container.appendChild(div_photo_icon);

  // Main container
  var div_main_container = document.createElement("DIV");
  div_main_container.setAttribute("id", "main-container");
  div_main_container.setAttribute("class", "main-container");
  div_main_container.appendChild(div_user_container);
  div_main_container.appendChild(div_countries_container);

  // Overlay
  var div_overlay_content = document.createElement("DIV");
  div_overlay_content.setAttribute("class", "overlay-content");
  div_overlay_content.appendChild(div_main_container);
  var div_overlay = document.createElement("DIV");
  div_overlay.setAttribute("id", "overlay");
  div_overlay.setAttribute("class", "overlay");
  div_overlay.setAttribute("onscroll", "changeUserBackgroundColor()");
  div_overlay.appendChild(div_overlay_content);
  div_overlay.style.width = "0%";

  document.body.append(div_overlay);

}

function toggleOverlay() {
  if (document.getElementById("overlay").style.width == "0%") {
    openOverlay();
  } else {
    closeOverlay();
  }
}

function openOverlay() {
  document.getElementById("overlay").style.width = "400px";
  document.getElementById("menu").style.display = "none";
  document.getElementById("nav-button").style.margin = "60px 0 0 400px";
  fitBoundingBox(current_bbox);
}

function closeOverlay() {
  document.getElementById("overlay").style.width = "0%";
  document.getElementById("menu").style.display = "block";
  document.getElementById("nav-button").style.display = "block";
  document.getElementById("nav-button").style.margin = "60px 0 0 0";
  fitBoundingBox(current_bbox);
}

function getIconSrc(name) {
  return "../../icons/flags/".concat(name.replace(/\s/g, "-").toLowerCase()).concat(".svg");
}

function addListener(country) {
  var country_code = country[0];
  var country_bbox = [];
  var bbox_defined = true;

  if (typeof countries_bbox[country_code] === 'undefined') {
    bbox_defined = false;
  }

  if (bbox_defined) {
    country_bbox = countries_bbox[country_code][1];
  }

  document.getElementById(country_code).addEventListener('click', function() { fitBoundingBox(country_bbox) });

}

function fitBoundingBox(bbox) {

  current_bbox = bbox;

  var overlay_status = document.getElementById("overlay").style.width;

  if (overlay_status == '400px') {
    padding_left = 450;
  } else {
    padding_left = 50;
  }

  map.fitBounds([
    [bbox[0], bbox[1]],
    [bbox[2], bbox[3]]],
    {padding: {top:50, bottom:50, left:padding_left, right:50}}
  );

};

function changeUserBackgroundColor() {
  if (document.getElementById("overlay").scrollTop > 25) {
    document.getElementById("user-container").className = "user-container-black";
    document.getElementById("nav-button").className = "nav-button-black";
  } else {
    document.getElementById("user-container").className = "user-container";
    document.getElementById("nav-button").className = "nav-button";
  }
}

function addFooter() {
  var footer = document.createElement("DIV");
  footer.setAttribute("class", "footer");
  footer.innerHTML = "Map generated by <b>The Map Group</b> on <i><b>Flickr™</b></i>. <a href=\"https://www.flickr.com/groups/the-map-group/\" target=\"_blank\">Get yours</a> by joining the group!";
  document.body.append(footer);
}
