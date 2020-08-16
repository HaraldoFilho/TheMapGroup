function custom() {

  document.title = "The Map Group | Photos Map";

  addFavicon();
  createOverlay();
  createNavButton();
  fitBoundingBox(current_bbox);

  window.onkeyup = function (event) {
    if (event.keyCode == 27) {
      closeOverlay();
    }
  }

  var group_avatar = document.createElement("IMG");
  group_avatar.setAttribute("src", "map.png");
  group_avatar.setAttribute("width", "80px");
  group_avatar.setAttribute("height", "80px");
  document.getElementById("group-avatar").appendChild(group_avatar);

  var group_name = "The Map Group";
  var group_url = "https://www.flickr.com/groups/the-map-group/";

  var group_link = document.createElement("A");
  group_link.setAttribute("id", "group_link");
  group_link.setAttribute("href", group_url);
  group_link.setAttribute("target", "_blank");
  document.getElementById("group-name").appendChild(group_link);
  document.getElementById("group_link").innerText = group_name;

  document.getElementById("n-members").innerText = members.length.toString().concat(" members");

  document.getElementById("n-markers").innerText = locations.length.toString();
  var n_photos = 0;
  for (var i = 0; i < locations.length; i++) {
    n_photos = n_photos + locations[i][2];
  }
  document.getElementById("n-photos").innerText = n_photos;

  members.reverse();

  for (var i = 0; i < members.length; i++) {

    var member_name = members[i][2];

    var i_members_avatar = document.createElement("IMG");
    var icon_src = members[i][3];
    i_members_avatar.setAttribute("width", "16px");
    i_members_avatar.setAttribute("height", "16px");
    i_members_avatar.setAttribute("style", "border-radius: 50%");
    i_members_avatar.setAttribute("class", "tiny-icon");
    i_members_avatar.setAttribute("src", icon_src);
    document.getElementById("members-avatar").appendChild(i_members_avatar);

    var i_members = document.createElement("P");
    i_members.setAttribute("class", "member");
    i_members.setAttribute("id", members[i][0]);

    if (member_name.length > 12) {
      i_members.setAttribute("title", member_name);
      member_name = member_name.substring(0, 10).concat("...");
    }

    i_members.innerText = member_name;
    document.getElementById("members").appendChild(i_members);

    var i_places = document.createElement("P");
    i_places.setAttribute("class", "item");
    i_places.innerText = members[i][4];
    document.getElementById("places").appendChild(i_places);

    var i_places_icon = document.createElement("IMG");
    var icon_src = "icons/place.svg";
    i_places_icon.setAttribute("class", "tiny-icon");
    i_places_icon.setAttribute("src", icon_src);
    document.getElementById("place-icon").appendChild(i_places_icon);

    var i_photos = document.createElement("P");
    i_photos.setAttribute("class", "item");
    i_photos.innerText = members[i][5];
    document.getElementById("photos").appendChild(i_photos);

    var i_photos_icon = document.createElement("IMG");
    var icon_src = "icons/photo.svg";
    i_photos_icon.setAttribute("class", "tiny-icon");
    i_photos_icon.setAttribute("src", icon_src);
    document.getElementById("photo-icon").appendChild(i_photos_icon);
  }

  members.forEach(addListener);

}


// Functions

function addFavicon() {
  var favicon = document.createElement("LINK");
  favicon.setAttribute("rel", "shortcut icon");
  favicon.setAttribute("type", "image/x-icon");
  favicon.setAttribute("href", "favicon.ico");
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

  // Group Container
  var div_group_avatar = document.createElement("DIV");
  div_group_avatar.setAttribute("id", "group-avatar");
  div_group_avatar.setAttribute("class", "group-avatar");
  var div_group_name = document.createElement("DIV");
  div_group_name.setAttribute("id", "group-name");
  div_group_name.setAttribute("class", "group-name");
  var div_n_members = document.createElement("DIV");
  div_n_members.setAttribute("id", "n-members");
  div_n_members.setAttribute("class", "n-members");
  var div_u_place_icon = document.createElement("IMG");
  div_u_place_icon.setAttribute("class", "tiny-icon");
  div_u_place_icon.setAttribute("src", "icons/place.svg");
  var div_n_markers = document.createElement("DIV");
  div_n_markers.setAttribute("id", "n-markers");
  div_n_markers.setAttribute("class", "n-markers");
  var div_u_photo_icon = document.createElement("IMG");
  div_u_photo_icon.setAttribute("class", "tiny-icon");
  div_u_photo_icon.setAttribute("src", "icons/photo.svg");
  var div_n_photos = document.createElement("DIV");
  div_n_photos.setAttribute("id", "n-photos");
  div_n_photos.setAttribute("class", "n-photos");
  var div_group_container = document.createElement("DIV");
  div_group_container.setAttribute("id", "group-container");
  div_group_container.setAttribute("class", "group-container");
  div_group_container.appendChild(div_group_avatar);
  div_group_container.appendChild(div_group_name);
  div_group_container.appendChild(div_n_members);
  div_group_container.appendChild(div_u_place_icon);
  div_group_container.appendChild(div_n_markers);
  div_group_container.appendChild(div_u_photo_icon);
  div_group_container.appendChild(div_n_photos);

  // Members Container
  var div_members_avatar = document.createElement("DIV");
  div_members_avatar.setAttribute("id", "members-avatar");
  div_members_avatar.setAttribute("class", "members-avatar");
  var div_members = document.createElement("DIV");
  div_members.setAttribute("id", "members");
  div_members.setAttribute("class", "members");
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
  var div_members_container = document.createElement("DIV");
  div_members_container.setAttribute("id", "members-container");
  div_members_container.setAttribute("class", "members-container");
  div_members_container.appendChild(div_members_avatar);
  div_members_container.appendChild(div_members);
  div_members_container.appendChild(div_places);
  div_members_container.appendChild(div_place_icon);
  div_members_container.appendChild(div_photos);
  div_members_container.appendChild(div_photo_icon);

  // Main container
  var div_main_container = document.createElement("DIV");
  div_main_container.setAttribute("id", "main-container");
  div_main_container.setAttribute("class", "main-container");
  div_main_container.appendChild(div_group_container);
  div_main_container.appendChild(div_members_container);

  // Overlay
  var div_overlay_content = document.createElement("DIV");
  div_overlay_content.setAttribute("class", "overlay-content");
  div_overlay_content.appendChild(div_main_container);
  var div_overlay = document.createElement("DIV");
  div_overlay.setAttribute("id", "overlay");
  div_overlay.setAttribute("class", "overlay");
  div_overlay.setAttribute("onscroll", "changeGroupBackgroundColor()");
  div_overlay.appendChild(div_overlay_content);
  div_overlay.style.width = "400px";

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

function addListener(member) {
  var member_url = "https://the-map-group.pictures/people/".concat(member[1]);
  document.getElementById(member[0]).addEventListener('click', function() { window.location.href = member_url });
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

function changeGroupBackgroundColor() {
  if (document.getElementById("overlay").scrollTop > 25) {
    document.getElementById("group-container").className = "group-container-black";
    document.getElementById("nav-button").className = "nav-button-black";
  } else {
    document.getElementById("group-container").className = "group-container";
    document.getElementById("nav-button").className = "nav-button";
  }
}
