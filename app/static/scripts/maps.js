/**
 * Creates a new marker and adds it to a group
 * @param {H.map.Group} group       The group holding the new marker
 * @param {H.geo.Point} coordinate  The location of the marker
 * @param {String} html             Data associated with the marker
 */
function addMarkerToGroup(group, coordinate, html) {
    var marker = new H.map.Marker(coordinate, { volatility: true });
    marker.draggable = true;

    // add custom data to the marker
    marker.setData(html);
    group.addObject(marker);

    // disable the default draggability of the underlying map
    // and calculate the offset between mouse and target's position
    // when starting to drag a marker object:
    map.addEventListener('dragstart', function (ev) {
        var target = ev.target,
            pointer = ev.currentPointer;
        if (target instanceof H.map.Marker) {
            var targetPosition = map.geoToScreen(target.getGeometry());
            target['offset'] = new H.math.Point(pointer.viewportX - targetPosition.x, pointer.viewportY - targetPosition.y);
            behavior.disable();
        }
    }, false);

    // re-enable the default draggability of the underlying map
    // when dragging has completed
    map.addEventListener('dragend', function (ev) {
        var target = ev.target;
        if (target instanceof H.map.Marker) {
            behavior.enable();
        }
    }, false);

    // Listen to the drag event and move the position of the marker
    // as necessary
    map.addEventListener('drag', function (ev) {
        var target = ev.target,
            pointer = ev.currentPointer;
        if (target instanceof H.map.Marker) {
            target.setGeometry(map.screenToGeo(pointer.viewportX - target['offset'].x, pointer.viewportY - target['offset'].y));
        }
    }, false);
}

function saveMarker(element) {
    console.log("SENDING")
    var socket = io.connect("http://127.0.0.1:5000/");

    console.log(element)

    socket.emit('my_event', "hello");
}

/**
 * Add two markers showing the position of Liverpool and Manchester City football clubs.
 * Clicking on a marker opens an infobubble which holds HTML content related to the marker.
 * @param {H.Map} map A HERE Map instance within the application
 */
function addInfoBubble(map) {

    map.addObject(globalGroup);

    // add 'tap' event listener, that opens info bubble, to the group
    globalGroup.addEventListener('tap', function (evt) {
        // event target is the marker itself, group is a parent event target
        // for all objects that it contains
        var bubble = new H.ui.InfoBubble(evt.target.getGeometry(), {
            // read custom data
            content: evt.target.getData()
        });
        // show info bubble
        ui.addBubble(bubble);
    }, false);

    addMarkerToGroup(globalGroup, { lat: 51.380741, lng: -2.360147 },
        `
        <div class="info-bubble">
        <form action="http://localhost:5000/upload" enctype="multipart/form-data" method="POST">
            <input name="input-title" type="text" placeholder="Title">
            <textarea name="input-desc" type="text" placeholder="Description"></textarea>
            <div class="image-upload">
                <label for="fileInput">
                    <img class="btn-upload" src="../static/images/upload.png">
                </label>
            </div>
            <input type="file" name="pic" id="fileInput">
            <input id="submit-to-socket" type="submit" value="Save">
        </form>
    </div>
        `
    );
}

/**
 * Adds context menus for the map and the created objects.
 * Context menu items can be different depending on the target.
 * That is why in this context menu on the map shows default items as well as
 * the "Add circle", whereas context menu on the circle itself shows the "Remove circle".
 *
 * @param {H.Map} map Reference to initialized map object
 */
function addContextMenus(map) {
    // First we need to subscribe to the "contextmenu" event on the map
    map.addEventListener('contextmenu', function (e) {
        // As we already handle contextmenu event callback on circle object,
        // we don't do anything if target is different than the map.
        if (e.target !== map) {
            return;
        }

        // "contextmenu" event might be triggered not only by a pointer,
        // but a keyboard button as well. That's why ContextMenuEvent
        // doesn't have a "currentPointer" property.
        // Instead it has "viewportX" and "viewportY" properties
        // for the associates position.

        // Get geo coordinates from the screen coordinates.
        var coord = map.screenToGeo(e.viewportX, e.viewportY);

        // In order to add menu items, you have to push them to the "items"
        // property of the event object. That has to be done synchronously, otherwise
        // the ui component will not contain them. However you can change the menu entry
        // text asynchronously.
        e.items.push(
            // Create a menu item, that has only a label,
            // which displays the current coordinates.
            new H.util.ContextItem({
                label: [
                    Math.abs(coord.lat.toFixed(4)) + ((coord.lat > 0) ? 'N' : 'S'),
                    Math.abs(coord.lng.toFixed(4)) + ((coord.lng > 0) ? 'E' : 'W')
                ].join(' ')
            }),
            // Create an item, that will change the map center when clicking on it.
            new H.util.ContextItem({
                label: 'Center map here',
                callback: function () {
                    map.setCenter(coord, true);
                }
            }),
            // It is possible to add a seperator between items in order to logically group them.
            H.util.ContextItem.SEPARATOR,
            // This menu item will add a new circle to the map
            new H.util.ContextItem({
                label: 'New memory',
                callback: newMarker.bind(map, coord)
            })
        );
    });
}

/**
 * Adds a marker which has a context menu item to remove itself.
 *
 * @this H.Map
 * @param {H.geo.Point} coord Circle center coordinates
 */
function newMarker(coord) {
    addMarkerToGroup(globalGroup, coord,
        `
        <div class="info-bubble">
        <form action="http://localhost:5000/upload" enctype="multipart/form-data" method="POST">
            <input name="input-title" type="text" placeholder="Title">
            <textarea name="input-desc" type="text" placeholder="Description"></textarea>
            <div class="image-upload">
                <label for="fileInput">
                    <img class="btn-upload" src="../static/images/upload.png">
                </label>
            </div>
            <input type="file" name="pic" id="fileInput">
            <input type="submit" value="Save">
        </form>
        <button id="click-me">Test me</button>
    </div>
        `
    );
}

function importMarker(title, description, lat, long) {
    addMarkerToGroup(globalGroup, { lat: 51.380741, lng: -2.360147 },

        '<div>' + title + '</div>' +
        '</div><img width=200 height=200 src="../static/images/test.jpeg"></img></div>'

    );

}

/**
 * Adds a circle which has a context menu item to remove itself.
 *
 * @this H.Map
 * @param {H.geo.Point} coord Circle center coordinates
 */
function addCircle(coord) {
    // Create a new circle object
    var circle = new H.map.Circle(coord, 5000),
        map = this;

    // Subscribe to the "contextmenu" eventas we did for the map.
    circle.addEventListener('contextmenu', function (e) {
        // Add another menu item,
        // that will be visible only when clicking on this object.
        //
        // New item doesn't replace items, which are added by the map.
        // So we may want to add a separator to between them.
        e.items.push(
            new H.util.ContextItem({
                label: 'Remove',
                callback: function () {
                    map.removeObject(circle);
                }
            })
        );
    });

    // Make the circle visible, by adding it to the map
    map.addObject(circle);
}


// init map info

var platform = new H.service.Platform({
    'apikey': 'Ba5hywP2illU3WwuJO3dz9cZFjbLyyaWPcRsJZiqGgw'
});

var defaultLayers = platform.createDefaultLayers();

var map = new H.Map(document.getElementById('map-container'), defaultLayers.vector.normal.map, {
    // Barcelona location
    center: new H.geo.Point(51.380741, -2.360147),
    zoom: 14,
    pixelRatio: window.devicePixelRatio || 1
});

window.addEventListener('resize', () => map.getViewPort().resize());
// Behavior implements default interactions for pan/zoom 
var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));
var ui = H.ui.UI.createDefault(map, defaultLayers);



// demo add things to map
var globalGroup = new H.map.Group();

// add bubble
addInfoBubble(map);
addContextMenus(map);

//#00b7ff


$(document).ready(function () {
    var socket = io.connect("http://127.0.0.1:5000/");

    // socket event listeners
    $('#test-button').on('click', function () {
        console.log("Hi")
        socket.emit('my_event', "hello");
    });

    socket.on('connect', function () {
        console.log('joined');
        socket.emit('joined');
    });



    socket.on('receiveMarkers', function (data) {
        console.log("Received")
        console.log(data);
        for (const [id, marker] of Object.entries(data)) {
            console.log()
            importMarker(marker.title, marker.description, marker.lat, marker.long);
        }

    });

});