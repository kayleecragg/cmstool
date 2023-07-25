// Image toggle function
document.getElementById('toggle-images').addEventListener('click', function() {
    var images = document.getElementsByClassName('asset-image');
    for (var i = 0; i < images.length; i++) {
      var display = getComputedStyle(images[i]).display;
      images[i].style.display = display === 'none' ? 'block' : 'none';
    }
  });
  
  // Drag and Drop function
  var assets = document.querySelectorAll('.asset');
  var assetContainer = document.querySelector('.asset-container');
  var pin = document.querySelector('.pin');
  
  pin.addEventListener('dragstart', (e) => {
    e.dataTransfer.setData('text/plain', 'pin');
  });
  
  assets.forEach(asset => {
    asset.addEventListener('dragstart', (e) => {
      e.dataTransfer.setData('text/plain', asset.id);
    });
  
    asset.addEventListener('dragover', (e) => {
      e.preventDefault();
    });
  
    asset.addEventListener('drop', (e) => {
      e.preventDefault();
      var id = e.dataTransfer.getData('text/plain');
      if (id === 'pin') {
        asset.classList.add('pinned');
        assetContainer.insertBefore(asset, assetContainer.firstChild);
      } else {
        var assetDragged = document.getElementById(id);
        assetDragged.classList.remove('pinned');
  
        // Get the position of the asset being dropped onto
        var dropIndex = Array.prototype.indexOf.call(assetContainer.children, asset);
  
        // Insert the dragged asset at the drop position
        assetContainer.insertBefore(assetDragged, assetContainer.children[dropIndex]);
      }
    });
  });
  
  // Time conversion
  function convertTimestampToSydneyTime(timestamp) {
    // Convert timestamp to milliseconds
    var date = new Date(timestamp);
  
    // Format the date in the desired format
    var options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
    var formattedDate = date.toLocaleString('en-US', options);
  
    return formattedDate;
  }
  
  // Get all elements with class "livestart-date"
  var elements = document.querySelectorAll('.livestart-date');
  
  // Iterate over each element
  elements.forEach(function(element) {
    // Get the timestamp from the element's text content
    var timestamp = parseInt(element.textContent);
  
    // Convert timestamp to Sydney time + 12 hours
    var sydneyTimePlus12 = convertTimestampToSydneyTime(timestamp);
  
    // Update the element's text content with the converted time
    element.textContent = sydneyTimePlus12;
  });
  
  // Sort function
  document.getElementById('sort-by-date').addEventListener('click', function() {
    // Convert the NodeList to an Array
    var assetsArray = Array.prototype.slice.call(assets, 0);
  
    assetsArray.sort(function(a, b) {
      var dateA = parseInt(a.querySelector('.livestart-date').textContent);
      var dateB = parseInt(b.querySelector('.livestart-date').textContent);
      return dateA - dateB;
    });
  
    assetsArray.forEach(function(asset) {
      if (!asset.classList.contains('pinned')) {
        assetContainer.appendChild(asset);
      }
    });
  });
