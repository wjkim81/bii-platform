$(function() {

    var $document = $(document),
        $window = $(window),
        $html = $('html'),
        $body = $('body');


        // 20190528 설명 레이어 추가
        $document.on('click', '.section-calculate .subject a', function(e) {
            e.preventDefault();
            var _desc = $(this).closest('.col');

            var $this = $(this),
                _text = $(this).data('desc');

            $(this).closest('.section-calculate').find('.description').remove();
            $(this).closest('p').after('<div class="description"><div class="module">'+ _text + '</div></div>');
        });

});
