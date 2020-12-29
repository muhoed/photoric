/* arrays and object to save checked gallery items */
var checkedAlbums = [];
var checkedImages = [];

var checkedItems = {
        albums:checkedAlbums,
        images:checkedImages
};

/* add gallery items to checked lists */
function checkItem(itemId) {
    var checkbox = document.getElementById(itemId);
    var checkboxName = checkbox.getAttribute("name");
    var checkboxSrc = checkbox.getAttribute("src");
    var pos;
    if (checkboxSrc.indexOf("-fill")) {
        if (checkboxName.indexOf("album-") > -1) {
            pos = checkedAlbums.indexOf(itemId);
            checkedAlbums.splice(pos);
        } else if (checkboxName.indexOf("image-") > -1) {
            pos = checkedImages.indexOf(itemId);
            checkedImages.splice(pos);
        }
        checkbox.src = Flask.url_for('views.static', {'filename': '/images/check-circle.svg'});
    }
    if (checkboxSrc.indexOf("-fill") == -1) {
        if (checkboxName.indexOf("album-") > -1) {
            checkedAlbums.push(itemId);
        } else if (checkboxName.indexOf("image-") > -1) {
            checkedImages.push(itemId);
        }
        checkbox.src = Flask.url_for('views.static', {'filename': '/images/check-circle-fill.svg'});
    }
    if (checkedItems.albums[0] || checkedItems.images[0]) {
        document.getElementById("actionbar").style="display: block;";
    } else {
        document.getElementById("actionbar").style="display: none;";
    }
}

/*
function addToAlbum(itemId, checkFunction) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        checkFunction(itemId);
        }
    };
    xhttp.open("POST", "{{ url_for(target, item_id=itemId) }}");
    xhttp.send();
}
*/