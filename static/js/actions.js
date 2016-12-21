document.onkeydown = keydown;
function keydown(evt){
  if (evt.ctrlKey){
    var search = document.getElementById('search');
    search.className = 'open';
    document.getElementById('searchInput').focus();
  } else if (evt.keyCode == 27) {
      var search = document.getElementById('search');
      search.className = '';
      document.getElementById('searchInput').blur();
  }
}    
