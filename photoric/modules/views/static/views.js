/* arrays and object to save checked gallery items */
var checkedAlbums = [];
var checkedImages = [];

/* add album or image to list of checked items */
function checkItem(itemId) {
    var checkbox = document.getElementById(itemId);
    var pos;
    var srcChecked = Flask.url_for('views.static', {'filename': '/images/check-circle-fill.svg'});
    var srcUnchecked = Flask.url_for('views.static', {'filename': '/images/check-circle.svg'});
    if (itemId.indexOf("album") > -1) {
        pos = checkedAlbums.indexOf(itemId);
        if (pos > -1) {
            checkedAlbums.splice(pos, 1);
            checkbox.setAttribute("src", srcUnchecked);
        } else {
            checkedAlbums.push(itemId);
            checkbox.setAttribute("src", srcChecked);
        }
    } else if (itemId.indexOf("image") > -1) {
        pos = checkedImages.indexOf(itemId);
        if (pos > -1) {
            checkedImages.splice(pos, 1);
            checkbox.setAttribute("src", srcUnchecked);
        } else {
            checkedImages.push(itemId);
            checkbox.setAttribute("src", srcChecked);
        }
    }
    if (checkedAlbums.length > 0  || checkedImages.length > 0) {
        document.getElementById("actionbar").style="display: flex;";
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

function treeOpenClose(element) {
    if (element.getAttribute("src").indexOf("plus")) {
        element.setAttribute("src", Flask.url_for('nav.static', {'filename': '/images/dash-square.svg'}));
    } else {
        element.setAttribute("src", Flask.url_for('nav.static', {'filename': '/images/plus-square.svg'}));
    }
}


var albumSwitcher = 1
function collapseAlbum(id) {
    var albumOpener = document.getElementById(id);
    if (albumSwitcher % 2 > 0) {
        albumOpener.title = "open";
    } else {
        albumOpener.title = "close";
    }
    albumSwitcher++;
}

var imageSwitcher = 1
function collapseImage(id) {
    var imageOpener = document.getElementById(id);
    if (imageSwitcher % 2 > 0) {
        imageOpener.title = "open";
    } else {
        imageOpener.title = "close";
    }
    imageSwitcher++;
}