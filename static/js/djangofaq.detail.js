// load the answe form after 1 second
setTimeout(function(){
  $('.answer-main').show()}, 1000
);
$('.tab-martor-menu').removeClass('secondary pointing');
$('.martor-preview pre').each(function(i, block){hljs.highlightBlock(block)});

// comment
$(document).keyup(function(){
  if($('textarea[name=description]').val().length >= 10) {
    $('.post-answer-button').removeAttr('disabled');
  }else {
    $('.post-answer-button').attr({'disabled': 'disabled'});
  }
});

/* requirements
  - jQuery
  - hljs
-----------------*/
var baseLoadCommentsUrl = '/comments/offset/';
var baseAddCommentUrl = '/comments/create/';

// load the offset comments
var showMoreComments = function(selector) {
  var selector_data = selector.data('target').split(':');
  var model_name = selector_data[0];
  var object_id = parseInt(selector_data[1]);
  var url = baseLoadCommentsUrl+model_name+'/'+object_id+'/';

  $.ajax({
      url: url,
      type: 'GET',
      async: true,
      cache: false,
      contentType: false,
      success: function(response) {
        var table_tbody = selector.closest('.table-comments tbody');
        table_tbody.append(response);
        selector.remove();

        var tr_actions = 'tr.comment-actions';
        var tr_actions_clone = table_tbody.find(tr_actions).clone();
        table_tbody.find(tr_actions).remove();
        table_tbody.append(tr_actions_clone);

        //hljs.highlightBlock('pre');
      }
  });
}
$(document).on('click', '.show-more-comments', function() {
    showMoreComments($(this));
});

// load the comment form
var addComment = function(selector) {
  var selector_data = selector.data('target').split(':');
  var model_name = selector_data[0];
  var object_id = parseInt(selector_data[1]);
  var url = baseAddCommentUrl+model_name+'/'+object_id+'/';

  $.ajax({
      url: url,
      type: 'GET',
      async: true,
      cache: false,
      contentType: false,
      success: function(response) {
        var table_tbody = selector.closest('.table-comments tbody');
        table_tbody.find('.show-more-comments').trigger('click');
        setTimeout(function(){
          var lastTr = table_tbody.find('tr.comment-actions').last();
          let form = $(response).insertBefore(lastTr);
          form.find('textarea').focus();
        }, 500);
        selector.remove();
      }
  });
}
$(document).on('click', '.add-a-comment', function() {
    addComment($(this));
});
