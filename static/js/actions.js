document.onkeydown = keydown;
function keydown(evt){
  if (evt.ctrlKey && evt.keyCode == 32){
    var search = document.getElementById('search');
    search.className = 'open';
    document.getElementById('searchInput').focus();
  } else if (evt.keyCode == 27) {
      var search = document.getElementById('search');
      search.className = '';
      document.getElementById('searchInput').blur();
  }
}    
