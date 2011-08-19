// Based on http://edward.oconnor.cx/2009/08/presentation.js
var Presentation = function() {
  var slides = null;
  var current_slide = 0;
  var num_slides = 0;

  function set_current_slide(index) {
    current_slide = index;

    var slide = $(slides.get(index));

    slides.not(slide).hide();
    
    // Check if feature slide is about is supported by browser
    var feature = slide.attr('h5:feature');
    browser_support_feature(feature);
    
    slide.show();

    // Update hash if this slide has an @id
    var id = slide.attr('id');
    if (id) {
      location.hash = id;
    }
  }

  function set_slide(offset) {
    var index = current_slide + offset;
    if (index < 0) index = 0;
    if (index > (num_slides-1)) index = (num_slides-1);
    set_current_slide(index);
  }

  function previous_slide() {
    set_slide(-1);
    return false;
  }

  function next_slide() {
    set_slide(1);
    return false;
  }

  // Run through the slides automatically, switching every 15 seconds.
  function ignite() {
    $('#ignite').hide();
    setInterval(next_slide, 15*1000);
    return false;
  }

  function handle_keys(event) {
    /* Skip events with modifier keys */
    if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) {
      return true;
    }; 

    switch (event.keyCode) {
    case $.ui.keyCode.HOME:
      set_current_slide(0);
      break;
    case $.ui.keyCode.END:
      set_current_slide(num_slides-1);
      break;
    case $.ui.keyCode.RIGHT:
      next_slide();
      break;
    case $.ui.keyCode.LEFT:
      previous_slide();
      break;
    default:
      return true;
      break;
    }
    /* Squash propagation of key events so WebKit-based browsers
       * don't see two of everything.
       */
    event.stopPropagation();
    event.preventDefault();
    return false;
  }

  return function() {
      slides = $('article.slides > section');
      num_slides = slides.size();

      // If there's a hash, start there instead of the first slide
      if (location.hash != "") {
        set_current_slide(slides.index($(location.hash).get(0)));
      } else {
        set_current_slide(0);
      }

      $('#previous-slide').click(previous_slide);
      $('#next-slide').click(next_slide);
      var ignite = $('#ignite');
      if (ignite.size() > 0) {
          $('#ignite').click(ignite);
      } else {
          // avoid binding keys in ignite slides due to
          // contenteditable="" demo
          $('html').bind('keydown', handle_keys);
      }
    };
}();

function browser_support_feature(feature){
    if (feature == undefined) {
        $("#browsersupport").css("display","none");
		$("#nobrowsersupport").css("display","none");
		return false;
    }
    var test_feature = "Modernizr."+feature
	if (eval(test_feature)){
		$("#browsersupport").css("display","block");
		$("#nobrowsersupport").css("display","none");
		return true;
	} else {
		$("#nobrowsersupport").css("display","block");
		$("#browsersupport").css("display","none");
		return false;
	}
}

$(document).ready(Presentation);