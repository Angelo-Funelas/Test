
document.addEventListener('click', event => {
  clicktarget = event.target
  if (clicktarget.className == 'createclass') {
    $('.createclass-teacher-form').fadeIn(100);
  }

  if (clicktarget.className == 'close-classroom-new-form') {
    $('.createclass-teacher-form').fadeOut(100);
  }

  if (clicktarget.className == 'delete-class') {
    $('.deleteclass-teacher-form').fadeIn(100);
    document.querySelector('.deleteclass-teacher-form').style.display = "block";
  }

  if (clicktarget.dataset.ab == 'close-classroom-delete-form') {
    $('.deleteclass-teacher-form').fadeOut(100);
  }

  if (clicktarget.className == 'make_ann_input_gate') {
    $('.make_announcement_div').fadeIn(100);
    document.querySelector('.make_announcement_div').style.display = "block";
  }

  if (clicktarget.dataset.ae == 'close_ann_input_gate') {
    $('.make_announcement_div').fadeOut(100);

  }

  if (clicktarget.className == 'dim-form') {
    $('.createclass-teacher-form').fadeOut(100);
    $('.deleteclass-teacher-form').fadeOut(100);
    $('.make_announcement_div').fadeOut(100);
    $('.create_poll_block').fadeOut(100);
  }


});
