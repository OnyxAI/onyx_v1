
function next(last_menu, new_menu){
  $('.'+last_menu).tapTarget('close');
  $('.'+new_menu).tapTarget('open');
}
